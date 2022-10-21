# Tromboner

This is a visual/audio way to play Trombone Champ.

## Setup instructions

This program only supports Windows.
* Install Python (3.9+)
* Create a virtual environment:
  * `python -m venv env`
  * `.\env\Scripts\activate`
  * Remember to run `.\env\Scripts\activate` in a new terminal before running any scripts in the future
* Install required packages:
  * `pip install -r requirements.txt`

## Running the program

The program works by monitoring the audio and video feed, and sending commands which will override
the mouse control and send keyboard presses. The program only controls the mouse when it sees 2 colored
dots. To take back control of the mouse, just obscure the dots from view of the camera.

* Run the program
  * `python main.py`
* Run Trombone Champ
* When you're ready to play, press `m` to toggle mouse and keyboard override. A line between the 2 colored dots will show up when the program is taking control of the mouse.
* The audio input levels will be shown in a window. The yellow line represents the volume threshold (See audio.py for calibration)

### Controls
* `q` - quit the program
* `m` - toggle activating mouse and keyboard override
* `p` - print debug values (useful for calibration)

### Calibration and settings
Modify constants in the following files to calibrate the setup:

* `main.py` - for general calibration
* `vision.py` - for calibrating color and camera input related factors
* `audio.py` - for calibrating audio input