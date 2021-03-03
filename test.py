import cv2 
cv2.namedWindow("windowName")
img = cv2.imread("Uten navn.png")
def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 3, (0,255,0), -1)
            cv2.destroyAllWindows()

cv2.setMouseCallback("windowName", draw_circle)
cv2.imshow("windowName", img)
cv2.waitKey(0)
cv2.imshow("windowName", img)
cv2.waitKey(0)
cv2.destroyAllWindows()