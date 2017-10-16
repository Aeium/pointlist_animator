from animation import keyFrame, animation
import numpy as np

# basic example

anim = animation()

# making arrays for points

point2 = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160])
point1 = np.array([7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168])

# code to test spaces merging

spaces1 = np.zeros_like(point1)
spaces2 = np.zeros_like(point2)

spaces1[3] = 1
spaces1[5] = 1
spaces1[9] = 1

spaces2[1] = 1
#spaces2[4] = 1
#spaces2[7] = 1
#spaces2[9] = 1
#spaces2[13] = 1
#spaces2[15] = 1
#spaces2[22] = 1

keyFrame1 = keyFrame(point1, spaces1, 13, 13)
keyFrame2 = keyFrame(point2, spaces2, 13, 13)

# you will need to make the folders for the output

anim.interpolate(keyFrame1, keyFrame2, 200, path= "output1")

# direct read from clicktracker file example

words = np.genfromtxt('words_again.txt', delimiter=',')
words2 = np.genfromtxt('words2_again.txt', delimiter=',')

keyFrame3 = keyFrame(words, 0, 1080, 1080, True)
keyFrame4 = keyFrame(words2, 0, 1080, 1080, True)


anim.interpolate(keyFrame3, keyFrame4, 200, start = 200, path = "output2")