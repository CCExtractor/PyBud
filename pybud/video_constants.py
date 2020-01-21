from pathlib import Path

from PIL import ImageFont


# Color scheme
class Colors:
    background = (41, 45, 52, 255)
    green = (76, 175, 80, 255)
    orange = (190, 138, 89, 255)
    red = (193, 98, 102, 255)
    highlight = (95, 115, 130, 255)
    text_default = (240, 244, 250, 255)
    divider = text_default


# standard 1920x1080 at 1 fps
FPS = 1
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

# line exec section of canvas
LE_XSTART = 6 / 10 * FRAME_WIDTH
LE_YEND = 0.07 * FRAME_HEIGHT

# variable section of canvas
VAR_XSTART = LE_XSTART
VAR_YSTART = LE_YEND

# text properties
CONTAINER_PADDING = 10.0
LINE_SPACING = 0.1
FONT_SIZE = 20
FONT_DIR = Path(__file__).parent / "fonts"
FONT = ImageFont.truetype(str(FONT_DIR / "consolas.ttf"), FONT_SIZE)
