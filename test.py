import numpy as np
import cv2
img=np.array([[1,2,3],[4,5,6],[7,8,9]]).astype(float)

# Compute the horizontal gradient (sobelx8u) and the absolute gradient (sobel_8u)
sobelx8u = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
sobelx64f = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
abs_sobel64f = np.absolute(sobelx64f)
sobel_8u = np.uint8(abs_sobel64f)

print("Original matrix:")
print(img)
print("Horizontal gradient (sobelx8u):")
print(sobelx8u)
print("Absolute gradient (sobel_8u):")
print(sobel_8u)