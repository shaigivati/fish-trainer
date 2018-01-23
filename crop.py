import cv2
img = cv2.imread("back2fish.png")
crop_img = img[350:580, 0:1920] # Crop from x, y, w, h -> 100, 200, 300, 400
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
cv2.imwrite("cropped.png", crop_img)
cv2.waitKey(0)