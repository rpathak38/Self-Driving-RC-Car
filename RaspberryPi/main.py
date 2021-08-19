import cv2
import self_driver
import serial_comm

serial_comm.serial_input_ping(serial_command="Engage \n")
cap = cv2.VideoCapture(0)

while cap.isOpened():
    retVal, frame = cap.read()
    frame = cv2.flip(frame, -1)

    if retVal:
        serial_comm.serial_input_ping(serial_command="dc 255")
        try:
            angle = self_driver.suggested_path(frame, True)[1]
        except TypeError:
            serial_comm.serial_input_ping(serial_command="reset")
            break
        serial_comm.serial_input_ping(serial_command="servo " + str(angle) + "\n")

    else:
        serial_comm.serial_input_ping(serial_command="reset")
        break

    if cv2.waitKey(1) == ord("q"):
        serial_comm.serial_input_ping(serial_command="reset")
        break

cap.release()
cv2.destroyAllWindows()
