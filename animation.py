import numpy as np
import random
import math
from PIL import Image, ImageDraw, ImageOps

class keyFrame:

    def __init__(self, list):
        # this one figures out the dimensions from the highest and lowest number
        
        maxNum = max(list)
        minNum = min(list)

        

    def __init__(self, pointsList, spacesList, xDim, yDim, directRead = None):
    
        if(directRead):  # this will be the clicktracker input
        
            self.pointsList = []
            self.spacesList = []
            self.xDim = xDim
            self.yDim = yDim
            self.numPoints = 0
            self.numSpaces = 0
            
            self.xFloats = []
            self.yFloats = []
        
            count = 0
            nextSkip = False
            for element in pointsList:
                if(count % 2 == 0):
                    if(element == -1):
                        nextSkip = True
                        self.numSpaces = self.numSpaces + 1
                    else:
                        self.yFloats.append((element * 1.0 / xDim))
                        if (nextSkip):
                            self.spacesList.append(1)
                        else:
                            self.spacesList.append(0)
                        nextSkip = False
                        self.numPoints = self.numPoints + 1
                else:
                    if(element != -1):
                        self.xFloats.append((element * 1.0 / yDim))
                count = count + 1
                        
            self.spacesList = np.array(self.spacesList)
            self.xFloats = np.array(self.xFloats)
            self.yFloats = np.array(self.yFloats)
                        
        else:
            self.pointsList = pointsList
            self.spacesList = spacesList  #represents lines or gaps between points, with 1 for gap, 0 for line. last space must be 1 because n-1 spaces for n points
            self.xDim = xDim
            self.yDim = yDim
            self.numPoints = len(pointsList)
            self.numSpaces = np.sum(spacesList)
        
            self.xFloats = np.zeros((self.numPoints), dtype=np.float64)
            self.yFloats = np.zeros((self.numPoints), dtype=np.float64)
      
            for i in range(self.numPoints):
                self.xFloats[i] = ((pointsList[i] % xDim) * 1.0) / xDim
                self.yFloats[i] = ((pointsList[i] / xDim) * 1.0) / yDim
      
    def getPointIndex(point):
        return pointsList[point], spacesList[point]
        
    def getPointXY(point):
        return pointsList[point] % xDim, pointsList[point] / xDim, spacesList[point]


