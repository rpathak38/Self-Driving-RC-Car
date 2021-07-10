import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    retVal, frame = cap.read()

    if retVal:
        cv2.imshow(frame)
    else:
        break

    if cv2.waitKey("q"):
        break

cap.release()
cv2.destroyAllWindows()
