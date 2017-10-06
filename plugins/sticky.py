from __main__ import Plugin

class main(Plugin):

    def helptext(self):

        yield "$sticky <subreddit>"
        yield "Fetches the current stickied post(s) on /r/<subreddit>"

    def exe(self, message):

        exists=False

        success = '{} - {}'
        failure = '/r/{} does not have any stickied posts at this time'

        for post in self.r.subreddit(self.args[1]).hot(limit=2):

            if post.stickied:
                exists=True
                yield success.format(post.shortlink, post.title)

        if not exists:
            yield failure.format(args[1])
                
