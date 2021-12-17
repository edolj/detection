import os

folder = "./doneLabels/"

for filename in os.listdir(folder):
    oldName = filename
    newName = oldName[0:4] + ".txt"
    
    old = os.path.join(folder, oldName)
    new = os.path.join(folder, newName)
    os.rename(old, new)
