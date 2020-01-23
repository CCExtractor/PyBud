from pathlib import Path

import yaml
from PIL import ImageFont


class VideoCFG(object):
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.yml: dict = yaml.load(f, Loader=yaml.FullLoader)
        self.FONT_DIR = Path(__file__).parent / ".." / "fonts"

        # Color scheme
        self.Colors = Colors()

        # Variable display settings
        self.muted_variables = self.yml["muted-variables"]

        # Display settings
        self.intro_text = self.yml["intro"]["text"]
        self.intro_time = self.yml["intro"]["time"]
        self.intro_font = ImageFont.truetype(str(self.FONT_DIR / self.yml["intro"]["font-family"]), self.yml["intro"]["font-size"])
        self.intro_color = self.yml["intro"]["color"]
        self.watermark = self.yml["watermark"]
        self.output_width = self.yml["output-resolution"]["width"]
        self.output_height = self.yml["output-resolution"]["height"]

        # Frame properties
        self.fps = self.yml["fps"]
        self.frame_width = self.yml["render-resolution"]["width"]
        self.frame_height = self.yml["render-resolution"]["height"]
        self.divider_width = 3

        # Line exec section of canvas
        self.LE_XSTART = 0.0
        self.LE_XEND = 2 / 3 * self.frame_width
        self.LE_YSTART = 0.0
        self.LE_YEND = 0.06 * self.frame_height

        # Variable section of canvas
        self.VAR_XSTART = self.LE_XEND
        self.VAR_XEND = self.frame_width
        self.VAR_YSTART = 0.0
        self.VAR_YEND = self.frame_height

        # Output section of canvas
        self.OP_XSTART = 0.0
        self.OP_XEND = self.VAR_XSTART
        self.OP_YSTART = 0.89 * self.frame_height
        self.OP_YEND = self.frame_height

        # Source code section of canvas
        self.SRC_XSTART = 0.0
        self.SRC_XEND = self.VAR_XSTART
        self.SRC_YSTART = self.LE_YEND
        self.SRC_YEND = self.OP_YSTART

        # Text properties
        self.CONTAINER_PADDING = 10.0
        self.LINE_SPACING = 0.1
        self.font_size = self.yml["font"]["font-size"]
        self.main_font = ImageFont.truetype(str(self.FONT_DIR / self.yml["font"]["font-family"]), self.font_size)


class Colors(VideoCFG, object):
    def __init__(self):
        self.background = (41, 45, 52, 255)
        self.green = (76, 175, 80, 255)
        self.orange = (190, 138, 89, 255)
        self.red = (193, 98, 102, 255)
        self.highlight = (95, 115, 130, 255)
        self.text_default = (240, 244, 250, 255)
        self.watermark_color = (255, 255, 255, 90)
        self.divider = self.text_default
