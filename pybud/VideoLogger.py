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

        self.var_char_width = None
        self.var_char_height = None

        self.code_char_width = None

    def init_frame_props(self):
        print("init frame props")
        self.frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), color=Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        self.font_width, self.font_height = self.frame_drawer.textsize("T", font=FONT)

        self.font_height = self.font_height * 1.2

        self.var_char_width = (FRAME_WIDTH - LE_XSTART - 2 * LINE_PADDING) // self.font_width
        self.var_char_height = (FRAME_HEIGHT - LE_YEND - 2 * LINE_PADDING) // self.font_height

        self.code_char_width = (LE_XSTART - 2 * LINE_PADDING) // self.font_width

    def gen_frame(self):
        print("drawing frame")
        self.frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), color=Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # draw dividers
        self.frame_drawer.line((VAR_XSTART, 0, VAR_XSTART, FRAME_HEIGHT), fill=Colors.divider, width=1)
        self.frame_drawer.line((LE_XSTART, LE_YEND, FRAME_WIDTH, LE_YEND), fill=Colors.divider, width=1)

        # draw line execution information
        self.gen_line_info()

        # draw the code section
        self.gen_code()

        # draw the variables section

    def gen_var(self):
        print("build variables section")
        # TODO: implement

    def gen_code(self):
        print("build source code section")
        # draw the highlight rectangle
        highlight_start = (0,
                           LINE_PADDING + (self.step_contents["line"]["num"] - self.first_line) * self.font_height)
        highlight_end = (VAR_XSTART,
                         LINE_PADDING + (self.step_contents["line"]["num"] - self.first_line + 1) * self.font_height)
        self.frame_drawer.rectangle((highlight_start, highlight_end), fill=Colors.highlight)

        # draw the lines
        for adj_line, line in enumerate(self.src):
            self.frame_drawer.text((LINE_PADDING, LINE_PADDING + adj_line * self.font_height), self.src[adj_line],
                                   font=FONT, fill=Colors.text_default)

    def gen_line_info(self):
        line: dict = self.step_contents["line"]
        text = live_step(self.step) + " " + live_line(line["num"], line["cnt"], line["total"])

        text = "\n".join(textwrap.wrap(text, width=self.var_char_width))
        self.frame_drawer.text((LINE_PADDING + LE_XSTART, LINE_PADDING), text, font=FONT, fill=Colors.text_default)

    def generate(self, vid_path):
        self.init_frame_props()  # init frame properties, ie padding, text size, etc.
        self.vars_log = self.log_file["vars_log"]  # grab the variable log

        # init video writer
        writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        for step, contents in self.log_file["steps"].items():  # draw and write frame for each step
            self.step = step
            self.step_contents = contents
            self.gen_frame()
            writer.write(cv2.cvtColor(np.asarray(self.frame), cv2.COLOR_RGB2BGR))
        writer.release()
