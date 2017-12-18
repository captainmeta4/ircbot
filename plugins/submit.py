from __main__ import Plugin
import praw
import re

class Main(Plugin):

    def helptext(self):

        yield "Administrative use only."

    def exe(self, message):

        #check that it's me
        if not self.is_captainmetaphor(message):
            yield "You are not authorized to use that command"
            return

        args = message.body.split(maxsplit=3)

        #check url validity
        if re.match('https?://\S', args[2]) is None:
            yield "bad URL"
            return

        #make praw instance as captainmeta4
        r=praw.Reddit('captainmeta4')



        subreddit = r.subreddit(args[1])
        url = args[2]
        title=args[3]

        submission = subreddit.submit(title, url=url)

        yield self.to_text(submission)
        


