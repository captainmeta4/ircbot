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
              client_secret=os.environ.get('client_secret'_)

#command character
c='+'


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
            self.plugins[name]=__import__('plugins.%s'%name,fromlist=['plugins'])
            
            print('imported plugin: '+name)

        if refresh:
            for name in old_list:
                self.plugins[name]=importlib.reload(self.plugins[name])
            
        

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
        

        

    def run(self):

        
        #passive listening, with auto-handling of PING taken care of behind the scenes
        for message in self.i.listen():

            #hard code plugin reload
            if message.nick=="captainmeta4" and message.body==c+"reload":
                self.reload_plugins(refresh=True)
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

            #now try generic plugin call
            if message.body.startswith(c):
                self.args=message.body.lstrip(c).split()
                if self.args[0] not in self.plugins:
                    continue

                try:
                    message.reply(self.plugins[self.args[0]].main(message,r))
                except:
                    message.reply('%s: something went wrong there'%message.nick)

                
            
    
    


if __name__=="__main__":
    b=Bot()
    b.run()
