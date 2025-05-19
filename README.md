# Pyano - Piano with Python

A virtual Piano implemented using Python.

On running the program, *fingersound.py*, a virtual piano appears on the top half of the screen. 

This program uses OpenCV for Computer Vision and MediaPipe for hand tracking. 

It recognises the fingertips and whenever the fingertips enter the area of the key, those notes are played.

## Idea and Implementation

First install OpenCV and MediaPipe for camera and hand tracking functionalities.  
Can use hand gestures to play the on screen virtual piano.

Each hand has 21 landmarks(0-20)  
Each finger has landmarks, and the fingertips are:  
Thumb - 4  
Index Finger - 8  
Middle Finger - 12  
Ring Finger - 16  
Pinky Finger - 20  

Sectioned the area on the screen for different keys and when the fingertips enter a section that key is played.

I used pygame for adding sound and created a sound folder with all the necessary sounds(notes)

Downloaded the notes from [here](https://www.github.com/parisjava/wav-piano-sound)

Downloaded new notes from [here](https://www.github.com/plemaster01/PythonPiano)

Then I noticed that it does not work properly for multiple key pressing. So, added that.

Also included key highlight for the pressed key.
