import importlib
import inspect
import textwrap

import cv2
import numpy as np
from PIL import Image, ImageDraw

from pybud import json_helper
from pybud.printout_builders import *
from pybud.video_constants import *


class VideoLogger:
    def __init__(self, log_path):
        self.log_file = json_helper.json_file_to_dict(log_path)

        mod_name = Path(self.log_file["func_path"]).stem
        mod_spec = importlib.util.spec_from_file_location(mod_name, self.log_file["func_path"])
        module = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(module)
        func = getattr(module, self.log_file["func_name"])

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

        # UI props
        self.font_width = None
        self.font_height = None

        self.var_sec_width_char = None
        self.var_sec_height_char = None

        self.src_sec_width_char = None

    def init_frame_props(self):
        # print("init frame props")  # DEBUG
        self.frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), color=Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # get the size of a large character
        self.font_width, self.font_height = self.frame_drawer.textsize("|", font=FONT)

        self.font_height = self.font_height * (1.0 + 2 * LINE_SPACING)

        self.var_sec_width_char = (FRAME_WIDTH - LE_XSTART - 2 * CONTAINER_PADDING) // self.font_width
        self.var_sec_height_char = (FRAME_HEIGHT - LE_YEND - 2 * CONTAINER_PADDING) // self.font_height

        self.src_sec_width_char = (LE_XSTART - 2 * CONTAINER_PADDING) // self.font_width

    def gen_frame(self):
        # print("drawing frame")  # DEBUG
        self.frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), color=Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # draw dividers
        self.frame_drawer.line((VAR_XSTART, 0, VAR_XSTART, FRAME_HEIGHT), fill=Colors.divider, width=3)
        self.frame_drawer.line((LE_XSTART, LE_YEND, FRAME_WIDTH, LE_YEND), fill=Colors.divider, width=3)

        # draw line execution information
        self.gen_line_info()

        # draw the code section
        self.gen_code()

        # draw the variables section
        self.gen_vars()

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
                    var_lines.append({"contents": line, "color": Colors.green})
                var_lines.append({"contents": " ", "color": Colors.text_default})  # add space after variable
            elif var_init["step"] < self.step:
                if len(var_contents["changes"]) != 0:
                    changes, this_change = vid_history_up_to_step(var_contents["changes"], self.step)
                    if this_change is not None:
                        self.vars_cache[var_init["name"]] = this_change  # cache variable change
                        # wrap variable change
                        for line in wrap_text(vid_change_from_to(var_init["name"],
                                                                 self.vars_cache[var_init["name"]],
                                                                 this_change), self.var_sec_width_char):
                            var_lines.append({"contents": line, "color": Colors.green})
                    else:
                        # wrap variable no change
                        for line in wrap_text(vid_variable(var_init["name"],
                                                           self.vars_cache[var_init["name"]]), self.var_sec_width_char):
                            var_lines.append({"contents": line, "color": Colors.text_default})
                    # wrap changes text
                    for line in wrap_text(changes, self.var_sec_width_char):
                        var_lines.append({"contents": line, "color": Colors.text_default})

                else:
                    # wrap variable no change
                    for line in wrap_text(vid_variable(var_init["name"],
                                                       self.vars_cache[var_init["name"]]), self.var_sec_width_char):
                        var_lines.append({"contents": line, "color": Colors.text_default})
                var_lines.append({"contents": " ", "color": Colors.text_default})  # add space after variable

        # print the lines
        for lineno, line in enumerate(var_lines):
            x = VAR_XSTART + CONTAINER_PADDING
            y = VAR_YSTART + CONTAINER_PADDING + lineno * self.font_height
            self.frame_drawer.text((x, y), line["contents"], font=FONT, fill=line["color"])

    def gen_code(self):
        # print("build source code section")  # DEBUG
        # draw the highlight rectangle
        highlight_start = (float(0.0),
                           float(CONTAINER_PADDING - LINE_SPACING + (self.step_contents["line"]["num"]
                                                                     - self.first_line) * self.font_height))
        highlight_end = (float(VAR_XSTART - 3),
                         float(CONTAINER_PADDING + LINE_SPACING + (self.step_contents["line"]["num"]
                                                                   - self.first_line + 1) * self.font_height))
        self.frame_drawer.rectangle((highlight_start, highlight_end), fill=Colors.highlight)

        # draw the lines
        for adj_line, line in enumerate(self.src):
            self.frame_drawer.text((CONTAINER_PADDING, CONTAINER_PADDING + adj_line * self.font_height), self.src[adj_line],
                                   font=FONT, fill=Colors.text_default)

    def gen_line_info(self):
        line: dict = self.step_contents["line"]
        text = live_step(self.step) + " " + live_line(line["num"], line["cnt"], line["total"])

        text = "\n".join(textwrap.wrap(text, width=self.var_sec_width_char))
        self.frame_drawer.text((CONTAINER_PADDING + LE_XSTART, CONTAINER_PADDING), text, font=FONT, fill=Colors.text_default)

    def generate(self, vid_path):
        self.init_frame_props()  # init frame properties, ie padding, text size, etc.
        self.vars_log = self.log_file["vars_log"]  # grab the variable log

        # init video writer
        writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        for step, contents in self.log_file["steps"].items():  # draw and write frame for each step
            self.step = int(step)
            self.step_contents = contents
            self.gen_frame()
            writer.write(cv2.cvtColor(np.asarray(self.frame), cv2.COLOR_RGB2BGR))
        writer.release()


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
