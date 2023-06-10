import cv2
import math
import os.path
import threading
import tkinter as tk
import mediapipe as mp
from tkinter import ttk
from PIL import Image, ImageTk

CURRDIR = os.path.dirname(__file__)

def show_webcam():
  mp_drawing = mp.solutions.drawing_utils
  mp_hands = mp.solutions.hands

  cap = cv2.VideoCapture(0)
  path = []
  mode = 0
  tkinter_mode = 0

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
            thumbFinger = (int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0]))
            indexFinger = (int(index_tip.x * image.shape[1]), int(index_tip.y * image.shape[0]))

            cv2.circle(image, thumbFinger, 10, (255, 0, 0), -1)  # Adicionar círculo no dedo polegar
            cv2.circle(image, indexFinger, 10, (255, 0, 0), -1)  # Adicionar círculo no dedo indicador
            cv2.line(image, thumbFinger, indexFinger, (255, 0, 0), 2) # Adicionar uma linha ligando o dedo polegar e o dedo indicador

            # Calcular a distância entre os dedos polegar e indicador
            distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
            distance_normalized = min(distance / 0.5, 1.0)  # Normalizar a distância entre 0 e 1

            # Gerar valor para controlar o slider Valor entre 0 e 100
            distance_value = int(distance_normalized * 100)
            
            if tkinter_mode == 0:
              cv2.putText(image, "Tkinter Slider Mode", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
              update_slider_value(root, slider, distance_value)
              cv2.putText(image, f"Slider: {distance_value}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            elif tkinter_mode == 1:
              cv2.putText(image, "Tkinter Zoom Mode", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
              update_image_and_zoom(image_label, distance_value)
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
      cv2.putText(image, "Press E to reset modes", (image.shape[1] - 360, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

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
      elif key == ord('c'):
        mode = 2
        tkinter_mode = 0
      elif key == ord('z'):
        mode = 2
        tkinter_mode = 1

  cap.release()
  cv2.destroyAllWindows()
  root.destroy()


def show_tkinter_window(root):
  root.mainloop()

def update_slider_value(root, slider, value):
  slider.set(value)
  label.config(text=f"Slider value: {value}")  # Atualiza o texto da label com o valor atual do slider
  root.update()

# Função para atualizar a imagem e o zoom
def update_image_and_zoom(image_label, distance):
    # Carregar a imagem original

    original_image = Image.open(os.path.join(CURRDIR, 'imgs/hand-landmarks.png'))

    # Definir o fator de zoom com base na distância
    zoom_factor = distance / 100.0
    zoomed_image_width = int(original_image.width * zoom_factor)
    zoomed_image_height = int(original_image.height * zoom_factor)

    # Redimensionar a imagem com o fator de zoom
    zoomed_image = original_image.resize((zoomed_image_width, zoomed_image_height))

    # Converter a imagem para o formato suportado pelo tkinter
    zoomed_image_tk = ImageTk.PhotoImage(zoomed_image)

    # Atualizar a imagem no label
    image_label.configure(image=zoomed_image_tk)
    image_label.image = zoomed_image_tk  # Atualizar a referência da imagem

thread_video = threading.Thread(target=show_webcam)
thread_video.start()

root = tk.Tk()
root.title("Tkinter Window")
root.geometry("600x500")

slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
slider.pack()

label = tk.Label(root, text="Slider value: 0")  # Cria a label com o valor inicial do slider
label.pack()

image_label = tk.Label(root)
image_label.pack()
update_image_and_zoom(image_label, 25)

show_tkinter_window(root)