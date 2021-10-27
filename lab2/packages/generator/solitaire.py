class Solitaire:

    initialDeck = []
    deck = []
    A = 0
    B = 0

    def __init__(self, deck) -> None:
        self.initialDeck = deck.copy()
        self.deck = deck.copy()

        self.A = deck.index(53)
        self.B = deck.index(54)

    def _moveDown(self):

        self.deck.pop(self.A)
        if(self.A < 53):
            self.deck.insert(self.A + 1, 53)
            self.A = self.A + 1
        else:
            self.deck.insert((self.A + 2) % 54, 53)
            self.A = (self.A + 2) % 54

        self.deck.pop(self.B)
        if(self.B < 52):
            self.deck.insert(self.B + 2, 54)
            self.B = self.B + 2
        else:
            self.deck.insert((self.B + 3) % 54, 54)
            self.B = (self.B + 3) % 54

    def _swap(self):

        first = min(self.A, self.B)
        last = max(self.A, self.B)

        self.deck = self.deck[last+1:] + self.deck[first:last+1] + self.deck[:first]

        self.A = self.deck.index(53)
        self.B = self.deck.index(54)

    def _countCut(self):

        count = self.deck[-1]

        if(count < 53):
            self.deck = self.deck[count+1:-1] + self.deck[:count+1] + self.deck[-1:]
            self.A = self.deck.index(53)
            self.B = self.deck.index(54)

    def _getFromTop(self):

        count = self.deck[0]

        if (count < 53):
            return self.deck[count+1]
        else:
            return -1

    def get(self, n):

        if(n < 0):
            return []

        randList = []

        for i in range(n):
            oneByte = []
            j = 0
            while j<8:
                self._moveDown()
                self._swap()
                self._countCut()
                card = self._getFromTop()

                if card != -1:
                    oneByte.append(card%2)
                    j = j + 1
            
            randList.append(int(''.join(map(str,oneByte)),2))
        
        return bytes(randList)


    def getInterval(self, i, j):

        if (j < i):
            return []

        if (i < 0):
            return []

        randList = []
        
        self.deck = self.initialDeck.copy()
        self.A = self.deck.index(53)
        self.B = self.deck.index(54)

        for x in range(i):
            y = 0
            while y<8:
                self._moveDown()
                self._swap()
                self._countCut()
                card = self._getFromTop()

                if card != -1:
                    y = y + 1
        
        for x in range(i,j):
            oneByte = []
            y = 0
            while y<8:
                self._moveDown()
                self._swap()
                self._countCut()
                card = self._getFromTop()

                if card != -1:
                    oneByte.append(card%2)
                    y = y + 1

            randList.append(int(''.join(map(str,oneByte)),2))

        return bytes(randList)