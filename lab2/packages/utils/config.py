from packages.generator.solitaire import Solitaire
from packages.generator.blum_blum_shub import BlumBlumShub

class Config:

    key = None
    generator = None

    def __init__(self):
        
        deck = []

        with open("packages/utils/deck.txt") as file:

            line = file.readline()

            if line[-1] == '\n':
                deck = line[:-1].split(' ')
            else:
                deck = line.split(' ')

        self.key = [int(i) for i in deck]
        self.generator = Solitaire

        """
        number = 0

        with open("packages/utils/number.txt") as file:

            line = file.readline()

            if line[-1] == '\n':
                number = line[:-1]
            else:
                number = line

        self.key = int(number)
        self.generator = BlumBlumShub
        """
        

    def getGenerator(self):
        return self.generator

    def getKey(self):
        return self.key