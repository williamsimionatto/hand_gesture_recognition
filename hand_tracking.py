import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
path = []

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

    cv2.putText(image, "Feche a mao para encerrar!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )

        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

        if thumb_tip.y < index_tip.y < middle_tip.y < ring_tip.y < pinky_tip.y: # Verificar se a mão está fechada
          cv2.putText(image, "Mao fechada!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
          cap.release()
          cv2.destroyAllWindows()
          break

        elif index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and index_tip.y < pinky_tip.y: # Verificar se o dedo indicador está erguido
          cv2.putText(image, "Dedo indicador erguido! Para limpar abra a mao", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

          # Salva as coordenadas do dedo indicador
          index_tip_x = int(index_tip.x * image.shape[1])
          index_tip_y = int(index_tip.y * image.shape[0])
          path.append((index_tip_x, index_tip_y))

          for i in range(1, len(path)): # Desenhar o caminho do dedo indicador conforme as coordenadas salvas
            cv2.line(image, path[i-1], path[i], (255, 255, 0), 2)
        else:
          path = []
          cv2.putText(image, "Mao aberta!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
