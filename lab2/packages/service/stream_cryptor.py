class StreamCryptor:

    generator = None
    key = None
    index = 0

    def __init__(self, generator, key):
        self.generator = generator(key)
        self.key = key

    def encryptText(self, plainText):

        n = len(plainText)

        random_binary = self.generator.get(n)

        binary_text = [(char) for char in plainText]

        cipherText = []

        for (rand, text) in zip(random_binary, binary_text):
            cipherText.append(rand ^ text)

        cipherText = bytes(cipherText)

        return cipherText

    def decryptText(self, cipherText):

        n = len(cipherText)

        random_binary = self.generator.get(n)

        binary_text = [(char) for char in cipherText]

        plainText = []

        for (rand, text) in zip(random_binary, binary_text):
            plainText.append(rand ^ text)

        plainText = bytes(plainText)

        return plainText