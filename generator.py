import random

class Generator:
    def __init__(self, characters, model):
        """makes a generator. Requires characters, a list of characters, and model, a function 
        that assigns a probability to each character given a preceding context
        """
        self.model = model
        self.characters = characters

      
    def generate(self):

        word = ['<START>']

        while word[-1] != '<STOP>':
            probs = [self.model(char, word) for char in self.characters]
            choice = random.choices(self.characters, weights = probs)

            word = word + choice


        return self.niceString(word)

    def niceString(self, charlist):
        #make a nice string out of a character list

        nicelist = charlist[1:-1] #remove start en stop tokens
        #nicelist = nice[0].upper() + nice[1:] #uppercase first character
        return ''.join(nicelist)

    def printSample(self, N):
        for _ in range(N):
            print(self.generate())
