from matplotlib import pyplot as plt
import cv2

img = cv2.imread('D:/Lena.jpg')
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()