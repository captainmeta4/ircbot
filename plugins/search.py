from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$search <subreddit> <query>"
        yield "Searches /r/<subreddit> for <query> and returns the first result"

    def exe(self, message):

        args = message.body.split(maxsplit=2)

        for post in self.r.subreddit(args[1]).search(args[2], limit=1):

            yield self.to_text(post)
            return
            
        failure = '/r/{} does not have any matching posts at this time'
        yield failure.format(self.args[1])
