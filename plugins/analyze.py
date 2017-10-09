from __main__ import Plugin
import re
import requests
import os

class Main(Plugin):

    def on_start(self):

        self.key=os.environ.get('pastebin_api_dev_key')
        self.headers={'User-Agent': "captainmeta4 irc interface"}

    def helptext(self):

        yield "$analyze <redditor>"
        yield "See what domains /u/<redditor> links to the most within comments."

    def exe(self, message):

        #find the redditor
        account=self.r.redditor(self.args[1])

        try:
            x=next(account.new())
        except:
            yield "Can't find the account /u/"+self.args[1]
            return

        stats={}
        i=0

        #examine content for links
        for thing in account.overview(limit=100):

            #figure out where to look for links

            text=getattr(thing, 'body', getattr(thing, 'selftext', getattr(thing, 'url', None)))

            #find links
            links=re.findall('https?://([\w.-]+)', text)

            for link in links:

                #consolidate for readibility and better stats
                if link.startswith('www.'):
                    link=link.lstrip('w.')

                #add to stats
                if link in stats:
                    stats[link]+=1
                elif link not in stats:
                    stats[link]=1


            i+=1


        #jump out if no meaningful results
        if len(stats)==0:
            yield "/u/"+self.args[1]+" has no links in comments."
            return
        
        #list links in reverse order of frequency
        link_list=sorted(stats, key=stats.get, reverse=True)

        #get length of longest domain
        l=0
        for entry in link_list:
            l=max(l,len(entry))

        text= "In {} posts or comments, /u/{} has included links to the following sites:".format(str(i),self.args[1])

        #assemble the text of the response
        for entry in link_list:
            output = entry
            output += " "*(l-len(entry)+1)+"| "
            output += str(stats[entry])
            text+="\n"+output


        #assemble payload
        title= "Activity analysis for /u/"+self.args[1]
        url='https://pastebin.com/api/api_post.php'
        payload = {'api_dev_key':self.key,
                   'api_option':'paste',
                   'api_paste_code':text,
                   'api_paste_title':title,
                   'api_paste_private':1,
                   'api_paste_expire_date':'1W'}

        response = requests.post(url,data=payload,headers=self.headers)
        yield response.content.decode('utf-8')

        
                    
