from AllRecipes.parse import *
from AllRecipes.save import *

class QuickParse:
    def __init__(self):
        self.parse = ParseSiteMap()
        self.saver = Save_db()
        self.types, self.packages, self.links = self.parse()
        self.__cleaning()

    def __cleaning(self):
        for i in range(7):
            _pack, _link = [], []
            for j, elem in enumerate(self.packages[i]):
                pack = ' '.join(re.findall(r'\w+', elem))
                if len(pack) > 0:
                    _pack.append(pack)
                    _link.append(self.links[i][j])
            self.packages[i] = _pack
            self.links[i] = _link

    def parsing(self):
        for i in range(7):
            print(f'Type which parsing is {self.types[i]}')
            data_extractor = Recipe(
                self.types[i], self.packages[i], self.links[i]
            )
            data_extractor.get_recipes(save=True)
            print('-' * 30)

    def save(self):
        self.saver.save_to_db()

    def __del__(self):
        del self.saver
