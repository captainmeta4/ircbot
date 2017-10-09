from __main__ import Plugin
import re

class Main(Plugin):

    def helptext(self):

        yield "$analyze <redditor>"
        yield "See what domains /u/<redditor> links to the most within comments."

    def exe(self, message):

        #set plugin to respond as a notice
        self.notice=True

        #find the redditor
        account=self.r.redditor(self.args[1])

        try:
            x=next(account.new())
        except:
            yield "Can't find the account /u/"+self.args[1]
            return

        stats={}
        i=0

        #examine comments for links
        for comment in account.comments.new(limit=100):

            #find links
            links=re.findall('https?://([\w.-]+)', comment.body)

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
        
        #list links in reverse order of frequency
        link_list=sorted(stats, key=stats.get, reverse=True)

        #get length of longest domain
        l=0
        for entry in link_list:
            l=max(l,len(entry))
            

        yield "comment analysis for /u/"+self.args[1]
        if len(link_list)==0:
            yield "/u/"+self.args[1]+" has no links in comments."
            return

        yield "In {} comments, /u/{} has included links to the following sites:".format(str(i),self.args[1])

        for entry in link_list:
            output = 'https://'+entry
            output += " "*(l-len(entry)+1)+"| "
            output += str(stats[entry])
            yield output

        
                    
