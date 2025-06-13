import cv2
import numpy as np
import math

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Tamaño del teclado (60% del original)
keyboard_scale = 0.6
keyboard_width = int(1000 * keyboard_scale)
keyboard_height = int(400 * keyboard_scale)  # Reducido para mejor proporción

# Diseño del teclado QWERTY (filas completas)
keys_set_qwerty = {
    # Fila superior (Q W E R T Y U I O P)
    'Q': (50, 20), 'W': (120, 20), 'E': (190, 20), 'R': (260, 20), 'T': (330, 20),
    'Y': (400, 20), 'U': (470, 20), 'I': (540, 20), 'O': (610, 20), 'P': (680, 20),
    
    # Fila media (A S D F G H J K L Ñ)
    'A': (80, 80), 'S': (150, 80), 'D': (220, 80), 'F': (290, 80), 'G': (360, 80),
    'H': (430, 80), 'J': (500, 80), 'K': (570, 80), 'L': (640, 80), 'Ñ': (710, 80),
    
    # Fila inferior (Z X C V B N M , . -)
    'Z': (110, 140), 'X': (180, 140), 'C': (250, 140), 'V': (320, 140), 'B': (390, 140),
    'N': (460, 140), 'M': (530, 140), ',': (600, 140), '.': (670, 140), '-': (740, 140),
    
    # Barra espaciadora y tecla de borrado
    ' ': (250, 200, 300, 40),  # Espacio (x, y, ancho, alto)
    '<-': (600, 200, 100, 40)  # Borrar
}

# Escalar las coordenadas del teclado
keys_set_scaled = {}
for key, value in keys_set_qwerty.items():
    if key in [' ', '<-']:
        keys_set_scaled[key] = tuple(int(v * keyboard_scale) for v in value)
    else:
        keys_set_scaled[key] = tuple(int(v * keyboard_scale) for v in value)

# Parámetros para detección de manos
background = None
accumulated_weight = 0.5
roi_top, roi_bottom, roi_right, roi_left = 100, 300, 300, 600

# --- FUNCIONES ---
def calc_accum_avg(frame, accumulated_weight):
    global background
    if background is None:
        background = frame.copy().astype("float")
        return
    cv2.accumulateWeighted(frame, background, accumulated_weight)

def segment_hand(frame, threshold=25):
    global background
    diff = cv2.absdiff(background.astype("uint8"), frame)
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return (thresholded, max(contours, key=cv2.contourArea)) if contours else None

def count_fingers(thresholded, hand_segment):
    conv_hull = cv2.convexHull(hand_segment)
    extremes = {
        'top': tuple(conv_hull[conv_hull[:, :, 1].argmin()][0]),
        'bottom': tuple(conv_hull[conv_hull[:, :, 1].argmax()][0]),
        'left': tuple(conv_hull[conv_hull[:, :, 0].argmin()][0]),
        'right': tuple(conv_hull[conv_hull[:, :, 0].argmax()][0])
    }
    cX = (extremes['left'][0] + extremes['right'][0]) // 2
    cY = (extremes['top'][1] + extremes['bottom'][1]) // 2
    
    distance = math.sqrt((extremes['right'][0] - extremes['left'][0])**2 + 
                         (extremes['right'][1] - extremes['left'][1])**2)
    radius = int(distance * 0.3)
    
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    cv2.circle(circular_roi, (cX, cY), radius, 255, 10)
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
    
    contours, _ = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    count = 0
    for cnt in contours:
        (_, y, _, h) = cv2.boundingRect(cnt)
        if (cY + (cY * 0.25)) > (y + h) and (2 * math.pi * radius * 0.25) > cnt.shape[0]:
            count += 1
    return count

def draw_keyboard():
    keyboard = np.zeros((keyboard_height, keyboard_width, 3), np.uint8)
    keyboard.fill(50)  # Fondo gris oscuro
    
    for key, value in keys_set_scaled.items():
        key_size = 50 * keyboard_scale
        if key in [' ', '<-']:
            x, y, w, h = value
            color = (255, 0, 0) if key == '<-' else (255, 255, 255)
            cv2.rectangle(keyboard, (x, y), (x+w, y+h), color, 2)
            cv2.putText(keyboard, key, (x+10, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            x, y = value
            cv2.rectangle(keyboard, (x, y), (x+int(key_size), y+int(key_size)), (255, 255, 255), 2)
            cv2.putText(keyboard, key, (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Añadir título
    cv2.putText(keyboard, "TECLADO VIRTUAL QWERTY", (int(keyboard_width*0.2), 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    return keyboard

def get_key_pressed(x, y):
    key_size = 50 * keyboard_scale
    for key, value in keys_set_scaled.items():
        if key in [' ', '<-']:
            x_k, y_k, w, h = value
            if x_k <= x <= x_k+w and y_k <= y <= y_k+h:
                return key
        else:
            x_k, y_k = value
            if x_k <= x <= x_k+key_size and y_k <= y <= y_k+key_size:
                return key
    return None

# --- PROGRAMA PRINCIPAL ---
text = ""
frames_elapsed = 0
key_pressed = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()
    
    # ROI para detección de mano
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Calibración inicial
    if frames_elapsed < 60:
        calc_accum_avg(gray, accumulated_weight)
        cv2.putText(frame_copy, "CALIBRANDO... MANTENGA LA MANO EN EL AREA", 
                   (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        hand = segment_hand(gray)
        
        if hand:
            thresholded, hand_segment = hand
            cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0), 2)
            
            fingers = count_fingers(thresholded, hand_segment)
            cv2.putText(frame_copy, f"Dedos: {fingers}", (70, 45), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            if fingers == 1:
                M = cv2.moments(hand_segment)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"]) + roi_right
                    cY = int(M["m01"] / M["m00"]) + roi_top
                    cv2.circle(frame_copy, (cX, cY), 7, (0, 255, 0), -1)
                    
                    # Mapear a coordenadas del teclado
                    key_x = int((cX - roi_right) * (keyboard_width / (roi_left - roi_right)))
                    key_y = int((cY - roi_top) * (keyboard_height / (roi_bottom - roi_top)))
                    
                    key = get_key_pressed(key_x, key_y)
                    if key and key_pressed != key:
                        key_pressed = key
                        if key == '<-':
                            text = text[:-1]
                        else:
                            text += key
    
    frames_elapsed += 1
    
    # Dibujar ROI
    cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0, 0, 255), 2)
    
    # Crear teclado
    keyboard_img = draw_keyboard()
    
    # Mostrar texto
    cv2.putText(keyboard_img, f"Texto: {text}", (20, int(keyboard_height*0.9)), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Redimensionar y combinar
    cam_height, cam_width = frame_copy.shape[:2]
    scale_factor = keyboard_height / cam_height
    resized_cam = cv2.resize(frame_copy, (int(cam_width*scale_factor), keyboard_height))
    combined = np.hstack((resized_cam, keyboard_img))
    
    cv2.imshow("Teclado Virtual QWERTY con Camara", combined)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()