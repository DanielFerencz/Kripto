from packages.generator.blum_blum_shub import BlumBlumShub
from packages.service.stream_cryptor import StreamCryptor

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