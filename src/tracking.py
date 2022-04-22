import numpy as np
from cv2 import cv2

ESC_KEYPRESS = 27 

# identifica a camera 
# mudar para 0 ou 1 caso tenha webcam para identificar a realsense
cap = cv2.VideoCapture(1)

def setLimitsOfTrackBar():
    hue = {}
    hue["min"] = cv2.getTrackbarPos("Min Hue", trackbarWindow)
    hue["max"] = cv2.getTrackbarPos("Max Hue", trackbarWindow)
    if hue["min"] > hue["max"]:
        cv2.setTrackbarPos("Max Hue", trackbarWindow, hue["min"])
        hue["max"] = cv2.getTrackbarPos("Max Hue", trackbarWindow)

    sat = {}
    sat["min"] = cv2.getTrackbarPos("Min Saturation", trackbarWindow)
    sat["max"] = cv2.getTrackbarPos("Max Saturation", trackbarWindow)
    if sat["min"] > sat["max"]:
        cv2.setTrackbarPos("Max Saturation", trackbarWindow, sat["min"])
        sat["max"] = cv2.getTrackbarPos("Max Saturation", trackbarWindow)

    val = {}
    val["min"] = cv2.getTrackbarPos("Min Value", trackbarWindow)
    val["max"] = cv2.getTrackbarPos("Max Value", trackbarWindow)
    if val["min"] > val["max"]:
        cv2.setTrackbarPos("Max Value", trackbarWindow, val["min"])
        val["max"] = cv2.getTrackbarPos("Max Value", trackbarWindow)
    return hue, sat, val

def computeTracking(frame, hue, sat, val):
    # converte a imagem para HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define os intervalos de cores que irão aparecer na imagem final
    lowerColor = np.array([hue["min"], sat["min"], val["min"]])
    upperColor = np.array([hue["max"], sat["max"], val["max"]])

    # marcador para saber se o pixel pertence ao intervalo
    mask = cv2.inRange(hsvImage, lowerColor, upperColor)

    # compara a mascara com imagem e filtra 
    result = cv2.bitwise_and(frame, frame, mask = mask)

    # aplica LIMIARIZAÇÃO
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # encontra os contornos
    contours, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # retorna a area do primeiro grupo de pixels brancos
        maxArea = cv2.contourArea(contours[0]) 
        contourMaxAreaId = i = 0

        for cont in contours:
            if maxArea < cv2.contourArea(cont):
                maxArea = cv2.contourArea(cont)
                contourMaxAreaId = i
            i += 1
        
        # contorno com maior area
        contMaxArea = contours[contourMaxAreaId]

        # Desenha um retangulo que envolve a area
        xRect, yRect, wRect, hRect = cv2.boundingRect(contMaxArea)
        cv2.rectangle(frame, (xRect, yRect), (xRect + wRect, yRect + hRect), (0, 0, 255), 2)
    return frame, gray

def onChange(val):
    return

# ===================== CRIA AS TRACKBAR NA JANELA ======================
# cria janela
trackbarWindow = "trackbar window"
cv2.namedWindow(trackbarWindow)

cv2.createTrackbar("Min Hue", trackbarWindow, 0, 255, onChange)
cv2.createTrackbar("Max Hue", trackbarWindow, 255, 255, onChange)
cv2.createTrackbar("Min Saturation", trackbarWindow, 0, 255, onChange)
cv2.createTrackbar("Max Saturation", trackbarWindow, 255, 255, onChange)
cv2.createTrackbar("Min Value", trackbarWindow, 0, 255, onChange)
cv2.createTrackbar("Max Value", trackbarWindow, 255, 255, onChange)

# ======================= PEGA AS TRACKBAR ==========================
min_hue = cv2.getTrackbarPos("Min Hue", trackbarWindow)
max_hue = cv2.getTrackbarPos("Max Hue", trackbarWindow)
min_sat = cv2.getTrackbarPos("Min Saturation", trackbarWindow)
max_sat = cv2.getTrackbarPos("Max Saturation", trackbarWindow)
min_val = cv2.getTrackbarPos("Min Value", trackbarWindow)
max_val = cv2.getTrackbarPos("Max Value", trackbarWindow)

while True:
    success, frame = cap.read()

    hue, sat, val = setLimitsOfTrackBar()
    frame, gray = computeTracking(frame, hue, sat, val)

    cv2.imshow("mask", gray)
    cv2.imshow("webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or 0xFF == ESC_KEYPRESS:
        break

# destroi e limpa a memoria
cap.release()
cv2.destroyAllWindows()

