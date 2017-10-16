from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$recent <subreddit> <redditor>"
        yield "Get the most recent submission by /u/<redditor> to /r/<subreddit>."

    def exe(self, message):

        account=self.r.redditor(self.args[2])

        try:
            x=next(account.new())
        except:
            yield "Can't find the account /u/"+self.args[2]
            return

        subreddit = self.r.subreddit(self.args[1])

        try:
            x=next(subreddit.new())
        except:
            yield "Can't find the subreddit /r/"+self.args[1]
            return

        for submission in account.submissions.new(limit=100):
            if submission.subreddit==subreddit:
                yield self.to_text(submission)
                break
        else:
            yield "No recent submissions by /u/{} in /r/{} found".format(self.args[2],self.args[1])
