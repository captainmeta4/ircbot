from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$top <subreddit>"
        yield "Fetches the top post of all time on /r/<subreddit>"

    def exe(self, message):

        success = '{} - {}'
        failure = '/r/{} does not have any posts at this time'

        for post in self.r.subreddit(self.args[1]).top(limit=1):

            if post.stickied:
                continue

            yield self.to_text(post)
            return

        yield failure.format(self.args[1])
