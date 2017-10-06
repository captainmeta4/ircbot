import praw
import os
import irclib
import yaml
import plugins
from pathlib import Path
import importlib
import os

#set globals
r=praw.Reddit(user_agent="captainmeta4's interface with IRC",
              username='cm4_IRC_interface',
              password=os.environ.get('reddit-password'),
              client_id=os.environ.get('client_id'),
              client_secret=os.environ.get('client_secret'))

#command character
c='$'

class Plugin():

    def __init__(self):

        self.r=r

    def exe(self, message):
        #function to be overridden in subclasses
        pass

    def to_text(self, submission):

        #gives a readable string from a submission object
        return '{} - {}'.format(submission.shortlink, submission.title)

    def run(self, message):

        #make args

        self.args=message.body.lstrip(c).split()

        for response in self.exe(message):

            message.reply(message.nick+": "+response)


    def helptext(self):
        #this function intended to be overridden in subclasses
        yield "No help currently available for this function"

    def help(self, message):

        for line in self.helptext():
            message.reply(message.nick+": "+line)
        


class Bot():

    def __init__(self):

        #make new irc object, load config off reddit, connect to servers and join channels
        self.reset_irc()

        self.reload_plugins()


    def reset_irc(self):
        self.i=irclib.IRC()
        self.load_config()


        for entry in self.config:
            self.i.add_server(entry,
                         self.config[entry]['port'],
                         self.config[entry]['nick'],
                         self.config[entry]['username'],
                         self.config[entry]['password'],
                         self.config[entry]['realname'],
                         channels=self.config[entry].get('channels',[]),
                         raw=self.config[entry].get('raw',False)
                         )

    def reload_plugins(self, refresh=False):

        if refresh:
            old_list=self.plist

        #crawl the plugins folder
        p=Path('./plugins')



        self.plist=[]
        
        self.plugins={}
        
        for file in p.iterdir():
            if not file.name.endswith('.py'):
                continue
            self.plist.append(file.name.rsplit(sep='.py',maxsplit=1)[0])


        for name in self.plist:
            self.plugins[name]=__import__('plugins.%s'%name,fromlist=['plugins']).Main()
            
            print('imported plugin: '+name)

        if refresh:
            for name in old_list:
                if name in self.plugins:
                    self.plugins[name]=importlib.reload(__import__('plugins.%s'%name,fromlist=['plugins'])).Main()
            
        

    def load_config(self):

        #fetch and interpret wiki page
        self.config=next(yaml.safe_load_all(r.subreddit('captainmeta4bots').wiki['ircbot/config'].content_md))

    def save_config(self, reason=None):
        output = yaml.dump(self.config)
        output = "    "+output.replace("\n","\n    ")
        output = output.replace("    ---","---")
        r.subreddit('captainmeta4bots').wiki['ircbot/config'].edit(output,reason=reason)

    def admin(self, message):
        #admin commands

        args=message.body.lstrip(c).split(maxsplit=1)

        if args[0]=="ignore":

            #try to whois
            u=irclib.User(message.server, args[1])

            self.config[message.server.host]['ignore'].append(u.mask)
            self.save_config(reason="ignore "+args[1])
            message.reply("Now ignoring "+u.mask)
            
        elif args[0]=="ignorelist":
            o=""
            for entry in self.config[message.server.host]['ignore']:
                o=o+entry+" "
            message.reply("Currently ignoring: "+o)

        elif args[0]=="uignorelist":
            o=""
            for entry in self.config[message.server.host]['uignore']:
                o=o+entry+" "
            message.reply("Currently ignoring: "+o)            
            
        elif args[0]=="unignore":
            u=irclib.User(message.server, args[1])
            try:
                self.config[message.server.host]['ignore'].pop(self.config[message.server.host]['ignore'].index(u.mask))
            except ValueError:
                message.reply(u.mask+" not found in ignore list")
                return
            self.save_config(reason="unignore "+args[1])
            message.reply("Successfully unignored "+args[1])
                
        elif args[0]=="join":
            message.server.add_channel(args[1])
            self.config[message.server.host]['channels'].append(args[1].lower())
            self.save_config(reason="join "+args[1])
            
        elif args[0]=="part":
            message.server.part_channel(args[1])
            self.config[message.server.host]['channels'].pop(self.config[message.server.host]['channels'].index(args[1].lower()))
            self.save_config(reason="part "+args[1])

        elif args[0]=="send":
            message.server.send(args[1])

    def help(self, message):

        #send a PM to the user with available commands
        output=""
        p=[]
        for plugin in self.plugins:
            p.append(plugin)

        p.sort()
        for name in p:
            output+=name+" "

        message.server.notice(message.nick, 'List of available commands. Type "$help <command>" for more information on a specific function')
        message.server.notice(message.nick, output)

        

    def run(self):

        
        #passive listening, with auto-handling of PING taken care of behind the scenes
        for message in self.i.listen():

            #hard code plugin reload
            if message.nick=="captainmeta4" and message.body==c+"reload":
                self.reload_plugins(refresh=True)
                continue

            #check for channel invite
            if message.type=="INVITE":
                message.server.join(message.body)

            #hard code help
            if message.body==c+"help":
                self.help(message)
                continue
            

            #check for admin commands
            if message.nick=="captainmeta4" and message.body.startswith(c):
                self.admin(message)

            #ignore list:
            if message.nick is not None:
                if (message.nick.lower() in self.config[message.server.host]['ignore']+self.config[message.server.host]['uignore']
                    or "{}@{}".format(message.userid, message.host) in self.config[message.server.host]['ignore']+self.config[message.server.host]['uignore']
                    ):
                    continue

            #ignore other bots
            if "/bot/" in message.host:
                continue

            #now try generic plugin calls
            if message.body.startswith(c):
                self.args=message.body.lstrip(c).split()
                
                #help
                if self.args[0]=="help":
                    try:
                        self.plugins[self.args[1]].help(message)
                    except Exception as e:
                        message.reply(message.nick+": "+str(e))
                    continue

                #bogus commands
                if self.args[0] not in self.plugins:
                    continue


                
                #now do plugin
                try:
                    self.plugins[self.args[0]].run(message)
                except Exception as e:
                    message.reply(message.nick+": "+str(e))

                
            
    
    


if __name__=="__main__":
    b=Bot()
    b.run()
