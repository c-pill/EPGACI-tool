# EPGACI-tool
- Tool based on the EPGACI I developed and described in my research paper "ACCURATELY SCRAMBLING IMAGES USING EVOLUTIONARY COMPUTATION AS AN ALTERNATIVE MEAN OF CENSORSHIP" (available "https://github.com/c-pill/Generating-ACIs").

## Updates to EPGACI:
- memory management: resolved memory management issues present during my research
- Individuals in each generation is now represented as a pointer rather than the actual array of pixels

### Added functions:
- smart_swap_mutate: tweaked when formula for getting max_pixels when fitness < 0

## GUI
- This tool implements a GUI for EPGACI to provide an easier experience a cleaner experience
- Alters how EPGACI is used to censor images

### Values modifiable from GUI:
- Number of individuals in population
- Number of generations to compute
- Goal % similarity
- Image to censor

### Changes to how EPGACI is used: 
- Now only censors a portion of the selected image based on the user's drawing boundaries of portion
- Does not technically save image (saved briefly to display with correct name and then is deleted)
- Image may be saved once displayed

#### Files/Folders in repository:
- images: stores default image when no image is selected
- EPGACI-tool.exe: executable version of EPGACI-tool.py
- EPGACI-tool.py: code that runs tool
- EPGACI.c: c file used in EPGACI
- EPGACI.py: code that runs EPGACI
- EPGACI.so: c library created from EPGACI.c
- EPGACI-noGUI.py: functionally this tool without its GUI 

When creating and using an executable version of this tool, make sure the executable stays in the same folder as the code
