import random as ran

def noise(bits, flip_count):
    """ Flip flip_count bits at random indexes. Do not flip the same bit twice. """
    ran_index = -1
    excludes = [ran_index]
    if len(bits) < flip_count:
        raise IndexError("Amount of errors is greater than the amount of bits.")
    for error in range(flip_count):
        while(ran_index in excludes):
            ran_index = ran.randint(0,len(bits)-1)
        excludes.append(ran_index)
    noisy_bits = []
    for i in range(len(bits)):
        if i in excludes:
            noisy_bits.append(flip_bit(bits[i]))
        else:
            noisy_bits.append(bits[i])
    return noisy_bits
            
def pad_bits(bits:list,multiple:int):
    """ Add padding to a vector of bits so that it's length is a multiple of multiple """
    pad_count = multiple - (len(bits) % multiple) # Find out padding necessary to make len(bits) a multiple of 4
    padded_bits = []
    for bit in bits:
        padded_bits.append(bit)
    if pad_count == multiple: pad_count = 0 # Already a multiple of 4
    for i in range(pad_count):
        padded_bits.append(0)
    return padded_bits
   

def encoder(bits:list)->list:
    """ Encode bits with [7,4] block encoding """
    encoded_bits = []
    assert(len(bits)%4==0) # bits must be a multiple of 4
    pad_count = 28 - (len(bits) % 28) # Find out padding necessary to make len(bits) a multiple of 4
    if pad_count == 28: pad_count = 0 # Already a multiple of 4
    for i in range(pad_count):
        bits.append(0)
    for i in range(0,len(bits),4):
        block = [[]]
        for j in range(4):
            block[0].append(bits[i+j])
        encoded_block = encode_block(block)
        for j in range(7):
            encoded_bits.append(encoded_block[0][j])
    return encoded_bits

def encode_block(block):
    """ Encode 4 bits """
    g = generate()
    return multiply_matrices(block,g)

def multiply_matrices(m1,m2):
    """ m1 x m2 """
    m1_rows = len(m1)
    m1_cols = len(m1[0])
    m2_rows = len(m2)
    m2_cols = len(m2[0])
    assert(m1_cols==m2_rows)
    product = []
    for p_row in range(m1_rows):
        product.append([])
        for p_col in range(m2_cols): 
            result = 0
            for m1_col in range(m1_cols):
                result += m1[p_row][m1_col]*m2[m1_col][p_col]
            result = result % 2
            product[p_row].append(result)
    return product
        


            


def generate():
    """ [7,4] Block Code """
    return [[1,0,0,0,   1,1,1],
            [0,1,0,0,   0,1,1],
            [0,0,1,0,   1,0,1],
            [0,0,0,1,   1,1,0]]

def s_matrix():
    """ Error correction matrix """
    return [[1,1,1],
            [0,1,1],
            [1,0,1],
            [1,1,0],
            [1,0,0],
            [0,1,0],
            [0,0,1]]

def decode_bits(bits):
    """ Decode the [7,4] block encoded bits. """
    decoded_bits = []
    for i in range(0,len(bits),7):
        r = []
        for j in range(7):
            r.append(bits[i+j])
        decoded_block = decode_block([r])
        for j in range(4):
            decoded_bits.append(decoded_block[j])
    return decoded_bits

def decode_block(block):
    """ Decode a block of the [7,4] block encoded bits. """
    s = s_matrix()
    new_m = multiply_matrices(block,s)
    i = 0
    look_up_row_index = -1
    for row in s:
        if row == new_m[0]:
            look_up_row_index = i
            break
        i+=1
    if look_up_row_index != -1:
        block[0][look_up_row_index] = flip_bit(block[0][look_up_row_index])
    return block[0][0:4]

def flip_bit(bit):
    """ See below """
    return 1 ^ bit
        
def text2bits(message):
    """ Convert text into bits. 7 bits per character. """
    return [int(bit) for char in message for bit in format(ord(char), '07b')]            

def bits2text(bits):
    """
    Convert a flat iterable of 0/1 to a 7-bit ASCII string (MSB first).
    Pure-Python, no NumPy required.
    """
    bits = list(bits)
    if len(bits) % 7 != 0:
        raise ValueError("Length of bit stream must be a multiple of 7.")

    out_chars = []
    for i in range(0, len(bits), 7):
        byte = 0
        # MSB first: positions 0..6 map to weights 64..1
        # converts the binary chunk into its integer value
        for b in bits[i:i+7]:
            byte = (byte << 1) | (1 if b else 0)
        out_chars.append(chr(byte))
    # Joins the list of characters into a single string
    rx_text = ''.join(out_chars)
    #print('Received Message:', rx_text)
    return rx_text

def encode_noise_decode(message_sent,noise_flips):
    """ Block encode a message then send it through a simulated noisy channel then decode the message. """
    bits = text2bits(message_sent)
    padded_bits = pad_bits(bits,4) # Pad the message so that it can be encoded in 4 bit blocks
    padding = len(padded_bits) - len(bits)
    encoded_bits = encoder(padded_bits)
    noisy_bits = noise(encoded_bits,noise_flips)
    decoded_bits = decode_bits(noisy_bits)
    striped_bits = decoded_bits[0:len(decoded_bits)+padding] # Remove padding
    message_received  = bits2text(striped_bits)
    # Count the number of errors in the received message
    errors = 0
    for i in range(len(bits)):
        if bits[i] != striped_bits[i]:
            errors+=1

    # Print results
    print("bit count:\t", str(len(bits)))
    print("padding:\t", str(padding))
    print("message_sent:\t\t" + message_sent + "|||")
    print("message_received:\t" + message_received + "|||")
    print("Flips from noise:\t",noise_flips)
    print("Errors after decoding:\t", errors)
    print("Flips in noise per bit:\t", str(noise_flips/len(bits)))
    print("Error per bit:\t", str(errors/len(bits)))



def test_mult_matrices():
    """ Test matrix multiplication """
    d = [[1,0,1,0]]
    g = generate()
    p = multiply_matrices(d,g)
    print(d)
    print(g)
    print(p)

def main():
    """ Run the program """
    encode_noise_decode("I really love dogs a whole lot!!!",20)
    

if __name__ == '__main__':
    main()