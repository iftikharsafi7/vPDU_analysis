#Running passport on multiple reconstructed files
# Define the run numbers in an array
file_numbers=(419 448 449 450 451 452 453 454)

# Loop over each run number
for number in "${file_numbers[@]}"
do
    # Define the input file based on the run number
    input_file="/directory_of_the_root_file/run${number}.root"

    # Automatically pass the run number as the QR code or name
    qr_code="run${number}"

    # Call Python script with the necessary arguments
    python3.12 -m vPDUFingerAnalysis -I "$input_file" -P True -B 66.4 -T c -C q --Name "$qr_code"

done
