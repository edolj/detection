import os
import math

width = 480
height = 360

folder = "./labelsGray480/"

for filename in os.listdir(folder):
  #print(filename)
  f = open(folder+filename, "r")
  lines = f.readlines()
  newLine = ""
  for line in lines:
    q, x, y, w, h = map(float, line.split())
    #x*width -w/2, y*height - h/2, w*width, h*height
    newLine += str(int(q))+" "+str(int(math.ceil((x-w/2)*width)))+" "+str(int(math.ceil((y- h/2)*height)))+" "+str(int(math.ceil(w*width)))+" "+str(int(math.ceil(h*height)))+"\n"
  f.close()
  
  f2 = open(folder+filename, "w")
  f2.write(newLine)
  newLine = ""
  f2.close()
