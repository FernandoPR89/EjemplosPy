import os

thisdir = "C://INEEL_code//Unifilares_original"

# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".desp"):
            print(file[:-5])