class animation:
    def __init__(self):
        self.keyFrames = []
    
    def addKeyFrame(self, keyFrame):
        self.keyFrames.append(keyFrame)
        
    def animateLine(self, draw , y1, x1, y2, x2, gap1, gap2, stepOverSteps):
        # just handle the gaps here for fuck sake god damn
        
        
        
        #gap1 = random.randrange(2)
        #gap2 = random.randrange(2)
        
        dot = 4
        
        if(gap1 == 0 and gap2 == 0):
            draw.ellipse((  y1-dot , x1-dot ,  y1+dot , x1+dot ), fill = 'white')
            draw.line(( y1 , x1 , y2 , x2),  width=10, fill='white')
            
        if(gap1 == 1 and gap2 == 1):
            draw.ellipse((  y1-dot , x1-dot ,  y1+dot , x1+dot ), fill = 'white')
            #draw.line(( y1 , x1 , y2 , x2),  width=10, fill='white')
            
        if(gap1 == 1 and gap2 == 0):
            draw.ellipse((  y1-dot , x1-dot ,  y1+dot , x1+dot ), fill = 'white')
            halfStep = stepOverSteps / 2 
            deltaX = x1 - x2
            deltaY = y1 - y2
            
            # draw dots between original points and halfway to midpoint depending on step
            
            draw.ellipse(( y1-(halfStep * deltaY) - dot, x1-(halfStep * deltaX) - dot,  y1-(halfStep * deltaY) + dot, x1-(halfStep * deltaX) + dot), fill= 'white')
            draw.line(( y1 , x1 , y1-(halfStep * deltaY) , x1-(halfStep * deltaX)),  width=10, fill='white')
            
            draw.ellipse(( y2+(halfStep * deltaY) - dot, x2+(halfStep * deltaX) - dot,  y2+(halfStep * deltaY) + dot, x2+(halfStep * deltaX) + dot), fill= 'white')
            draw.line(( y2 , x2 , y2+(halfStep * deltaY) , x2+(halfStep * deltaX)),  width=10, fill='white')
            
        if(gap1 == 0 and gap2 == 1):
            draw.ellipse((  y1-dot , x1-dot ,  y1+dot , x1+dot ), fill = 'white')
            halfStep = ((1-stepOverSteps) / 2) 
            deltaX = x1 - x2
            deltaY = y1 - y2
            
            # draw dots between original points and halfway to midpoint depending on step
            
            draw.ellipse(( y1-(halfStep * deltaY) - dot, x1-(halfStep * deltaX) - dot,  y1-(halfStep * deltaY) + dot, x1-(halfStep * deltaX) + dot), fill= 'white')
            draw.line(( y1 , x1 , y1-(halfStep * deltaY) , x1-(halfStep * deltaX)),  width=10, fill='white')
            
            draw.ellipse(( y2+(halfStep * deltaY) - dot, x2+(halfStep * deltaX) - dot,  y2+(halfStep * deltaY) + dot, x2+(halfStep * deltaX) + dot), fill= 'white')
            draw.line(( y2 , x2 , y2+(halfStep * deltaY) , x2+(halfStep * deltaX)),  width=10, fill='white')
        
    # frame1 is the first keyframe
    # frame2 is the second keyfraome
    # steps is the number of intermediate frames to render
    # start is the number to start couting from for the files getting saved
    # path is the path to save to
    # im is an image to bring in (if you want the motion blur from that last keyframe)
    
    # the function saves the frames directly, and returns the last frame (in case you want to not clear the blur between keyframes, and pass it to the next set)
        
    def interpolate(self, frame1, frame2, steps, start = 0, path = ".", im = None):
        
        source = []
        
        target = []
        
        # if there is a gap there needs to be two of the same on the other side
        #
       
        breakBool = False
        
        if(frame1.numPoints >= frame2.numPoints):
            
            diff = frame1.numPoints - frame2.numPoints
            
            ratio = diff * 1.0 / (frame2.numPoints-1)
            
            count1 = 0 # counter for frame1
            count2 = 0 # counter for frame2
            extra1 = 0
            extra2 = 0
            mixin  = 1  # counter for mixing in extra for frame2 to match frame2
            
            #print frame1.numPoints
            #print frame1.numSpaces
            #print frame2.numPoints
            #print frame2.numSpaces
            
            #print ratio
            
            sourceX = []
            sourceY = []
            targetX = []
            targetY = []
        
            sourceSkips = frame1.spacesList
            targetSkips = []
            
            for i in range(frame2.numPoints):

                if(mixin > 1):
                    while(mixin > 1):
                        if(len(targetX) < frame1.numPoints):
                            targetX.append(frame2.xFloats[count2])
                            targetY.append(frame2.yFloats[count2])
                            targetSkips.append(0) #frame2.spacesList[count2])
                            mixin = mixin - 1
                if(len(targetX) < frame1.numPoints):
                    targetX.append(frame2.xFloats[count2])
                    targetY.append(frame2.yFloats[count2])
                    #print targetSkips
                    targetSkips.append(frame2.spacesList[count2])
                    count2 = count2 + 1
                    mixin = mixin + ratio
                                 
            sourceX = frame1.xFloats
            sourceY = frame1.yFloats
                    
            #print len(targetY)
            #print len(sourceY)

            #print len(targetX)
            #print len(sourceX)            
                    
        else:
        
            diff = frame2.numPoints - frame1.numPoints
        
            ratio = diff * 1.0 / (frame1.numPoints-1)
            
            count1 = 0 # counter for frame1
            count2 = 0 # counter for frame2
            extra1 = 0
            extra2 = 0
            mixin  = 1  # counter for mixing in extra for frame2 to match frame2
            
            #print frame1.numPoints
            #print frame1.numSpaces
            #print frame2.numPoints
            #print frame2.numSpaces
            
            #print ratio
            
            sourceX = []
            sourceY = []
            targetX = []
            targetY = []
        
            sourceSkips = []
            targetSkips = frame2.spacesList
            
            for i in range(frame1.numPoints):

                if(mixin > 1):
                    while(mixin > 1):
                        if(len(sourceX) < frame2.numPoints):
                            sourceX.append(frame1.xFloats[count2])
                            sourceY.append(frame1.yFloats[count2])
                            sourceSkips.append(0) #frame2.spacesList[count2])
                            mixin = mixin - 1
                if(len(sourceX) < frame2.numPoints):
                    sourceX.append(frame1.xFloats[count2])
                    sourceY.append(frame1.yFloats[count2])
                    sourceSkips.append(frame1.spacesList[count2])
                    count2 = count2 + 1
                    mixin = mixin + ratio
                                 
            targetX = frame2.xFloats
            targetY = frame2.yFloats
                    
            #print len(targetY)
            #print len(sourceY)

            #print len(targetX)
            #print len(sourceX)  
            
        targetX = np.array(targetX) * 1000
        targetY = np.array(targetY) * 1000
        
        sourceX = np.array(sourceX) * 1000
        sourceY = np.array(sourceY) * 1000
                
        diffX =  targetX - sourceX
        diffY =  targetY - sourceY
        
        diffX = np.true_divide(diffX, steps)
        diffY = np.true_divide(diffY, steps)
        
        resultX = np.zeros((steps, targetX.shape[0]))
        resultY = np.zeros((steps, targetX.shape[0]))
        
        if(im == None):
            im = Image.new("RGB", (1080, 1080), "black")  # this is black to start because it's simpler to do blur decay inverted then switch back
        
        for i in range(steps):
    
            fraction =  (i * 1.0) + 1 # / steps
        
            ##print(np.multiply(diffX, fraction))
    
            resultX[i,:] = np.copy(sourceX + np.multiply(diffX, fraction))
            resultY[i,:] = np.copy(sourceY + np.multiply(diffY, fraction))

            matrix = np.asarray(im)
            
            matrix = np.floor_divide(matrix, 32)
            
            matrix = matrix * 31  # this part is for the motion blur, it's just 31 / 32 the value of the old frame, exponential decay
            
            im = Image.fromarray(matrix)
            
            draw = ImageDraw.Draw(im)
            #draw2 = ImageDraw.Draw(im2)
            
            #dot1 = 5.071065
            
            #dot = dot1 + (i * (9.1421 - 5.071065)/steps)
            
            dot = 4
            
            border1 =  1000.0/ frame1.xDim 
            
            border2 =  1000.0/ frame2.xDim 
            
            for j in range(len(diffX)-1):
            
                border = 40 + ((border1 * 1.0 * (steps-i)) / steps + (border2 * 1.0 * i) / steps) / 2
            
                ##print (len(diffX))
                ##print j
            
                draw.ellipse((  resultY[i,j]-dot + border, resultX[i,j]-dot + border,  resultY[i,j]+dot + border, resultX[i,j]+dot + border ), fill = 'white')
                self.animateLine(draw, resultY[i,j] + border, resultX[i,j] + border, resultY[i,j+1] + border, resultX[i,j+1] + border, sourceSkips[j+1], targetSkips[j+1], (i * 1.0)/steps) 
                #if(sourceSpace[j+1] == 0): # or i > (steps/2-10)):
                #
                #draw.line(( resultY[i,j] , resultX[i,j] ,  resultY[i,j+1], resultX[i,j+1] ),  width=10, fill='black')
                #else:
                #    draw.ellipse((  resultY[i,j]-dot , resultX[i,j]-dot ,  resultY[i,j]+dot , resultX[i,j]+dot ), fill = 'black')

            
            draw.ellipse((  resultY[i,len(diffX)-1]-dot + border , resultX[i,len(diffX)-1]-dot + border,  resultY[i,len(diffX)-1]+dot + border, resultX[i,len(diffX)-1]+dot + border ), fill = 'white')
            
            del draw

            ImageOps.invert(im).save("%s/%s.png" % (path, (i + start)))
            
        return im

        
    