from __main__ import Plugin

class Main(Plugin):

    def helptext(self):

        yield "$sticky <subreddit>"
        yield "Fetches the current stickied post(s) on /r/<subreddit>"

    def exe(self, message):

        exists=False

        failure = '/r/{} does not have any stickied posts at this time'

        for post in self.r.subreddit(self.args[1]).hot(limit=2):

            if post.stickied:
                exists=True
                yield self.to_text(post)

        if not exists:
            yield failure.format(args[1])
                
