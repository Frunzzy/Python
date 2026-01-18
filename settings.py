import cv2
import numpy as np

#    Default Settings

response_brightness = 180
size_core = 3
clean_iterations = 2
min_area_contour = 5000
max_contours_to_show = 1
resolution_x = 1280
resolution_y = 720

# -----------------------

def update_brightness(val):
    global response_brightness
    response_brightness = val
def update_size_core(val):
    global size_core
    size_core = val
def update_clean_iterations(val):
    global clean_iterations
    clean_iterations = val
def update_min_area(val):
    global min_area_contour
    min_area_contour = val
def update_max_contours(val):
    global max_contours_to_show
    max_contours_to_show = val
def window_settings():   
    cv2.namedWindow("Settings")
    cv2.resizeWindow ("Settings", 400, 200)
    cv2.createTrackbar("Brightness", "Settings", 0, 255, update_brightness)
    cv2.createTrackbar("Size Core", "Settings", 0, 15, update_size_core)
    cv2.createTrackbar('Clean Iter', 'Settings', 1, 10, update_clean_iterations)
    cv2.createTrackbar('Min Area', 'Settings', 1000, 300000, update_min_area)
    cv2.createTrackbar('Max Contours', 'Settings', 1, 10, update_max_contours)