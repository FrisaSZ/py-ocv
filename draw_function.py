import numpy as np
import cv2

img = np.zeros((720, 1280, 3), np.uint8)
cv2.line(img, (0, 0), (767, 767), (255, 156, 0), 10)
cv2.circle(img, (512, 384), 100, (128, 255, 255), 3)
cv2.ellipse(img, (512, 384), (200, 150), 45, 0, 270, (0, 0, 255), -1)
pts = np.array([[100, 100], [200, 50], [300, 50], [400, 100], [250, 300]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], True, (0, 255, 255), 3)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'CookCooller', (100, 512), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imwrite('D:/draw.png', img)
cv2.destroyAllWindows()