from bs4 import BeautifulSoup as soup
from AllRecipes.Const import Const
from AllRecipes import ParseConnection
import re
import json

class ParseSiteMap(ParseConnection):

    def __init__(self):
        """
        initialize class object
        """
        self._secure_connection(Const.BASE_URL)
        self.__setup()

    def __call__(self):
        """
        override method to more clearly code
        :return (types. packages, links):
        :types : list which include types of every packages
        :packages : list which include name of every example by type
        :links : list which include link for every packages
        """
        self.__make_parse()
        return self.types, self.packages, self.links

    def __setup(self):
        """
        make __init__ more clearly, cut part of code from html file
        """
        self.types, self.packages, self.links = [], [], []
        self.page_soup = soup(self.page, "html.parser")
        self.__tr = self.page_soup.find('tr')
        self.__td = self.__tr.findAll('td')

    def __clear_types(self, span):
        """
        method for filtering unnecessary text
        :param span: list of spans
        :return: (types, spans)
        :types : text from filtered spans
        :spans : filtered spans
        """
        spans = list(span).copy()
        [spans.remove(tp) for tp in span if len(tp.get_text()) < 7]
        types = [tp.get_text() for tp in spans]
        return types, spans

    def __getattribute__(self, item):
        """
        override method for getting attributes
        :param item: item, which return
        :return: item
        """
        return object.__getattribute__(self, item)

    def __make_parse(self, debug=False):
        """
        method which take all data what we need, like:
            types of food packages
            names of food packages
            links of food packages
        from website -> www.allrecipes.com
        """
        where_looting = iter(self.__td)

        for i, td in enumerate(where_looting):
            _types, _spans = self.__clear_types(td.findAll('span'))
            self.types.extend(_types)

            html_part = str(td)
            counter = len(_types)

            for j in range(counter):

                start = html_part.find(str(_spans[j]))
                if j < counter - 1:
                    end = html_part.find(str(_spans[j + 1]))
                else:
                    end = -1

                soup_part = soup(html_part[start:end], "html.parser")
                _packages = [pkg.get_text() for pkg in soup_part.findAll('a')]
                _links = [pkg.get_attribute_list('href')[0] for pkg in soup_part.findAll('a')]

                self.packages.append(_packages)
                self.links.append(_links)
                if debug == True:
                    print(f'Count i, j -> {i + 1, j + 1}')
                    print('-' * 10)


