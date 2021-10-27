from packages.generator.blum_blum_shub import BlumBlumShub
from packages.service.stream_cryptor import StreamCryptor

stream1 = StreamCryptor(BlumBlumShub, 123)
stream2 = StreamCryptor(BlumBlumShub, 123)

cipherText1 = stream1.encryptText(b"Hello en Dani vagyok.")
cipherText2 = stream1.encryptText(b"Hello en vagyok Dani.")

print(cipherText1)
print(cipherText2)

planText1 = stream2.decryptText(cipherText1)
planText2 = stream2.decryptText(cipherText2)

print(planText1)
print(planText2)

#binary_text = [bin(ord(char)) for char in 'plainText']

#print(binary_text)