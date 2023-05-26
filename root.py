import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
  static_image_mode=True,
  max_num_hands=2,
  min_detection_confidence=0.5
) as hands:
  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
