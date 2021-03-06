class StreamCryptor:

    generator = None
    key = None
    offSet = 0

    def __init__(self, generator, key):
        self.generator = generator(key)
        self.key = key

    def encryptText(self, plainText):

        n = len(plainText)

        self.offSet = self.offSet + n

        random_binary = self.generator.get(n)

        binary_text = [(char) for char in plainText]

        cipherText = []

        for (rand, text) in zip(random_binary, binary_text):
            cipherText.append(rand ^ text)

        cipherText = bytes(cipherText)

        return cipherText

    def decryptText(self, cipherText):

        n = len(cipherText)

        self.offSet = self.offSet + n

        random_binary = self.generator.get(n)

        binary_text = [(char) for char in cipherText]

        plainText = []

        for (rand, text) in zip(random_binary, binary_text):
            plainText.append(rand ^ text)

        plainText = bytes(plainText)

        return plainText

    def encryptTextOffset(self, plainText, offset):

        n = len(plainText)

        self.offSet = offset + n

        random_binary = self.generator.getInterval(offset, offset + n)

        binary_text = [(char) for char in plainText]

        cipherText = []

        for (rand, text) in zip(random_binary, binary_text):
            cipherText.append(rand ^ text)

        cipherText = bytes(cipherText)

        return cipherText

    def decryptTextOffset(self, cipherText, offset):

        n = len(cipherText)

        self.offSet = offset + n

        random_binary = self.generator.getInterval(offset, offset + n)

        binary_text = [(char) for char in cipherText]

        plainText = []

        for (rand, text) in zip(random_binary, binary_text):
            plainText.append(rand ^ text)

        plainText = bytes(plainText)

        return plainText

    def getOffset(self):
        return self.offSet