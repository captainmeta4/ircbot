from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$hot <subreddit>"
        yield "Fetches the current hottest post on /r/<subreddit>"

    def exe(self, message):

        success = '{} - {}'
        failure = '/r/{} does not have any posts at this time'

        for post in self.r.subreddit(self.args[1]).hot(limit=3):

            if post.stickied:
                continue

            yield self.to_text(post)
            return

        yield failure.format(self.args[1])
