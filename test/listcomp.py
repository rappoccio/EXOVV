import glob, os
f = open('images.txt', 'w')
for file in glob.glob("unfolded*_fullband_*.pdf"):
    f.write(file + "\n")
f.close()
print "To generate the tar file, please use the following command: tar -cvf images.tar -T images.txt"
quit()
