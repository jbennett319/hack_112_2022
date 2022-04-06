Summary - Group 11's project is a diet version of wii sports baseball. Using the mediapie hand tracking module, we track the movements of a players hand to determine a swing location 
and speed. Then an animation plays throwing a randomly selected pitch in {fastball, slider, etc} (which animates and has the physical properties of said pitch type). The launch force,
trajectory, elevation gain, etc are then calculated using OOP. The pitching will continue until the player hits the q key.

Module - Mediapipe: https://google.github.io/mediapipe/solutions/solutions.html:
This can be installed using pip by running "pip install mediapipe". This should install the other required modules as well (including opencv2). The open cv2 is used to handle image captures
from the camera.

The tracking mechanics itself are almost plug and play, but actually accessing the data was a Herculean task, since it uses the craziest data structure we've ever seen, 
so it took a TON of webscraping to get info on its functionality and data storing norms. The only code we directly stripped (stackOverflow) was for getting the max and can be found here
(https://stackoverflow.com/questions/19448078/python-opencv-access-webcam-maximum-resolution)

A full list of all the sources that we used is listed below:
https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/hands.py
https://google.github.io/mediapipe/solutions/solutions.html
https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html

HOW TO USE OUR PROGRAM:
1. Navigate to the file named run_game.py.
2. Running this code willbring up a camera window (please give the camera a few moments to boot up as this often takes some time). You will need to put your left hand behind your back
   or out of view. This will allow the program to only track your right hand. When ready to swing, place your hand in the red rectangle as indicated on the screen to start the timer.
3. One the timer begins to count down, the program is preparing for your swing. A swing includes taking a capture of where your hand is when the timer hits 0. You will then have a brief
   moment to move your hand to a new location where it will take a second screenshot.
4. If your swing was invalid (i.e. you did not move your hand far enough) then the program will automatically reset.
5. There are a few things to note about your swing:
   - the total distance that your hand moves determines where the bat is when the ball makes contact with the bat. Larger distances will produce a move optimal swing by hitting the ball
     later and thus with a better angle of attack.
   - the y distance that you are from the bottom of the camera window will determine where the bat makes contact with the ball. For example if you finish your swing close to the bottom
     of the screen, then you will hit the ball closer to the bottom and produce a pop fly. Alternatively if you finish your swing close to the top of the screen you will hit the ball
     on its top and drive it into teh ground quicker. All being said, the more optinal swings are thise that finish in the middle if the window, but you may use your own judgement
     for the result you desire.
6. Once the swing data is collected, the program runs a series of computations to find the 3D path of the ball.
7. The program will then automatically display that path from a birds eye view of the field. A vew notes on reading the screen output:
   - a black ball means that it is still in the air and a red ball means that it has hit the ground and is rolling to its final destination
   - a larger ball means that it is higher up, i.e. closer to the screen from the top down view provided. Conversely a smaller ball means that it is closer to the ground.
8. Once the program has finished running, close the view window and run again if desired.

We apologize for the less than ideal UI, but the core fuctionality of the program is here and this is the best way to run the program that we could put together in limited time
Thanks!