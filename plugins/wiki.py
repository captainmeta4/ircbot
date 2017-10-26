from __main__ import Plugin
import requests

class Main(Plugin):

    def helptext(self):

        yield "$wiki <query>"
        yield "Search en.wikipedia.org for <query> and return the top result"

    def on_start(self):

        self.api = 'https://en.wikipedia.org/w/api.php'
        self.headers = {"User-Agent": "ircbot by /u/captainmeta4. Contact at reddit.com/u/captainmeta4 (reddit account required)"}

    def exe(self, message):

        query = message.body.split(maxsplit=1)[1]

        params={'action':'opensearch',
                'list':'search',
                'search':query,
                'format':'json'}

        x = requests.get(self.api, params=params, headers=self.headers)

        data = x.json()
        #check for no results found
        if len(data[1]) == 0:
            yield 'No results found for "{}" on wikipedia'.format(query)
            return
        
        result = data[1][0]
        text = data[2][0][0:100]



        yield "https://en.wikipedia.org/wiki/{} - {}".format(result, text)



        
