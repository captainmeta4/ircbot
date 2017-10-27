from bot import Plugin
import random
import re

class Main(Plugin):

    def helptext(self):

        yield "$trump"
        yield "Generates a random Donald Trump phrase."

    def on_start(self):

        self.generate_corpus()

    def text_to_triples(self, text):
        #generates triples given text

        data = text.split()

        #cancel out on comments that are too short
        if len(data) < 3:
            return

        self.lengths.append(len(data))

        #iterate through triples
        for i in range(len(data)-2):
            yield (data[i], data[i+1], data[i+2])

    
    def generate_text(self, text=""):
        key = random.choice(self.starters)
        output = self.continue_text(key)

        # fix formatting
        output = re.sub(" \* ","\n\n* ",output)
        output = re.sub(" >","\n\n> ",output)
        output = re.sub(" \d+\. ","\n\n1. ", output)
        
        return output

    def continue_text(self, key):

        #start the output based on a key of ('word1','word2)
        output = key[0]+" "+key[1]
        
        length = random.choice(self.lengths)

        #Add words until we hit text-ending criteria or a key not in the corpus
        while True:

            if (len(output.split())> length and
                ((output.endswith(".") and not output.endswith("..."))
                 or output.endswith("!")
                 or output.endswith("?"))
                ):
                break

            if key not in self.corpus:
                break
            
            next_word = random.choice(self.corpus[key])
            output += " " + next_word

            key = (key[1], next_word)
            
        return(output)

    def generate_corpus(self):

        #loads comments and generates a dictionary of
        #  {('word1','word2'): ['word3','word4','word5'...]...}

        self.corpus = {}
        self.starters = []
        self.lengths = []


        
        #for every comment
        for line in open('plugins/trump.txt','br'):

            l=line.decode()

            #ignore titles
            if l.startswith('#'):
                continue

            #ignore paragraph breaks
            if len(l)==0:
                continue
            
            #print("processing comment "+str(i))
            #get 3-word sets
            #add line starters to starters list
            start_of_line=True
            
            for triple in self.text_to_triples(l):
                key = (triple[0], triple[1])

                #note valid comment starters
                if start_of_line:
                    self.starters.append(key)
                    start_of_line=False

                #add to corpus

                if key in self.corpus:
                    self.corpus[key].append(triple[2])
                else:
                    self.corpus[key] = [triple[2]]

    def exe(self, message):

        #generate corpus

        yield self.generate_text()
        
