# Prime Tower as an Exclude Object
This script searches the gcode file from Orca Slicer to find the extents of the prime tower, then adds it as an exclude object.
_WHY?_ you may ask. Well, if you're using Klipper Adaptive Bed Mesh, it won't scan the area outside of the exclude objects. So, the answer is to put it in an exclude object.

Now, just as a word of caution, I would not try to exclude the prime tower during a print. I haven't tried it. I probably wont. But I can't see anything good coming of it.
