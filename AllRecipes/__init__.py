import urllib.request as req
from AllRecipes.Const import Const

class ParseConnection:

    def _secure_connection(self, url):
        """
        opening up connection, grabbing the page and closing connection for safety
        take data from website -> www.allrecipes.com
        """
        client = req.urlopen(url)
        self.page = client.read()
        self.code = client.code
        client.close()
