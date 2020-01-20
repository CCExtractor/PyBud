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

        self.var_char_width = (FRAME_WIDTH - LE_XSTART - 2 * LINE_PADDING) // self.font_width
        self.var_char_height = (FRAME_HEIGHT - LE_YSTART - 2 * LINE_PADDING) // self.font_height

        self.code_char_width = (LE_XSTART - 2 * LINE_PADDING) // self.font_width

    def gen_frame(self):
        print("drawing frame")
        self.frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), color=Colors.background)
        self.frame_drawer = ImageDraw.Draw(self.frame)  # connect the image drawer to this frame

        # draw dividers
        self.frame_drawer.line((VAR_XSTART, 0, VAR_XSTART, FRAME_HEIGHT), fill=Colors.divider, width=1)
        self.frame_drawer.line((LE_XSTART, LE_YSTART, FRAME_WIDTH, LE_YSTART), fill=Colors.divider, width=1)

        # draw line execution information
        self.gen_line_info()

    def gen_var(self):
        print("build variables section")
        # TODO: implement

    def gen_code(self):
        print("build source code section")
        # TODO: implement

    def gen_line_info(self):
        line: dict = self.step_contents["line"]
        text = live_step(self.step) + " " + live_line(line["num"], line["cnt"], line["total"])

        text = "\n".join(textwrap.wrap(text, width=self.var_char_width))
        self.frame_drawer.text((LINE_PADDING + LE_XSTART, LINE_PADDING), text, font=FONT, fill=Colors.text_default)

    def generate(self, vid_path):
        self.init_frame_props()
        writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        self.vars_log = self.log_file["vars_log"]
        for step, contents in self.log_file["steps"].items():
            self.step = step
            self.step_contents = contents
            self.gen_frame()
            writer.write(cv2.cvtColor(np.asarray(self.frame), cv2.COLOR_RGB2BGR))
        writer.release()
