from __main__ import Plugin
import requests
import os

class Main(Plugin):

    def on_start(self):

        self.key=os.environ.get('yandex_key')
        self.headers={"User-Agent":"Translation Module for captainmeta4 IRC Interface"}
        
        #get supported languages
        url='https://translate.yandex.net/api/v1.5/tr.json/getLangs'
        params = {'key': self.key,
                  'ui':'en'}
        x=requests.get(url,params=params, headers=self.headers)
        self.langs=x.json()

    def helptext(self):

        yield "$translate <language> <text>"
        yield "Translate <text> to <language> using Yandex.Translate."

        
    def exe(self, message):

        #valid languages

        if self.args[1] not in self.langs['langs']:
            yield 'Target language not specified.'
            self.notice=True
            yield "Supported Languages:"
            for lang in self.langs['langs']:
                yield lang+" - "self.langs['langs'][lang]
            self.notice=False
            return

        #get text to translate
        text=message.body.split(maxsplit=2)[2]

        #Assemble params for translation
        params={'key':self.key,
                'text':text,
                'lang':self.args[1],
                'format':'plain'}
        url='https://translate.yandex.net/api/v1.5/tr.json/translate'

        #hit translation api
        response = requests.get(url,params=params,headers=self.headers)

        yield response.json()['text'][0]
