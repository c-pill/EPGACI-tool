Tool based on EPGACI created and described in my research paper "ACCURATELY SCRAMBLING IMAGES USING EVOLUTIONARY COMPUTATION AS AN ALTERNATIVE MEAN OF CENSORSHIP" (available "https://github.com/c-pill/Generating-ACIs").

This tool uses an updated version of EPGACI.

Updates to EPGACI:
- memory management: uses memory management to keep the amount of memory used throughout the program to a minimum. Old version waited to the end to release memory which caused memory usage to build up (too many generations could crash)

- smart_swap_mutate: tweaked when formula for getting max_pixels when fitness < 0

- individuals are pointers to pixels rather than arrays of pixels. Only converted to arrays to display images. Helps with memory management.


This tool implements a GUI for easier modification to values given to EPGACI. This tool also changes how EPGACI is used.

Values modifiable from GUI:
- number of individuals in population
- number of generations to compute
- goal % similarity
- image to censor

Changes to how EPGACI is used: 
- now only censors a portion of the selected image based on the user's drawing boundaries of portion
- does not technically save image (saved briefly to display with correct name and then is deleted)
- image may be saved once displayed


Files/Folders in repository:
- images: stores default image when no image is selected
- EPGACI-tool.exe: executable version of EPGACI-tool.py
- EPGACI-tool.py: code that runs tool
- EPGACI.c: c file used in EPGACI
- EPGACI.py: code that runs EPGACI
- EPGACI.so: c library created from EPGACI.c
- EPGACI-noGUI.py: functionally this tool without its GUI 


Note: EPGACI-tool.exe MUST stay in the its folder to work properly. Create a shortcut if you want to move it elsewhere 