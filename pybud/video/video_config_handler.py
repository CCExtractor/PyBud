from pathlib import Path

import yaml
from PIL import ImageFont


class VideoCFG(object):
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.yml: dict = yaml.load(f, Loader=yaml.FullLoader)

        # Color scheme
        self.Colors = Colors()

        # Display settings
        self.intro_text = self.yml["intro"]["text"]
        self.intro_time = self.yml["intro"]["time"]
        self.watermark = self.yml["watermark"]

        # Frame properties
        self.FPS = self.yml["fps"]
        self.FRAME_WIDTH = 1920
        self.FRAME_HEIGHT = 1080
        self.DIVIDER_WIDTH = 3

        # line exec section of canvas
        self.LE_XSTART = 6 / 10 * self.FRAME_WIDTH
        self.LE_YEND = 0.07 * self.FRAME_HEIGHT

        # variable section of canvas
        self.VAR_XSTART = self.LE_XSTART
        self.VAR_YSTART = self.LE_YEND

        # text properties
        self.CONTAINER_PADDING = 10.0
        self.LINE_SPACING = 0.1
        self.FONT_SIZE = self.yml["font"]["font-size"]
        self.FONT_DIR = Path(__file__).parent / ".." / "fonts"
        self.FONT = ImageFont.truetype(str(self.FONT_DIR / self.yml["font"]["font-family"]), self.FONT_SIZE)


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
