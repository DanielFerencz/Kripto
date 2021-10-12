#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Ferencz Daniel
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import utils

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """

    if(len(plaintext)<1):
        print('plaintext length is not greater than 0')
        raise ValueError
    
    if(not plaintext.isupper()):
        print('plaintext is not in uppercase')
        raise ValueError

    ciphertext = ""

    for char in plaintext:
        if (ord(char)>=ord('A') and ord(char)<=ord('Z')):
            cipherchar = ord(char) + 3
            if cipherchar > ord('Z'):
                cipherchar = cipherchar - ord('Z') + ord('A') - 1
            ciphertext += chr(cipherchar)
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    if(len(ciphertext)<1):
        print('ciphertext length is not greater than 0')
        raise ValueError
    
    if(not ciphertext.isupper()):
        print('ciphertext is not in uppercase')
        raise ValueError

    plaintext = ""

    for char in ciphertext:
        if (ord(char)>=ord('A') and ord(char)<=ord('Z')):
            plainchar = ord(char) - 3
            if plainchar < ord('A'):
                plainchar = plainchar + ord('Z') - ord('A') + 1
            plaintext += chr(plainchar)
        else:
            plaintext += char
    
    return plaintext


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    if(len(plaintext)<1):
        print('plaintext length is not greater than 0')
        raise ValueError
    
    if(not plaintext.isupper()):
        print('plaintext is not in uppercase')
        raise ValueError

    if(len(keyword)<1):
        print('keyword length is not greater than 0')
        raise ValueError
    
    if(not keyword.isupper()):
        print('keyword is not in uppercase')
        raise ValueError

    for char in keyword:
        if(ord(char)<ord('A') or ord(char)>ord('Z')):
            print('keyword contains non-alphabetic charaters')
            raise ValueError

    ciphertext = ""
    length = 0

    for char in plaintext:

        if(ord(char)<ord('A') or ord(char)>ord('Z')):
            print('plaintext contains non-alphabetic charaters')
            raise ValueError

        rot = ord(keyword[length])-ord('A')

        length += 1

        if (length == len(keyword)):
            length = 0

        cipherchar = ord(char) + rot
        if cipherchar > ord('Z'):
            cipherchar = cipherchar - ord('Z') + ord('A') - 1
        ciphertext += chr(cipherchar)
    
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    if(len(ciphertext)<1):
        print('ciphertext length is not greater than 0')
        raise ValueError
    
    if(not ciphertext.isupper()):
        print('ciphertext is not in uppercase')
        raise ValueError

    if(len(keyword)<1):
        print('keyword length is not greater than 0')
        raise ValueError
    
    if(not keyword.isupper()):
        print('keyword is not in uppercase')
        raise ValueError

    for char in keyword:
        if(ord(char)<ord('A') or ord(char)>ord('Z')):
            print('keyword contains non-alphabetic charaters')
            raise ValueError

    plaintext = ""
    length = 0

    for char in ciphertext:

        if(ord(char)<ord('A') or ord(char)>ord('Z')):
            print('plaintext contains non-alphabetic charaters')
            raise ValueError
        
        rot = ord(keyword[length])-ord('A')

        length += 1

        if (length == len(keyword)):
            length = 0

        plainchar = ord(char) - rot
        if plainchar < ord('A'):
            plainchar = plainchar + ord('Z') - ord('A') + 1
        plaintext += chr(plainchar)
    
    return plaintext

def encrypt_scytale(plaintext, circumference, binary):


    if(len(plaintext)<1):
        print('plaintext length is not greater than 0')
        raise ValueError
    
    if(circumference<1):
        print('circumference is not greater than 0')
        raise ValueError

    if binary:
        cipherlist = []

        ratio = len(plaintext) // circumference
        
        for i in range(circumference):
            cipherlist += [plaintext[ind*circumference+i] for ind in range(ratio) if ind*circumference+i<len(plaintext)]

        ciphertext = bytes(cipherlist)

        return ciphertext

    ciphertext = ""

    ratio = len(plaintext) // circumference
    
    for i in range(circumference):
        ciphertext += "".join([plaintext[ind*circumference+i] for ind in range(ratio) if ind*circumference+i<len(plaintext)])

    return ciphertext

def decrypt_scytale(ciphertext, circumference, binary):

    if(len(ciphertext)<1):
        print('ciphertext length is not greater than 0')
        raise ValueError
    
    if(circumference<1):
        print('circumference is not greater than 0')
        raise ValueError

    if binary:
        plainlist = []

        ratio = len(ciphertext) // circumference
        
        for i in range(circumference):
            plainlist += [ciphertext[ind*circumference+i] for ind in range(ratio) if ind*circumference+i<len(ciphertext)]

        plaintext = bytes(plainlist)

        return plaintext

    plaintext = ""

    ratio = len(ciphertext) // circumference
    
    for ind in range(ratio):
        plaintext += "".join([ciphertext[i*ratio+ind] for i in range(circumference) if i*ratio+ind<len(ciphertext)])

    return plaintext

def merge(text1, text2):
    
    merged = ""

    for i in range(len(text1)):
        if(i < len(text2)):
            merged += "".join([text1[i],text2[i]])
        else:
            merged += "".join([text1[i]])
    
    return merged

def demerge(text):
    
    text1 = ""
    text2 = ""

    for i in range(len(text)):
        if(i % 2 == 0):
            text1 += "".join([text[i]])
        else:
            text2 += "".join([text[i]])
    
    return text1,text2

def encrypt_railfence(plaintext, num_rails):

    if(len(plaintext)<1):
        print('plaintext length is not greater than 0')
        raise ValueError
    
    if(num_rails<1):
        print('num_rails is not greater than 0')
        raise ValueError

    ciphertext = ""

    if (num_rails == 1):
        return plaintext

    gap = num_rails*2-2

    ciphertext += "".join(plaintext[slice(0,len(plaintext),gap)])

    for i in range(1,num_rails-1):

        text1 = plaintext[slice(i,len(plaintext),gap)]
        text2 = plaintext[slice(gap-i,len(plaintext),gap)]

        ciphertext += merge(text1,text2)

    ciphertext += "".join(plaintext[slice(num_rails-1,len(plaintext),gap)])

    return ciphertext

def decrypt_railfence(ciphertext, num_rails):

    if(len(ciphertext)<1):
        print('ciphertext length is not greater than 0')
        raise ValueError
    
    if(num_rails<1):
        print('num_rails is not greater than 0')
        raise ValueError

    plainlist = [char for char in ciphertext]

    if (num_rails == 1):
        return ciphertext

    gap = num_rails*2-2

    slc = slice(0,len(ciphertext),gap)
    length = len(ciphertext[slc])
    plainlist[slc] = [ciphertext[i] for i in range(length)]

    for i in range(1,num_rails-1):
        slc1 = slice(i,len(ciphertext),gap)
        length1 = len(ciphertext[slc1])
        slc2 = slice(gap-i,len(ciphertext),gap)
        length2 = len(ciphertext[slc2])

        text1, text2 = demerge(ciphertext[length:length+length1+length2])

        length += length1+length2

        plainlist[slc1] = [char for char in text1]
        plainlist[slc2] = [char for char in text2]

    slc = slice(num_rails-1,len(ciphertext),gap)
    plainlist[slc] = [char for char in ciphertext[length:]]

    return "".join(plainlist)

def decrypt_int_vigenere(ciphertext, possible_keys):

    if(len(ciphertext)<1):
        print('ciphertext length is not greater than 0')
        raise ValueError
    
    if(len(possible_keys)<1):
        print('possible_keys length is not greater than 0')
        raise ValueError

    allWords = []

    ciphertext = ciphertext.lower()

    with open('words.txt') as f:
        for line in f:
            allWords.append(line.strip())

    punctuation = [":","-",".",",","'","/","!","?",";",")","("]
    
    for keyword in possible_keys:
        
        plaintext = ""
        length = 0

        for char in ciphertext:

            if(ord(char)>=ord('a') and ord(char)<=ord('z')):
            
                rot = ord(keyword[length])-ord('a')

                length += 1

                if (length == len(keyword)):
                    length = 0

                plainchar = ord(char) - rot
                if plainchar < ord('a'):
                    plainchar = plainchar + ord('z') - ord('a') + 1
                plaintext += chr(plainchar)
            
            else:
                plaintext += char

        wordList = plaintext.split()

        wordList = list(filter(lambda x: x not in punctuation, wordList))

        ok = True

        for word in wordList:
            if word not in allWords:
                ok = False
                break
        
        if ok == True:
            return plaintext

    return ciphertext


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here

    


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

