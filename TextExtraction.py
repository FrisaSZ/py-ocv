import cv2
import numpy as np

img = cv2.imread('D:/Images/Text/text0.bmp')
cv2.imshow('Text', img)
cv2.waitKey(0)
cv2.destroyAllWindows()