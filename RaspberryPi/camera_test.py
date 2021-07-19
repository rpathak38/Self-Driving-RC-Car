import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    retVal, frame = cap.read()
    frame = cv2.flip(frame, 0)

    if retVal:
        cv2.imshow("frame", frame)
        cv2.imwrite("laneImage.jpg", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
