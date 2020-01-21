import importlib
import inspect
import textwrap

import cv2
import numpy as np
from PIL import Image, ImageDraw

from pybud import json_helper
from pybud.printout_builders import *
from pybud.utils import prYellow
from pybud.video.encoders import *
from pybud.video.video_config_handler import *


class VideoLogger:
    def __init__(self, log_path, config_path=str(Path(__file__).parent / "config.yml")):
        self.log_file = json_helper.json_file_to_dict(log_path)

        mod_name = Path(self.log_file["func_path"]).stem
        mod_spec = importlib.util.spec_from_file_location(mod_name, self.log_file["func_path"])
        module = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(module)
        func = getattr(module, self.log_file["func_name"])

        self.config = VideoCFG(config_path)

        # file text
        self.src, self.first_line = inspect.getsourcelines(func)

        # variable section helpers
        self.vars_cache = {}

        # log data
        self.step = 0
        self.step_contents = {}
        self.vars_log = {}

        # image generation tools
        self.frame = None
        self.frame_drawer: ImageDraw = None

        # UI properties
        self.font_width = None
        self.font_height = None

        self.var_sec_width_char = None
        self.var_sec_height_char = None

        self.src_sec_width_char = None

    def init_frame_props(self):
        # print("init frame props")  # DEBUG
        self.frame = Image.new("RGBA", (self.config.frame_width, self.config.frame_height),
                               color=self.config.Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # get the size of a large character
        self.font_width, self.font_height = self.frame_drawer.textsize("|", font=self.config.main_font)

        self.font_height = self.font_height * (1.0 + 2 * self.config.LINE_SPACING)

        self.var_sec_width_char = (self.config.VAR_XEND - self.config.VAR_XSTART - 2 * self.config.CONTAINER_PADDING) // self.font_width
        self.var_sec_height_char = (self.config.VAR_YEND - self.config.VAR_YSTART - 2 * self.config.CONTAINER_PADDING) // self.font_height

        self.src_sec_width_char = (self.config.SRC_XEND - self.config.SRC_XSTART - 2 * self.config.CONTAINER_PADDING) // self.font_width

    def gen_frame(self):
        # print("drawing frame")  # DEBUG
        self.frame = Image.new("RGBA", (self.config.frame_width, self.config.frame_height),
                               color=self.config.Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # draw dividers
        self.frame_drawer.line((self.config.VAR_XSTART, self.config.VAR_YSTART, self.config.VAR_XSTART, self.config.VAR_YEND),
                               fill=self.config.Colors.divider, width=self.config.divider_width)
        self.frame_drawer.line(
            (self.config.LE_XSTART, self.config.LE_YEND, self.config.LE_XEND, self.config.LE_YEND),
            fill=self.config.Colors.divider, width=self.config.divider_width)
        self.frame_drawer.line(
            (self.config.OP_XSTART, self.config.OP_YSTART, self.config.OP_XEND, self.config.OP_YSTART),
            fill=self.config.Colors.divider, width=self.config.divider_width)

        # draw line execution information
        self.gen_line_info()

        # draw the code section
        self.gen_code()

        # draw the variables section
        self.gen_vars()

        # generate watermark if needed
        if self.config.watermark:
            self.gen_watermark()

        # resize to output resolution
        self.resize_frame()

    def gen_vars(self):
        # print("build variables section")  # DEBUG
        var_lines = []
        for var, var_contents in self.vars_log.items():
            # check if this variable has been initialized yet
            var_init: dict = var_contents["init"]
            if var_init["step"] == self.step:
                self.vars_cache[var_init["name"]] = str(var_init["val"])
                # wrap init text
                for line in wrap_text(vid_var_init(var_init["name"], var_init["type"],
                                                   var_init["val"], var_init["line"]), self.var_sec_width_char):
                    var_lines.append({"contents": line, "color": self.config.Colors.green})
                var_lines.append(
                    {"contents": " ", "color": self.config.Colors.text_default})  # add space after variable
            elif var_init["step"] < self.step:
                if len(var_contents["changes"]) != 0:
                    changes, this_change = vid_history_up_to_step(var_contents["changes"], self.step)
                    if this_change is not None:
                        # wrap variable change
                        for line in wrap_text(vid_change_from_to(var_init["name"],
                                                                 self.vars_cache[var_init["name"]],
                                                                 this_change), self.var_sec_width_char):
                            var_lines.append({"contents": line, "color": self.config.Colors.green})
                        self.vars_cache[var_init["name"]] = this_change  # cache variable change
                    else:
                        # wrap variable no change
                        for line in wrap_text(vid_variable(var_init["name"],
                                                           self.vars_cache[var_init["name"]]), self.var_sec_width_char):
                            var_lines.append({"contents": line, "color": self.config.Colors.text_default})
                    # wrap changes text
                    for line in wrap_text(changes, self.var_sec_width_char):
                        var_lines.append({"contents": line, "color": self.config.Colors.text_default})

                else:
                    # wrap variable no change
                    for line in wrap_text(vid_variable(var_init["name"],
                                                       self.vars_cache[var_init["name"]]), self.var_sec_width_char):
                        var_lines.append({"contents": line, "color": self.config.Colors.text_default})
                var_lines.append(
                    {"contents": " ", "color": self.config.Colors.text_default})  # add space after variable

        # print the lines
        for lineno, line in enumerate(var_lines):
            x = self.config.VAR_XSTART + self.config.CONTAINER_PADDING
            y = self.config.VAR_YSTART + self.config.CONTAINER_PADDING + lineno * self.font_height
            self.frame_drawer.text((x, y), line["contents"], font=self.config.main_font, fill=line["color"])

    def gen_code(self):
        # print("build source code section")  # DEBUG
        x_s = self.config.CONTAINER_PADDING + self.config.SRC_XSTART
        y_s = self.config.CONTAINER_PADDING + self.config.SRC_YSTART

        # draw the highlight rectangle
        highlight_start = (float(self.config.SRC_XSTART),
                           float(y_s - self.config.LINE_SPACING + (
                                       self.step_contents["line"]["num"]
                                       - self.first_line) * self.font_height))
        highlight_end = (float(self.config.SRC_XEND - self.config.divider_width),
                         float(y_s + self.config.LINE_SPACING + (
                                     self.step_contents["line"]["num"]
                                     - self.first_line + 1) * self.font_height))
        self.frame_drawer.rectangle((highlight_start, highlight_end), fill=self.config.Colors.highlight)

        # draw the lines
        for adj_line, line in enumerate(self.src):
            self.frame_drawer.text(
                (x_s, y_s + adj_line * self.font_height),
                self.src[adj_line],
                font=self.config.main_font, fill=self.config.Colors.text_default)

    def gen_line_info(self):
        line: dict = self.step_contents["line"]
        text = live_step(self.step) + " " + live_line(line["num"], line["cnt"], line["total"])

        text = "\n".join(textwrap.wrap(text, width=self.src_sec_width_char))
        self.frame_drawer.text((self.config.CONTAINER_PADDING + self.config.LE_XSTART, self.config.CONTAINER_PADDING),
                               text, font=self.config.main_font,
                               fill=self.config.Colors.orange)

    def gen_watermark(self):
        x = self.config.frame_width - self.config.CONTAINER_PADDING
        y = self.config.frame_height - self.config.CONTAINER_PADDING
        w_font = ImageFont.truetype(str(self.config.FONT_DIR / "UbuntuMono-B.ttf"), 40)
        # create transparent overlay
        overlay = Image.new("RGBA", (self.config.frame_width, self.config.frame_height), (255, 255, 255, 0))
        o_draw = ImageDraw.Draw(overlay)
        w, h = o_draw.textsize("Generated by PyBud", font=w_font)
        x -= w
        y -= h

        o_draw.text((x, y), "Generated by PyBud", fill=self.config.Colors.watermark_color, font=w_font)
        self.frame = Image.alpha_composite(self.frame, overlay)

    def resize_frame(self):
        self.frame = self.frame.resize((self.config.output_width, self.config.output_height))

    def draw_intro_frame(self):
        self.frame = Image.new("RGBA", (self.config.frame_width, self.config.frame_height),
                               color=self.config.Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        x = self.config.frame_width / 2
        y = self.config.frame_height / 2
        w, h = self.frame_drawer.textsize(self.config.intro_text, font=self.config.intro_font)
        self.frame_drawer.text((x - w / 2, y - h / 2), self.config.intro_text, font=self.config.intro_font,
                               fill=self.config.intro_color)
        # resize image to output resolution
        self.resize_frame()

    def generate(self, vid_path):
        prYellow("# Generating video rendering of PyBud program flow... #")
        # init video writer
        if ".mp4" in vid_path:
            writer: OutputEncoder = MP4Encoder(vid_path, self.config.fps, self.config.output_width, self.config.output_height)
        else:
            writer: OutputEncoder = GIFEncoder(vid_path, self.config.fps)

        # draw intro frames if needed
        if self.config.intro_text:
            self.draw_intro_frame()
            for _ in range(round(self.config.intro_time * self.config.fps)):
                writer.write_frame(self.frame)

        self.init_frame_props()  # init frame properties, ie padding, text size, etc.
        self.vars_log = self.log_file["vars_log"]  # grab the variable log

        for step, contents in self.log_file["steps"].items():  # draw and write frame for each step
            self.step = int(step)
            self.step_contents = contents
            self.gen_frame()
            writer.write_frame(self.frame)
        writer.save()  # save the output
        prYellow("# Video rendering complete! #")


def wrap_text(text, cols):
    lines = text.split("\n")

    # Wrap text
    wrapped_lines = []
    for line in lines:
        line_wrapped = textwrap.wrap(line, width=cols)
        if len(line_wrapped) == 0:
            wrapped_lines.append("")
        else:
            wrapped_lines += line_wrapped

    return wrapped_lines
