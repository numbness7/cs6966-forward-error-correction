import random as ran
import numpy as np
def noise(bits, errors):
    ran_index = -1
    excludes = [ran_index]
    if len(bits) < errors:
        raise IndexError("Amount of errors is greater than the amount of bits.")
    for error in range(errors):
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
            
def encoder(bits):
    """ TODO: add forward error detection block encoding to bits."""
    encoded_bits = []
    for i in range(0,len(bits),4):
        block = [[]]
        for j in range(4):
            block[0].append(bits[i+j])
        encoded_block = encode_block(block)
        for j in range(7):
            encoded_bits.append(encoded_block[0][j])
    return encoded_bits

def encode_block(block):
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
    return [[1,1,1],
            [0,1,1],
            [1,0,1],
            [1,1,0],
            [1,0,0],
            [0,1,0],
            [0,0,1]]

def decode_bits(bits):
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
    """ TODO: add forward error detection block decoding to bits."""
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
    return 1 ^ bit
        
def text2bits(message):
    return [int(bit) for char in message for bit in format(ord(char), '07b')]            

def encode_noise_decode():
    message = "dogs"
    #noisy_bytes = noise(message,6)
    bits = text2bits(message)
    encoded_bits = encoder(bits)
    noisy_bits = noise(encoded_bits,6)
    decoded_bits = decode_bits(noisy_bits)
    print("bits:\t" + str(bits))
    print("d_bits:\t" + str(decoded_bits))
    print("e_bits:\t" + str(encoded_bits))
    print("n_bits:\t" + str(noisy_bits))

def test_mult_matrices():
    d = [[1,0,1,0]]
    g = generate()
    p = multiply_matrices(d,g)
    print(d)
    print(g)
    print(p)

def main():
    encode_noise_decode()
    

if __name__ == '__main__':
    main()