from __main__ import Plugin
import requests

user_agent="archive plugin for /u/captainmeta4's IRC interface"

class Main(Plugin):

    def helptext(self):

        yield "$archive <url>"
        yield "Obtain the most recent archive of <url> if it exists, or begin archiving if it does not."

    def exe(self, message):

        url=self.args[1]

        #apis
        check='http://archive.org/wayback/available?url={}'
        save = 'https://web.archive.org/save/{}'
        headers={'User-Agent':user_agent}

        

        #check to see if it is already archived

        x=requests.get(check.format(url), headers=headers)
        j=x.json()
        if 'closest' in j['archived_snapshots']:
            yield j['archived_snapshots']['closest']['url']
            return

        #archive it

        x=requests.get(save.format(url), headers=headers)
        if x.status_code == 403:
            yield "Internet Wayback Machine does not archive that site."
            return
        elif x.status_code != 200:
            yield "There was an error archiving your url"
            return

        yield "Archive started. Try again in a minute or two to see if there's a saved archive page."

        

        
