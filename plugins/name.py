from __main__ import Plugin

class Main(Plugin):

    def exe(self, message):

        yield 'your name is '+message.nick
        return
