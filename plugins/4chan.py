from __main__ import Plugin
import requests

class Main(Plugin):

    def on_start(self):

        self.api='https://a.4cdn.org/{}/catalog.json'
        self.headers = {"User-Agent":"snoonet ircbot by anon"}
        self.reply_url='http://boards.4chan.org/{}/thread/{}'
        self.reply = "{} - {}"

        

        #load list of boards
        self.boards=[]
        for board in requests.get('https://a.4cdn.org/boards.json',headers=self.headers).json()['boards']:
            self.boards.append(board['board'])

    def helptext(self):

        yield "$4chan <board>"
        yield "Retrieves the top 3 non-sticky post from /<board>/. Results may be NSFW"

    def exe(self, message):

        board = self.args[1]

        if board not in self.boards:
            yield "/{}/ does not exist".format(board)
            return

        #get top posts

        x=requests.get(self.api.format(board), headers=self.headers)
        data=x.json()

        i=0
        for thread in data[0]['threads']:
            #ignore stickies
            if 'sticky' in thread:
                continue

            subject=thread.get('sub','[no subject]')
            number=thread['no']

            response_url = self.reply_url.format(board,number)

            reply = self.reply.format(response_url, subject)

            yield reply
            i+=1
            if i>=3:
                break
            
        return

            
            

        
