import numpy as np
import cv2

start_point = [0, 0]
end_point = [0, 0]
segment_color = [255, 156, 0]
img = np.zeros((900, 1600, 3), np.uint8)

while(True):
    key = cv2.waitKey(0) & 0xFF

    if key == ord('w'):
        start_point[1] -= 5
    if key == ord('s'):
        start_point[1] += 5
    if key == ord('a'):
        start_point[0] -= 5
    if key == ord('d'):
        start_point[0] += 5
    if key == ord('i'):
        end_point[1] -= 5
    if key == ord('k'):
        end_point[1] += 5
    if key == ord('j'):
        end_point[0] -= 5
    if key == ord('l'):
        end_point[0] += 5
    if key == 27:
        break
    img_draw = img.copy()
    cv2.line(img_draw, tuple(start_point), tuple(end_point), tuple(segment_color), 5)
    cv2.imshow('img', img_draw)

cv2.destroyAllWindows()