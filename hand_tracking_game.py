import cv2
import mediapipe as mp
import random

def show_text(frame, text, position, font_size=1):
  cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), 2, cv2.LINE_AA)


def check_winner(player_gesture, computer_gesture):
  if player_gesture == computer_gesture:
    return "Tie"

  if (
    (player_gesture == "rock" and computer_gesture == "scissors") or 
    (player_gesture == "paper" and computer_gesture == "rock") or 
    (player_gesture == "scissors" and computer_gesture == "paper")
  ):
    return "Winner"

  return "Loser"


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

player_score = 0
computer_score = 0
game_started = False
player_gesture_last = None
player_gesture = None
gestures = ["rock", "paper", "scissors"]
computer_gesture = ""
result = "Tie"

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
          player_gesture_last = player_gesture
          player_gesture = "Paper"
        elif (
          thumb_tip < index_finger_tip
          and thumb_tip < middle_finger_tip
          and thumb_tip < ring_finger_tip
          and thumb_tip < pinky_tip
        ):
          player_gesture_last = player_gesture
          player_gesture = "Rock"
        elif (
          thumb_tip < thumb_ip and middle_finger_tip < middle_finger_dip
        ):
          player_gesture_last = player_gesture
          player_gesture = "Scissors"
        else:
          player_gesture = None

        if (player_gesture and game_started):
          if (player_gesture_last != player_gesture):
            computer_gesture = random.choice(gestures)
            result = check_winner(player_gesture, computer_gesture)

            if result == "Winner":
              player_score += 1
            elif result == "Loser":
              computer_score += 1

          show_text(frame, "Computer: {}".format(computer_gesture), (frame.shape[1] - 250, 80), font_size=0.7)
          show_text(frame, "Player: {}".format(player_gesture), (frame.shape[1] - 250, 40), font_size=0.7)
          show_text(frame, result, (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)))

    if game_started:
      show_text(frame, "Player = {}".format(player_score), (20, 40))
      show_text(frame, "Computer = {}".format(computer_score), (20, 80))
      show_text(frame, "Press Q to finish game", (20, frame.shape[0] - 20))
    else:
      show_text(frame, "Press S to start game", (20, frame.shape[0] - 20))

    key = cv2.waitKey(1)
    cv2.imshow("Rock Paper Scissor Game", frame)

    if key == ord("s") and not game_started:
      game_started = True
      player_score = 0
      computer_score = 0
    
    if key == ord("q"):
      result_final = "Tie"
      if player_score > computer_score:
        result_final = "Victory"
      elif player_score < computer_score:
        result_final = "Defeat"

      print(result_final)
      show_text(frame, result_final, (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)))
      cv2.imshow("Rock Paper Scissor Game", frame)
      cv2.waitKey(2000)
      break


cap.release()
cv2.destroyAllWindows()