class ParsePage(ParseConnection):
    def __init__(self, name_type, pack, url):
        """
        initialize class for parsing page
        :param name_type: string, type from package
        :param pack: list, name from package
        :param url: list, link from package
        """
        self.__type = name_type
        self.__pack = pack
        self.__url = url

    def __parse_name(self, page_soup):
        name = page_soup.find('h1', {'class': 'headline heading-content'}).get_text()
        return name

    def __parse_summary(self, page_soup):
        """
        extract summary from page
        :param page_soup: BeatifulSoup, where is searching
        :return: string, with string from page
        """
        text = page_soup.find('div', {'class': 'recipe-summary margin-8-bottom'}).get_text()
        return text

    def __parse_image(self, page_soup):
        image = page_soup.find('div', {'class': 'image-container'}).div.img['src']
        return image

    def __clear_string(self, string):
        """
        clear text from tag, like ' ', '\n' and other....
        :param string: str, what to clear
        :return: cleared string
        """
        clear = re.sub(r"^\s+|\s+$", "", string)
        return clear

    def __parse_meta_info(self, page_soup):
        """
        extract meta info from page
        :param page_soup: BeatifulSoup, where is searching
        :return: list, (header, body) with string from page
        """
        section = page_soup.find('section', {'class': 'recipe-meta-container two-subcol-content clearfix'})
        divs = section.findAll('div', {'class': 'recipe-meta-item'})
        meta_info = []
        for div in divs:
            header = div.find('div', {'class': 'recipe-meta-item-header'}).get_text()
            header = self.__clear_string(header)
            body = div.find('div', {'class': 'recipe-meta-item-body'}).get_text()
            body = self.__clear_string(body)
            meta_info.append((header, body))
        return meta_info

    def __parse_ingredients(self, page_soup):
        """
        extract ingredients from page
        :param page_soup: BeatifulSoup, where is searching
        :return: list, list with string from page
        """
        section = page_soup.find('ul', {'class': 'ingredients-section'})
        lis = section.findAll('li', {'class': 'ingredients-item'})
        ingredients = []
        for li in lis:
            text = li.find('span', {'class': 'ingredients-item-name'}).get_text()
            text = self.__clear_string(text)
            ingredients.append(text)
        return ingredients

    def __parse_direction(self, page_soup):
        """
        extract direction from page
        :param page_soup: BeatifulSoup, where is searching
        :return: list, list with string from page
        """
        section = page_soup.find('ul', {'class': 'instructions-section'})
        lis = section.findAll('li', {'class': 'subcontainer instructions-section-item'})
        directions = []
        for li in lis:
            text = li.find('p').get_text()
            text = self.__clear_string(text)
            directions.append(text)
        return directions

    def __parse_nutrition_facts(self, page_soup):
        """
        extract nutrition_facts from page
        :param page_soup: BeatifulSoup, where is searching
        :return: string, text from page
        """
        section = page_soup.find('section', {'class': 'nutrition-section container'})
        if section is None:
            return 'None'
        text = section.find('div', {'class': 'section-body'})
        [x.extract() for x in text.find('a')]
        text = text.get_text()
        text = self.__clear_string(text)
        return text

    def go_parse(self):
        """
        parsing page with recipe
        :return: dictionary with all info about recipe
        """
        self._secure_connection(self.__url)
        page_soup = soup(self.page, "html.parser")
        recipe_name = self.__parse_name(page_soup)
        recipe_summary = self.__parse_summary(page_soup)
        preview_image = self.__parse_image(page_soup)
        meta_recipe = self.__parse_meta_info(page_soup)
        ingredients = self.__parse_ingredients(page_soup)
        direction = self.__parse_direction(page_soup)
        nutrition_facts = self.__parse_nutrition_facts(page_soup)
        values = [
            self.__type, self.__pack, self.__url, recipe_name,
            recipe_summary, preview_image, meta_recipe,
            ingredients, direction, nutrition_facts,
        ]
        keys = [
            'type', 'package', 'link', 'name',
            'summary', 'image', 'meta',
            'ingredients', 'direction', 'facts',
        ]
        return dict(zip(keys, values))


class Recipe(ParseConnection):

    def __init__(self, by_type, by_packages, links):
        """
        class for parse by special links
        :param by_type: group names of packages
        :param by_packages: package name
        :param links: package links
        """
        self.__type = by_type
        self.__pk_names = by_packages
        self.__pk_links = links

    def __parse_packages_page(self, url):
        """
        method for parcing links from page
        :param url: string, where is searching
        :return: list, list with urls
        """
        self._secure_connection(url)
        page_soup = soup(self.page, "html.parser")
        script = page_soup.find('script', {'type': 'application/ld+json'})
        string = str(script)
        pattern = 'http[s]?://www.allrecipes.com/recipe/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(pattern, string[script.contents[0].find('url'):])
        return urls

    def save_data(self, to_save, file_name):
        """
        method to write all data to json file
        :param to_save: dict with another dict(include recipe's info)
        """
        print(f'Saving to file -> {file_name}.json')
        with open(f'Data/{file_name}.json', 'w') as file:
            json.dump(to_save, file)


    def get_recipes(self, save=True):
        """
        get dict  where every item is another dictionary with recipe from every delicious
        or save to json file
        :return: list, include dictionary's
        """
        all_data = []
        link_iter = iter(self.__pk_links)
        pack_iter = iter(self.__pk_names)
        for i, (url, pack) in enumerate(zip(link_iter, pack_iter)):
            pack_data = []
            pack = '_'.join(re.findall(r'\w+', pack.lower()))
            # parse links to food recipes from page
            links_to_recipes = iter(self.__parse_packages_page(url))
            # end
            for j, link in enumerate(links_to_recipes):
                print(f'Start iteration -> {i, j}')
                parse_page = ParsePage(self.__type, pack, link)

                dict_with_data = parse_page.go_parse()
                pack_data.append(dict_with_data)

            if save:
                self.save_data(pack_data, f'{pack}')

        return all_data
