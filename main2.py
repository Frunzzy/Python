import cv2
import numpy as np

# Начальные значения настроек
response_brightness = 180
n_size_core = 3
clean_iterations = 2
min_area_contour = 5000
max_contours_to_show = 1
resolution_x = 1280
resolution_y = 720

# Функции обратного вызова для трекбаров
def update_brightness(val):
    global response_brightness
    response_brightness = val

def update_kernel_size(val):
    global n_size_core
    n_size_core = max(1, val)

def update_clean_iterations(val):
    global clean_iterations
    clean_iterations = val

def update_min_area(val):
    global min_area_contour
    min_area_contour = val * 100

def update_max_contours(val):
    global max_contours_to_show
    max_contours_to_show = max(1, val)

def update_resolution_x(val):
    global resolution_x
    resolution_x = val * 100
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)

def update_resolution_y(val):
    global resolution_y
    resolution_y = val * 100
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

# Инициализация камеры
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

# Создание окна с ползунками
cv2.namedWindow('Settings')
cv2.resizeWindow('Settings', 400, 300)

# Создание трекбаров с названиями
cv2.createTrackbar('Brightness', 'Settings', response_brightness, 255, update_brightness)
cv2.createTrackbar('Kernel Size', 'Settings', n_size_core, 15, update_kernel_size)
cv2.createTrackbar('Clean Iter', 'Settings', clean_iterations, 10, update_clean_iterations)
cv2.createTrackbar('Min Area', 'Settings', min_area_contour // 100, 200, update_min_area)
cv2.createTrackbar('Max Contours', 'Settings', max_contours_to_show, 10, update_max_contours)
cv2.createTrackbar('Res X', 'Settings', resolution_x // 100, 20, update_resolution_x)
cv2.createTrackbar('Res Y', 'Settings', resolution_y // 100, 20, update_resolution_y)

# Главный цикл
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Изменение размера кадра под текущие настройки разрешения
    frame = cv2.resize(frame, (resolution_x, resolution_y))
    
    # Основная обработка
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, response_brightness, 255, cv2.THRESH_BINARY)
    kernel = np.ones((n_size_core, n_size_core), np.uint8)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, clean_iterations)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel, clean_iterations)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = contours[:max_contours_to_show]
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_contour:
            valid_contours.append(contour)
    
    for contour in valid_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            cv2.putText(frame, f'({cx},{cy})', (cx+10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
    
    # Отображение окон
    cv2.imshow('Contour', frame)
    cv2.imshow('Threshold', threshold)
    
    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()