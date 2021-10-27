from packages.generator.blum_blum_shub import BlumBlumShub
from packages.generator.solitaire import Solitaire
from packages.service.stream_cryptor import StreamCryptor

"""
print(BlumBlumShub(123).get(4))

stream1 = StreamCryptor(BlumBlumShub, 123)
stream2 = StreamCryptor(BlumBlumShub, 123)

cipherText1 = stream1.encryptTextOffset(b"Hello en Dani vagyok.", 3)
cipherText2 = stream1.encryptTextOffset(b"Hello en vagyok Dani.", 10)

print(cipherText1)
print(cipherText2)

planText1 = stream2.decryptTextOffset(cipherText2, 10)
planText2 = stream2.decryptTextOffset(cipherText1, 3)

print(planText1)
print(planText2)

#binary_text = [bin(ord(char)) for char in 'plainText']

#print(binary_text)

"""

deck = []

with open("deck.txt") as file:

    line = file.readline()

    if line[-1] == '\n':
        deck = line[:-1].split(' ')
    else:
        deck = line.split(' ')

deck = [int(i) for i in deck]

stream1 = StreamCryptor(Solitaire, deck)
stream2 = StreamCryptor(Solitaire, deck)

cipherText1 = stream1.encryptText(b"Hello en Dani vagyok.")
cipherText2 = stream1.encryptText(b"Hello en vagyok Dani.")

print(cipherText1)
print(cipherText2)

planText1 = stream2.decryptText(cipherText1)
planText2 = stream2.decryptText(cipherText2)

print(planText1)
print(planText2)




