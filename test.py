
import os
filename = "calibration_record.txt"
print(os.getcwd())
a = os.getcwd()
filepath = os.path.join(a, filename)
print(filepath)

  
# Path 
path = "/home"
  
# Join various path components  
print(os.path.join(path, filename, "file.txt")) 