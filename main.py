import struct

def ibm_to_float(ibm, precision):
    ibm = str(ibm) # just to make sure its a string
    sign = ibm[:1]

    #assuming these will be either binary or hex, so check for binary first
    is_binary = all(c in '01' for c in ibm)
    

    
    if is_binary is False:
        number =   ibm[2:]
        
    else:
        number =    int(ibm[1:], 2)
        number =    str(hex(number))[2:]
    
    # the part after x is the exponent and fraction
    
    exponent = int(number[:2], 16) - 64
    
    fraction = '0'+str(number[2:])
    
    fracFloat = 0.0
    n = 0
    for i in fraction:
        fracFloat = fracFloat+ float(int(i,16))*16**n
        n = n-1
        
    result = fracFloat*16**exponent

    if sign == '1':
        result = result*-1
        


    bits, = struct.unpack('!I', struct.pack('!f', result))
    if precision == "double":
        ieee = "{:064b}".format(bits)
    elif precision == "single":
        ieee = "{:032b}".format(bits)
        
    return ieee




# Prompt the user for conversion type
input_precision = input("Enter precision for input ('single' or 'double'):")

# Prompt the user for conversion type
precision = input("Enter precision for output ('single' or 'double'):")

# Prompt the user for input filename
input_filename = input("Enter input filename: ")

# Prompt the user for output filename
output_filename = input("Enter output filename: ")

try:
    # Open the input and output files
    with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
        # Process each line in the input file
        if input_precision == "double":
            chunk_size = 8
        elif input_precision == "single":
            chunk_size = 4
        while True:
            line = input_file.read(chunk_size)
            line = line.hex()
            if not line:  # If the chunk is empty, we've reached the end of the file
                break
            
            # Convert the line
            if input_precision == "double":
                converted_line = ibm_to_float(format(int(line, 16), '064b'), precision)
            elif input_precision == "single":
                converted_line = ibm_to_float(format(int(line, 16), '032b'), precision)
            output = hex(int(converted_line,2))
            print(str(line)+" --> "+str(output))

            
            
            # Write the converted line to the output file
            output_file.write(bytes.fromhex(str(output)[2:]))

    print("Conversion complete. Output written to", output_filename)
except FileNotFoundError:
    print("File not found. Please make sure the input file exists.")

