import random as ran
def noise(bits, errors):
    ran_index = -1
    excludes = [ran_index]
    if len(bits) < errors:
        assert(False)
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
            

        
def text2bits(message):
    return [int(bit) for char in message for bit in format(ord(char), '07b')]            


def main():
    message = "dogs"
    #noisy_bytes = noise(message,6)
    bits = text2bits(message)
    noisy_bits = noise(bits,5)
    print("bits:\t" + str(bits))
    print("n_bits:\t" + str(noisy_bits))
    #print(noisy_bytes)

if __name__ == '__main__':
    main()