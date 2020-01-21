from abc import ABC, abstractmethod

import cv2
import numpy as np
from PIL import Image


class OutputEncoder(ABC):

    @abstractmethod
    def write_frame(self, frame):
        pass

    @abstractmethod
    def save(self):
        pass


class GIFEncoder(OutputEncoder):
    def __init__(self, vid_path, fps):
        self.frames = []
        self.vid_path = vid_path
        self.duration = 1000 / fps

    def write_frame(self, frame: Image):
        self.frames.append(frame)

    def save(self):
        self.frames[0].save(self.vid_path, save_all=True, append_images=self.frames[1:], duration=self.duration, loop=0)


class MP4Encoder(OutputEncoder):
    def __init__(self, vid_path, fps, width, height):
        self.writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                      (width, height))

    def write_frame(self, frame: Image):
        self.writer.write(cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR))

    def save(self):
        self.writer.release()
