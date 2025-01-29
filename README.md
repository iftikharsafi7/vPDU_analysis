# vPDU_analysis
This repository is for analysis of the vPDUs

Instructions:
1. temp_logger.py: This script plots the temperature values from the 4 thermocouples. Inside the file, add the name of the text file and directory.
2. IV.py: This script plots the IV curves from the text files. It can plot the IV data for all tiles in each quadrant (meaning that each tile is ON one by one) and also it can plot the whole quadrant data (meaning that all tiles are ON). 
   To run this file use this command "python3 IV.py -I IV_data.csv -PS c" where the -PS is the power supply argument and c is the CAEN power supply.
3. reco_finger_plots.py: This script creates the finger plots from the reconstructed root files. Inside the file, add the name of the text file and directory. I will plot the finger plots for each tile.
   
vPDU data files are available on the chuck server at CAMK
/work/chuck/iftikhar/vpdu_files/



For the passport analysis from the repository "https://gitlab.in2p3.fr/darkside/veto_passport/-/tree/vPDUdev" here are the instructions.
1. Noise analysis for the vPDUs for each tile. This is done both at warm and cold temperatures.  
   python3.12 pyreco/exe/fft2.py -i run00310.mid.lz4 -o fft_run00310
2. Reconstruction of root files from the mid.lz4 files. It will create a root file as an output. Use the below command.  
   python3.12 -m vPDUreco -i input_file_directory -c napoli.ini -o reconstructed_root_file
3. Passport analysis is used to calculate the signal-to-noise ratio, Dark count rate, Direct crosstalk, 1 PE amplitude.  
   python3.12 -m vPDUFingerAnalysis.py  -I input_file_directory -P False -B 69 -T c -C q  
   The arguments are:  
   
    parser.add_argument("-I","--InputReco",help ="Directory/to/data/for/spe")  
    parser.add_argument("-P","--plot",help = "Plot = True or False")  
    parser.add_argument("-B","--bias",help = "Bias voltage (V)")  
    parser.add_argument("-T","--temp",help= "Warm(w) or Cold Test(c)")  
    parser.add_argument("-C","--channel",help="q or t")  
    parser.add_argument("-S", "--ini_file", help="Path to .ini file")  
    parser.add_argument("-R", "--reading", help="Which channels to read in")  
    parser.add_argument("-V", "--IV", help="IV curve path")  
    parser.add_argument("-N", "--Name", help="Output csv names")  
   
