from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$new <subreddit>"
        yield "Fetches the newest post on /r/<subreddit>"

    def exe(self, message):

        success = '{} - {}'
        failure = '/r/{} does not have any posts at this time'

        for post in self.r.subreddit(self.args[1]).new(limit=1):

            yield self.to_text(post)
            return

        yield failure.format(self.args[1])
