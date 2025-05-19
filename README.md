# Pyano - Piano with Python

A virtual Piano implemented using Python.

On running the program a virtual piano appears on the top half of the screen. 

This program uses OpenCV for Computer Vision and MediaPipe for hand tracking. 

It recognises the fingertips and whenever the fingertips enter the area of the key, those notes are played.

## Idea and Implementation

First install OpenCV and MediaPipe for camera and hand tracking functionalities

each hand has 21 landmarks(0-20)
Each finger has landmarks, and the fingertips are:
Thumb - 4
Index Finger - 8
Middle Finger - 12
Ring Finger - 16
Pinky Finger - 20

We are using pygame for adding sound

We are also creating a sound folder with all the necessary sounds(notes)

Downloaded the notes from [here](https://www.github.com/parisjava/wav-piano-sound)

Downloaded new notes from [here](https://www.github.com/plemaster01/PythonPiano)

Then I noticed that it does not work properly for multiple key pressing. So, added that.

Also included key highlight for the pressed key.
