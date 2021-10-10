import cv2
import numpy as np
image = cv2.imread('earth.jpg')
cv2.imshow('text', image)
cv2.waitKey(0)
cv2.destroyAllWindows()