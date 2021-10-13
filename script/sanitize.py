import os
import csv
import json

from models import BasicSentence, SentenceEncoder

class Sanitizer:
    """ Basic sentence filter/sanitizer to reduce inital sentence list """
    ignore_list: object
    from_lang: str
    to_lang: str

    def __init__(self, from_lang, to_lang, ignore_file):
        with open(ignore_file) as f:
            self.ignore_list = json.load(f)
            f.close()
        self.from_lang = from_lang
        self.to_lang = to_lang

    # DUPLICATES

    def is_object_duplicate(self, sentence_a: str, sentence_b: str) -> bool:
        """ Check if both sentences are actually just the same with swapped out objects. """
        cleaned_a = []
        cleaned_b = []

        a = sentence_a.upper().replace(',', ' ,').replace('.', ' .').split(' ')
        for word in a:
            if word in self.ignore_list['OBJECTS'] or word in self.ignore_list['MISC']:
                continue
            cleaned_a.append(word)
        b = sentence_b.upper().replace(',', ' ,').replace('.', ' .').split(' ')
        for word in b:
            if word in self.ignore_list['OBJECTS'] or word in self.ignore_list['MISC']:
                continue
            cleaned_b.append(word)
        return cleaned_a == cleaned_b

    def is_id_duplicate(self, id_a: int, id_b: int) -> bool:
        """ Check if both sentences share the same id"""
        return int(id_a) == int(id_b)

    # LENGTH

    def is_too_short(self, sentence: str) -> bool:
        """ Will check if the supplied sentences is too short to be interesting. """
        cleaned_s = []

        s = sentence.upper().split(' ')
        for word in s:
            if word in self.ignore_list['VERBS'] or word in self.ignore_list['MISC'] or word in self.ignore_list['FAMILY']:
                continue
            cleaned_s.append(word)

        return len(cleaned_s) <= 3

    def is_too_long(self, sentence: str) -> bool:
        """ Remove sentences that are too long and specific """
        s = sentence.upper().split(' ')

        return len(s) > 10

    # CONTENT

    def is_too_boring(self, sentence: str) -> bool:
        """ Don't include sentences that have too many generic words """
        boring_words = []
        s = sentence.upper().replace(',', ' ,').replace('.', ' .').split(' ')

        for word in s:
            if word in self.ignore_list['OBJECTS'] or word in self.ignore_list['VERBS'] or word in self.ignore_list['FAMILY'] or word in self.ignore_list['MODIFIERS']:
                boring_words.append(word)

        return len(boring_words)/len(s) > 0.5


    def process_list(self, raw_file: str) -> "list[BasicSentence]":
        sanitized_data = []

        with open(raw_file,  encoding='utf-8-sig') as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')

            current_row = next(rd)
            for next_row in rd:
                # FORMAT: [0] SV id [1] SV sentence [2] ALT id [3] ALT sentence

                if not (
                    # REMOVE DUPLICATES
                    self.is_id_duplicate(current_row[0], next_row[0]) or
                    self.is_id_duplicate(current_row[2], next_row[2]) or
                    self.is_object_duplicate(current_row[1], next_row[1]) or
                    self.is_object_duplicate(current_row[3], next_row[3]) or

                    # REMOVE LENGTH
                    self.is_too_short(current_row[1]) or
                    self.is_too_long(current_row[1]) or

                    # CONTENT FILTER
                    self.is_too_boring(current_row[1])
                ):
                    sanitized_data.append(BasicSentence(self.from_lang, current_row[1], self.to_lang, current_row[3], current_row[0]))

                current_row = next_row

        return sanitized_data

if __name__ == '__main__':
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    raw_file_path = os.path.join(data_folder, "de", "SvDeDump.tsv")
    ignore_file_path = os.path.join(data_folder, "ignores.json")

    sani = Sanitizer("sv", "de", ignore_file_path)
    sentences = sani.process_list(raw_file_path)

    print(f"Loaded {len(sentences)} sentences.")

    data = json.dumps(sentences[0:10], cls=SentenceEncoder)
    print(data)
