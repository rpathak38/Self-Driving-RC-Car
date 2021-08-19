import cv2
import self_driver
import serial_comm

cap = cv2.VideoCapture(0)

while cap.isOpened():
    retVal, frame = cap.read()
    frame = cv2.flip(frame, -1)

    if retVal:
        cv2.imshow("frame", frame)
        print(self_driver.suggested_path(frame)[1])

    else:
        break

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()