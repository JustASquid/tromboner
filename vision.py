import numpy as np
import cv2

# =========================== CALIBRATION AND SETTINGS =========================

# These control the color range for what is accepted as a "dot".
# e.g. if you want to use red dots instead of green, replace the first (H)
# value in these tuples with the 0-255 HSV value for red
LOWER_BOUND_HSV = (50, 20, 20)
UPPER_BOUND_HSV = (100, 255, 255)

# ==============================================================================

KERNEL_SIZE = 3
EROSION_ITERATIONS = 3

def process_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_bound = np.array(LOWER_BOUND_HSV)
    upper_bound = np.array(UPPER_BOUND_HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KERNEL_SIZE, KERNEL_SIZE))
    mask = cv2.erode(mask, kernel, iterations=EROSION_ITERATIONS)

    contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)
    contours = contours[:2]

    blobs = []

    for contour in contours:
        # box = cv2.boundingRect(contour)
        # img = cv2.rectangle(img, box, (0, 255, 0))

        moments = cv2.moments(contour)
        if moments["m00"] > 0:
            c_x = int(moments["m10"] / moments["m00"])
            c_y = int(moments["m01"] / moments["m00"])

            img = cv2.circle(img, (c_x, c_y), radius=10, color=(255, 0, 0), thickness=2)

            blobs.append((c_x, c_y))

    return blobs, mask, img