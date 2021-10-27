class BlumBlumShub():

    p = 7043
    q = 4271
    seed = 0
    N = 0
    index = 0
    next = 0

    def __init__(self, seed):
        self.seed = seed
        self.N = self.p * self.q
        self.next = (seed ** 2) % self.N
    
    def get(self,n):

        if(n < 0):
            return []

        randList = []

        for i in range(n):
            oneByte = []
            for j in range(8):
                oneByte.append(self.next%2)
                self.next = (self.next ** 2) % self.N
                self.index = self.index + 1
            
            randList.append(int(''.join(map(str,oneByte)),2))
        
        return randList

    def getInterval(self, i, j):

        if (j < i):
            return []

        if (i < 0):
            return []

        randList = []
        next = (self.seed ** 2) % self.N

        for i in range(i):
            for j in range(8):
                next = (next ** 2) % self.N
        
        for i in range(i,j):
            oneByte = []
            for j in range(8):
                oneByte.append(next%2)
                next = (next ** 2) % self.N

            randList.append(int(''.join(map(str,oneByte)),2))

        return randList

    def goTo(self, n):

        if(n < 0):
            return

        self.index = 0
        self.next = (self.seed ** 2) % self.N

        for i in range(n-1):
            for j in range(8):
                self.next = (self.next ** 2) % self.N
                self.index = self.index + 1

        return