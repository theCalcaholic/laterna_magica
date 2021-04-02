import cv2
import numpy as np

frame_0 = cv2.imread('resource/test/Archaeologist-Tux-icon.png')
shape_0 = frame_0.shape[:]

offset = (shape_0[0], shape_0[1])

frame_0_left_bottom = (5, 5)

frame_0_right_top = (
    frame_0_left_bottom[0] + shape_0[0],
    frame_0_left_bottom[1] + shape_0[1]
)

new_shape = [shape_0[0] + 5, shape_0[1] + 5]

new_shape.extend(shape_0[2:])
new_frame = np.zeros(tuple(new_shape))

print(new_shape)
print(frame_0_left_bottom)
print(frame_0_right_top)
print(new_frame.shape)

new_frame[frame_0_left_bottom[0]:frame_0_right_top[0], frame_0_left_bottom[1]:frame_0_right_top[1]] = frame_0

cv2.imshow('debug', new_frame)

cv2.waitKey(0)
