import cv2
import numpy as np
import settings

settings.window_settings()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.resolution_x) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.resolution_y)
print("Нажмите 'q' для выхода")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, settings.response_brightness, 255, cv2.THRESH_BINARY)
    kernel = np.ones((settings.size_core, settings.size_core), np.uint8)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, settings.clean_iterations)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel, settings.clean_iterations)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = contours[:settings.max_contours_to_show]
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > settings.min_area_contour:
            valid_contours.append(contour)
    cx = cy = 0
    for contour in valid_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"]) # центр масс =сумма координат / площадь(кол-во точек) 
            cy = int(M["m01"]/M["m00"])
            
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            cv2.putText(frame, f'({cx},{cy})', (cx+10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2) # -1 значит что рисуем все контура
    x_to_stm = int(((cx/settings.resolution_x)*100))
    y_to_stm = int(((cy/settings.resolution_y)*100))
    print(x_to_stm, "    ", y_to_stm)
    cv2.imshow('Contour', frame)
    #cv2.imshow('Threshold', threshold)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()


# C:\Users\p151y\Desktop\ЛЭТИ\Diplom\Python\OpenCV>cv_env\Scripts\activate.bat
# (cv_env) C:\Users\p151y\Desktop\ЛЭТИ\Diplom\Python\OpenCV>python main.py


##DFDD