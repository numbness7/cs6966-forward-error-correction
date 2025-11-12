import random as ran
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
            noisy_bits.append(1^bits[i])
        else:
            noisy_bits.append(bits[i])
    return noisy_bits
            
def encoder(bits):
    """ TODO: add forward error detection block encoding to bits."""
    return bits

def decoder(bits):
    """ TODO: add forward error detection block decoding to bits."""
    return bits
        
def text2bits(message):
    return [int(bit) for char in message for bit in format(ord(char), '07b')]            


def main():
    message = "dogs"
    #noisy_bytes = noise(message,6)
    bits = text2bits(message)
    encoded_bits = encoder(bits)
    noisy_bits = noise(bits,6)
    decoded_bits = decoder(noisy_bits)
    print("bits:\t" + str(bits))
    print("n_bits:\t" + str(noisy_bits))
    print("d_bits:\t" + str(decoded_bits))
    print("e_bits:\t" + str(encoded_bits))
    #print(noisy_bytes)

if __name__ == '__main__':
    main()