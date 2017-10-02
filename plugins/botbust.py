from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$botbust <redditor>"
        yield "Report /u/<redditor> to /r/BotBust"

    def exe(self, message):

        account=self.r.redditor(self.args[1])

        try:
            x=next(account.new())
        except:
            yield "Can't find the account /u/"+self.args[1]
            return

        url="http://reddit.com/u/"+self.args[1]
        title="Overview for "+self.args[1]
        comment="Reported by {} in channel {} on {}".format(message.nick, message.target, message.server.host)

        post=self.r.subreddit('botbust').submit(title=title,url=url)

        post.reply(comment)

        yield 'http://reddit.com'+post.permalink
