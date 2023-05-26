import cv2

cap = cv2.VideoCapture(0)

# status of camera
while cap.isOpened():
  ret, frame = cap.read()

  if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  ## window height and width
  cv2.imshow('Cam', gray)

  if cv2.waitKey(1) == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()