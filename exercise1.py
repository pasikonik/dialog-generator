import csv
import random
import nltk

actors = {}


def tokenizer(dialog, gram=3):
    tokenized = nltk.word_tokenize(dialog)
    if len(tokenized) < gram:
        pass
    else:
        for i in range(len(tokenized) - gram):
            yield (tokenized[i:i + (gram + 1)])


class Actor:
    def __init__(self, name):
        self.name = name
        self.dialogs = []
        self.probabilities = {}
        self.lengths = []

    def add_dialog(self, dialog):
        for sequence in tokenizer(dialog):

            key = tuple(sequence[0:-1])
            if key in self.probabilities:
                self.probabilities[key].append(sequence[-1])
            else:
                self.probabilities[key] = [sequence[-1]]

        self.lengths.append(len(nltk.word_tokenize(dialog)))
        self.dialogs.append(dialog)

    def generate(self):
        result = []
        length = random.choice(self.lengths)
        first_atom = random.choice(list(self.probabilities.keys()))
        for word in list(first_atom):
          result.append(word)
        while len(result) < length:
            current_key = tuple(result[-3:])
            atom = random.choice(self.probabilities[current_key])
            result.append(atom)
        print(' '.join(result))


with open('transcriptions/clean_dialog.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        actor_name = row[2]
        if actor_name in actors:
            actors[actor_name].add_dialog(row[3])
        else:
            new_actor = Actor(actor_name)
            new_actor.add_dialog(row[3])
            actors[actor_name] = new_actor
