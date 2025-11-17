import unireedsolomon as rs
import random
import os

def add_byte_errors(data: bytes, error_count: int) -> bytes:
    """
    Corrupts 'error_count' random bytes in the byte string.
    
    This is different from your 'noise' function, which flips bits.
    This function corrupts entire bytes, which is what Reed-Solomon
    is designed to correct.
    """
    if error_count == 0:
        return data
        
    # Ensure we don't try to corrupt more bytes than we have
    if error_count > len(data):
        raise ValueError("Error count cannot be greater than data length")

    # Pick unique random indexes to corrupt
    error_indices = random.sample(range(len(data)), error_count)
    
    # Convert to a mutable bytearray to apply errors
    mutable_data = bytearray(data, 'latin-1')
    
    for index in error_indices:
        original_byte = mutable_data[index]
        # Flip all bits in the byte (a simple way to guarantee corruption)
        # You could also use (original_byte + random.randint(1, 255)) % 256
        corrupted_byte = original_byte ^ 0xFF 
        mutable_data[index] = corrupted_byte
        
    print(f"   -> Introduced {error_count} byte errors at indices: {error_indices}")
    
    # Return immutable bytes
    return bytes(mutable_data).decode('latin-1')

def main():
    """
    Run the encode-noise-decode process using Reed-Solomon.
    """
    
    # --- 1. Setup the Codec ---
    
    # We will use a RS(255, 223) code.
    # This is a very common standard that works on GF(2^8), or bytes.
    # n = 255: Total bytes in a full codeword (message + parity)
    # k = 223: Bytes in the original message
    #
    # This means the codec will add (n - k) = 32 parity bytes.
    # It can correct (n - k) / 2 = 16 corrupted bytes (symbols) anywhere
    # in the 255-byte block.
    
    n = 255
    k = 223
    ecc_symbols = n - k # 32
    
    try:
        coder = rs.RSCoder(n, k)
    except Exception as e:
        print(f"Error initializing RSCoder: {e}")
        print("Please ensure 'unireedsolomon' is installed: pip install unireedsolomon")
        return

    print(f"Using Reed-Solomon RS({n}, {k}) Codec")
    print(f"Can correct up to {ecc_symbols // 2} byte errors per block.\n")

    # --- 2. Define the Message ---
    
    # We'll use your message.
    message_sent = "I really love dogs a whole lot!!!"
    
    # Reed-Solomon works on bytes. We must encode the string.
    # The message must be exactly 'k' (223) bytes long for this
    # simple implementation. We'll pad it with null bytes.
    message_bytes = message_sent.encode('utf-8')
    
    if len(message_bytes) > k:
        print(f"Message is too long ({len(message_bytes)} bytes) for k={k}. Truncating.")
        message_bytes = message_bytes[:k]
    else:
        # Pad with null bytes ('\x00')
        padding = k - len(message_bytes)
        message_bytes = message_bytes + (b'\x00' * padding)
        
    print(f"Original message: '{message_sent}'")
    print(f"Padded message size: {len(message_bytes)} bytes (k={k})")

    # --- 3. Encode the Message ---
    
    print("\n--- Encoding ---")
    try:
        encoded_message = coder.encode(message_bytes)
        print(f"Encoded message size: {len(encoded_message)} bytes (n={n})")
    except Exception as e:
        print(f"Error during encoding: {e}")
        return

    # --- 4. Add Noise ---
    
    noise_flips = 10 # Let's add 10 *byte* errors
    print(f"\n--- Adding Noise ({noise_flips} errors) ---")
    
    noisy_message = add_byte_errors(encoded_message, noise_flips)

    # --- 5. Decode the Message ---
    
    print("\n--- Decoding ---")
    try:
        # The decode function automatically finds and corrects errors
        decoded_bytes = coder.decode(noisy_message)[0]
        print("Decoding successful.")
        
        # The library returns the k-length message.
        # We need to strip the null-byte padding we added.
        message_received = decoded_bytes.rstrip('\x00')
        
    except Exception as e:
        # This will happen if there are > 16 errors
        print(f"*** DECODING FAILED ***: {e}")
        message_received = "--- CORRUPTED ---"

    # --- 6. Print Results ---
    
    print("\n--- Results ---")
    print(f"Message Sent:\t\t{message_sent}|||")
    print(f"Message Received:\t{message_received}|||")
    
    if message_sent == message_received:
        print(f"\nSUCCESS: The message was perfectly recovered despite {noise_flips} byte errors.")
    else:
        print("\nFAILURE: The message could not be recovered.")
        print(f"(This is expected if errors > {ecc_symbols // 2})")

if __name__ == '__main__':
    main()