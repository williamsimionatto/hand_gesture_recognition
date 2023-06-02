import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
path = []
mode = 0

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

    if mode == 0:
      cv2.putText(image, "Feche as duas maos para encerrar!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    closed_hands = 0  # Contador de mãos fechadas

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

        if mode == 0 and thumb_tip.y < index_tip.y < middle_tip.y < ring_tip.y < pinky_tip.y: # Verificar se a mão está fechada e não está no modo desenho
          closed_hands += 1
        elif mode == 1 and index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and index_tip.y < pinky_tip.y: # Verificar se o dedo indicador está erguido
          cv2.putText(image, "Dedo indicador erguido! Para limpar abra a mao", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

          # Salva as coordenadas do dedo indicador
          index_tip_x = int(index_tip.x * image.shape[1])
          index_tip_y = int(index_tip.y * image.shape[0])
          path.append((index_tip_x, index_tip_y))
          closed_hands = 0

          for i in range(1, len(path)): # Desenhar o caminho do dedo indicador conforme as coordenadas salvas
            cv2.line(image, path[i-1], path[i], (255, 255, 0), 2)
        elif mode == 2:
          cv2.putText(image, "Tkinter Mode", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
          thumbTip = (int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0]))
          indexTip = (int(index_tip.x * image.shape[1]), int(index_tip.y * image.shape[0]))

          cv2.circle(image, thumbTip, 10, (255, 0, 0), -1)  # Adicionar círculo no dedo polegar
          cv2.circle(image, indexTip, 10, (255, 0, 0), -1)  # Adicionar círculo no dedo indicador
          cv2.line(image, thumbTip, indexTip, (255, 0, 0), 2) # Adicionar uma linha ligando o dedo polegar e o dedo indicador

          # Calcular a distância entre os dedos polegar e indicador
          distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
          distance_normalized = min(distance / 0.5, 1.0)  # Normalizar a distância entre 0 e 1

          # Gerar valor para controlar o slider Valor entre 0 e 100
          slider_value = int(distance_normalized * 100)
          cv2.putText(image, f"Slider: {slider_value}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        else:
          path = []
          closed_hands = 0
          cv2.putText(image, "Mao aberta!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if closed_hands == 2:  # Verifica se todas as mãos estão fechadas
      cv2.putText(image, "Todas as mãos estão fechadas! Fechando o programa...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
      cap.release()
      cv2.destroyAllWindows()
      break

    if mode == 1:
      cv2.putText(image, "Drawing mode enabled", (image.shape[1] - 260, image.shape[0] - 700), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.putText(image, "Press D to enable a drawing", (image.shape[1] - 360, image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(image, "Press E to disable a drawing", (image.shape[1] - 360, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Hand Tracking', image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
      break
    elif key == ord('d'):
      mode = 1
    elif key == ord('e'):
      path = []
      mode = 0
    elif key == ord('t'):
      mode = 2

cap.release()
cv2.destroyAllWindows()
