import cv2
import numpy as np
import io


def buffer2cv(buffer):
    return cv2.imdecode(np.frombuffer(buffer, np.uint8), 1)


# def buffer_for_npy(buffer):
#     return np.load(io.BytesIO(buffer), allow_pickle=True)
