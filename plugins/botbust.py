def main(message, r, *args):

    arg=message.body.split()

    name=arg[1]

    account=r.redditor(name)

    try:
        x=next(account.new())
    except:
        return message.nick+": Can't find the account /u/"+name

    url="http://reddit.com/u/"+name
    title="Overview for "+name
    comment="Reported by {} in channel {}".format(message.nick, message.target)

    post=r.subreddit('botbust').submit(title=title,url=url)

    post.reply(comment)

    return 'http://reddit.com'+post.permalink
