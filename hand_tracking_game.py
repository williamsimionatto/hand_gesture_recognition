import cv2
import mediapipe as mp
import random

def mostrar_texto(imagem, texto, posicao, tamanho_fonte=1):
  cv2.putText(imagem, texto, posicao, cv2.FONT_HERSHEY_SIMPLEX, tamanho_fonte, (255, 0, 0), 2, cv2.LINE_AA)


def verificar_vencedor(player_gesto, computer_gesto):
  if player_gesto == computer_gesto:
    return "Tie"

  if (
    (player_gesto == "rock" and computer_gesto == "scissors") or 
    (player_gesto == "paper" and computer_gesto == "rock") or 
    (player_gesto == "scissors" and computer_gesto == "paper")
  ):
    return "Winner"

  return "Loser"


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

player_score = 0
computer_score = 0
game_started = False
player_gesto_last = None
player_gesto = None
gestos = ["rock", "paper", "scissors"]
computer_gesto = ""
resultado = "Tie"

with mp_hands.Hands(
  min_detection_confidence=0.5,
  min_tracking_confidence=0.5
) as hands:
  while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
        ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

        if (
          thumb_tip > index_finger_tip
          and thumb_tip > middle_finger_tip
          and thumb_tip > ring_finger_tip
          and thumb_tip > pinky_tip
        ):
          player_gesto_last = player_gesto
          player_gesto = "paper"
        elif (
          thumb_tip < index_finger_tip
          and thumb_tip < middle_finger_tip
          and thumb_tip < ring_finger_tip
          and thumb_tip < pinky_tip
        ):
          player_gesto_last = player_gesto
          player_gesto = "rock"
        elif (
          thumb_tip < thumb_ip and middle_finger_tip < middle_finger_dip
        ):
          player_gesto_last = player_gesto
          player_gesto = "scissors"
        else:
          player_gesto = None

        if (player_gesto and game_started):
          if (player_gesto_last != player_gesto):
            computer_gesto = random.choice(gestos)
            resultado = verificar_vencedor(player_gesto, computer_gesto)

            if resultado == "Winner":
              player_score += 1
            elif resultado == "Loser":
              computer_score += 1

          mostrar_texto(frame, "Computer: {}".format(computer_gesto), (frame.shape[1] - 250, 80), tamanho_fonte=0.7)
          mostrar_texto(frame, "Player: {}".format(player_gesto), (frame.shape[1] - 250, 40), tamanho_fonte=0.7)
          mostrar_texto(frame, resultado, (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)))

    if game_started:
      mostrar_texto(frame, "Player = {}".format(player_score), (20, 40))
      mostrar_texto(frame, "Computer = {}".format(computer_score), (20, 80))
      mostrar_texto(frame, "Press Q to finish game", (20, frame.shape[0] - 20))
    else:
      mostrar_texto(frame, "Press S to start game", (20, frame.shape[0] - 20))

    key = cv2.waitKey(1)
    cv2.imshow("Gesture Recognition", frame)

    if key == ord("s") and not game_started:
      game_started = True
      player_score = 0
      computer_score = 0
    
    if key == ord("q"):
      resultado_final = "Tie"
      if player_score > computer_score:
        resultado_final = "Victory"
      elif player_score < computer_score:
        resultado_final = "Defeat"

      print(resultado_final)
      mostrar_texto(frame, resultado_final, (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)))
      cv2.imshow("Gesture Recognition", frame)
      cv2.waitKey(2000)
      break


cap.release()
cv2.destroyAllWindows()
