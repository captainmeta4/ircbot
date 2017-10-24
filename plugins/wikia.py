rom __main__ import Plugin
import requests

class Main(Plugin):

    def on_start(self):

        self.api="http://{}.wikia.com/api/v1/Search/List/"
        self.headers={"User-Agent":"ircBot by /u/captainmeta4 for snoonet"}

    def helptext(self):

        yield "$wikia <site> <query>"
        yield "Search <site>.wikia.com for <query>, and return the first result"

    
    def exe(self, message):

        self.args=message.body.split(maxsplit=2)

        site=self.args[1]
        query=self.args[2]

        #set url and params
        url=self.api.format(site)
        params={'query':query,
            'limit':25,
            'lang':'en',
            'namespaces':'0'
            }

        x=requests.get(url, params=params, headers=self.headers)

        #check for non-200
        if x.status_code == 404:
            yield '{}.wikia.com has no articles matching "{}"'.format(site,query)
            return
        elif x.status_code != 200:
            yield 'There was an error searching wikia.com. Please try again later.'
            return

        #check for invalid community
        if 'http://community.wikia.com/wiki/Community_Central:Not_a_valid_community?' in x.url:
            yield '{}.wikia.com does not exist'.format(site)

        j=x.json()
        page=j['items'][0]

        output = '{}: {} - {}'.format(page['title'],page['url'],page['snippet'][0:50])
        yield output

        

        
        

        
