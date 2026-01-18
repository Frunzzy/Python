@echo off
echo ============================================
echo ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С NUMPY 2.4.0
echo ============================================
echo.

echo 1. Выходим из текущего окружения...
call deactivate 2>nul

echo 2. Удаляем старое окружение...
if exist cv_env rmdir /s /q cv_env

echo 3. Создаем новое окружение...
python -m venv cv_env

echo 4. Активируем...
call cv_env\Scripts\activate

echo 5. Устанавливаем NumPy 1.24.3 (важно первым!)...
pip install numpy==1.24.3

echo 6. Устанавливаем OpenCV 4.8.1.78...
pip install opencv-python==4.8.1.78

echo 7. Проверка...
python -c "import numpy as np; print('NumPy версия:', np.__version__)"
python -c "import cv2; print('OpenCV версия:', cv2.__version__)"

echo.
echo ============================================
echo Тестовый скрипт...
echo ============================================

echo import cv2 > test_fix.py
echo import numpy as np >> test_fix.py
echo. >> test_fix.py
echo print("Тест после исправления") >> test_fix.py
echo print("-" * 40) >> test_fix.py
echo print(f"NumPy: {np.__version__}") >> test_fix.py
echo print(f"OpenCV: {cv2.__version__}") >> test_fix.py
echo. >> test_fix.py
echo img = np.zeros((100, 100, 3), dtype=np.uint8) >> test_fix.py
echo img[30:70, 30:70] = [0, 255, 0]  # Зеленый квадрат >> test_fix.py
echo cv2.imwrite('test_success.jpg', img) >> test_fix.py
echo print("Изображение сохранено: test_success.jpg") >> test_fix.py
echo. >> test_fix.py
echo # Проверка камеры >> test_fix.py
echo cap = cv2.VideoCapture(0) >> test_fix.py
echo if cap.isOpened(): >> test_fix.py
echo     print("Камера обнаружена") >> test_fix.py
echo     cap.release() >> test_fix.py
echo else: >> test_fix.py
echo     print("Камера не найдена") >> test_fix.py
echo. >> test_fix.py
echo print("-" * 40) >> test_fix.py
echo print("✅ ВСЁ РАБОТАЕТ!") >> test_fix.py

echo.
echo Запускаю тест...
python test_fix.py

echo.
pause