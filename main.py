import cv2
import numpy as np

import time

import win32
from audio import AudioHandler, AudioGraph
from fps import FPS, PeriodFPS
from util import map_value
from vision import process_image
from win32 import send_keydown, send_keyup, set_cursor_pos

# =========================== CALIBRATION AND SETTINGS =========================

# Height and width of the capture - this may depend on webcam model
CAPTURE_HEIGHT = 360
CAPTURE_WIDTH = 640

# This should be set to the value of 'Distance' when the dots are at their closest possible point
# (To see 'Distance', Press 'p' while the program is running)
CALIBRATION_IN_LOW = 0.1

# This should be set to the value of 'Distance' when the dots are at their furthest possible point
CALIBRATION_IN_HIGH = 0.45

# This should be set to the Y position of the cursor at the TOP of the play area
# (To see the current cursor Y position, Press 'p' while the program is running)
CALIBRATION_OUT_LOW = 0.15
# this should be set to the Y position of the cursor at the BOTTOM of the play area
CALIBRATION_OUT_HIGH = 0.6

# Set this to the X position of the cursor when the program is running
# This value shouldn't matter much but you might need to change it in multi monitor
# scenarios
CURSOR_X = 0.5

# ==============================================================================


MAX_DIST = np.linalg.norm((CAPTURE_WIDTH, CAPTURE_HEIGHT))


def main():
    cv2.namedWindow("main")

    # Enable camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

    fps = PeriodFPS(10)

    audio_graph = AudioGraph()

    # State
    enable_control = False
    sending_key = False

    with AudioHandler() as audio:
        while True:
            audio.check_exception()
            audio_graph.update(audio.get_data())

            success, img = cap.read()

            blobs, mask, img = process_image(img)

            dist_normalized = None
            out_y = None

            if enable_control:
                is_past_threshold = audio.is_past_threshold()
                if is_past_threshold and not sending_key:
                    sending_key = True
                    send_keydown()

                if not is_past_threshold and sending_key:
                    sending_key = False
                    send_keyup()

                if len(blobs) == 2:
                    dist_raw = np.linalg.norm(np.array(blobs[0]) - np.array(blobs[1]))
                    img = cv2.line(img, blobs[0], blobs[1], (255, 0, 0), 3)
                    dist_normalized = map_value(dist_raw, 0, MAX_DIST, 0, 1)
                    out_y = map_value(dist_normalized, CALIBRATION_IN_LOW, CALIBRATION_IN_HIGH, CALIBRATION_OUT_LOW, CALIBRATION_OUT_HIGH)
                    set_cursor_pos(CURSOR_X, out_y)
            else:
                if sending_key:
                    sending_key = False
                    send_keyup()

            #print(f"Control enabled: {enable_control} Sending key: {sending_key}")

            #cv2.imshow("mask", mask)
            cv2.imshow("main", img)
            cv2.imshow("audio", cv2.flip(audio_graph.array, 0))

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("m"):
                enable_control = not enable_control

            if key == ord("p"):
                print(f"FPS: {fps.get_fps():.3f}")
                cursor_x, cursor_y = win32.get_cursor_pos()
                print(f"Cursor X: {cursor_x:.3f}, Cursor Y: {cursor_y:.3f}")
                if dist_normalized is not None: print(f"Distance: {dist_normalized:.3f}")
                if out_y is not None: print(f"Mouse Y: {out_y:.3f}")
                print(f"Current audio RMS: {audio.get_current_rms()}")

            fps.update()


    cap.release()


if __name__ == "__main__":
    main()