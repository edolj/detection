import os

width = 480
height = 360

for filename in os.listdir("./train_YOLO_format/"):
  #print(filename)
  f = open("./train_YOLO_format/"+filename, "r")
  lines = f.readlines()
  newLine = ""
  for line in lines:
    q, x, y, w, h = map(float, line.split())
    newLine += str(q)+" "+str((x+w/2)/width)+" "+str((y+h/2)/height)+" "+str(w/width)+" "+str(h/height)+"\n"
  f.close()
  
  f2 = open("./train_YOLO_format/"+filename, "w")
  f2.write(newLine)
  newLine = ""
  f2.close()
