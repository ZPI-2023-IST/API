from game.Freecell import FreeCell
from translator.freecell_translator.freecell_translator import FreecellTranslator

class Runner:
    def __init__(self):
        self.game = FreeCell(seed=0)
        self.translator = FreecellTranslator(self.game)
        
    def reset(self):
        print("Resetting game")
        self.game = FreeCell(seed=0)
        self.translator = FreecellTranslator(self.game)
        
