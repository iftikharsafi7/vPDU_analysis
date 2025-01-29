# vPDU_analysis
This repository is for analysis of the vPDUs

Instructions:
1. temp_logger.py: This script plots the temperature values from the 4 thermocouples. Inside the file, add the name of the text file and directory.
2. IV.py: This script plots the IV curves from the text files. It can plot the IV data for all tiles in each quadrant (meaning that each tile is ON one by one) and also it can plot the whole quadrant data (meaning that all tiles are ON). 
   To run this file use this command "python3 IV.py -I IV_data.csv -PS c" where the -PS is the power supply argument and c is the CAEN power supply.
3. reco_finger_plots.py: This script creates the finger plots from the reconstructed root files. Inside the file, it needs the input file. 
   
