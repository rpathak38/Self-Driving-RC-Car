import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    retVal, frame = cap.read()
    frame = cv2.flip(frame, -1)
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if retVal:
        cv2.imshow("frame", frame)
        cv2.imwrite("laneImage.jpg", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
