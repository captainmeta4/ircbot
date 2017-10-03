from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$history <redditor>"
        yield "See what domain /u/<redditor> submits to reddit the most."

    def exe(self, message):

        account=self.r.redditor(self.args[1])

        try:
            x=next(account.new())
        except:
            yield "Can't find the account /u/"+self.args[1]
            return

        stats={}
        total_posts=0
        for post in account.submissions.new(limit=100):

            if post.domain not in stats:
                stats[post.domain]=1
            else:
                stats[post.domain]+=1

            total_posts+=1

        x=0
        d="null"
        for entry in stats:
            if stats[entry]>x:
                x=stats[entry]
                d=entry

        percent=round(100*x/total_posts,1)

        output= "/u/{}'s most commonly submitted domain is {} at {}% of their submission activity."

        yield output.format(self.args[1], d, str(percent))

        
