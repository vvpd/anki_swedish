import csv
import re
import os
import stanza
from models import BasicSentence, AugmentedSentence, FrequencyData

class Grader:
    MAX_WPM = 3000.0
    cerf_levels = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "C2": 5}
    word_list: "dict[str, FrequencyData]" = {}
    ignore_lemmas = ["@", "”", "\"", "–", "-", "'", "'"]

    def __init__(self, language, frequency_file):
        self.nlp = stanza.Pipeline(language, logging_level='WARN')
        with open(frequency_file, encoding="utf-8-sig") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:
                lemma = re.sub(r"\([^()]*\)", "", row[4])
                if lemma not in self.word_list:
                    self.word_list[lemma] = FrequencyData(
                        int("0" + row[0]), float(row[1].replace(",", ".")), row[2], row[3], row[4]
                    )

    def grade_sentence(self, input_sentence: BasicSentence) -> AugmentedSentence:
        """Takes in a sentence string and returns its grading"""
        doc = self.nlp(input_sentence.original)
        word_count = 0
        wpm = 0.0
        cefr = "A1"
        hardest_word = self.word_list['i']
        lemmas: list[str] = []
        for sentence in doc.sentences:
            for word in sentence.words:
                # Skip interpunction
                if word.upos == 'PUNCT':
                    continue
                lemma = word.lemma
                if lemma in self.ignore_lemmas:
                    continue
                if lemma not in self.word_list:
                    continue

                # Now we do sth
                if lemma not in lemmas:
                    lemmas.append(lemma)
                word_info = self.word_list[lemma]
                word_count += 1
                wpm += min(
                    self.MAX_WPM,
                    word_info.wpm,
                )
                if self.cerf_levels[word_info.cefr] >= self.cerf_levels[cefr]:
                    cefr = word_info.cefr
                    if word_info.wpm < hardest_word.wpm:
                        hardest_word = word_info

        avg_wpm = wpm / word_count if word_count > 0 else 0

        return AugmentedSentence(input_sentence, avg_wpm, word_count, cefr, self.cerf_levels[cefr], hardest_word, lemmas)

    def grade_list(self, sentence_list: "list[BasicSentence]") -> "list[AugmentedSentence]":
        augmented = []
        length = len(sentence_list)
        i = 1
        print(f"Starting to augment {length} sentences")
        for sentence in sentence_list:
            augmented.append(self.grade_sentence(sentence))
            print(f"  ...processing {i}/{length}", end='\r')
            i+=1
        print("All done.")
        return augmented

if __name__ == "__main__":
    frequency_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "data",
        "sv_frequency_8000.tsv",
    )
    g = Grader("sv", frequency_file_path)
    a = g.grade_sentence(
        BasicSentence("sv", "Om du kunde resa tillbaka i tiden, vad skulle du i så fall ändra på?", "de", "", "12")
    )
    print(a)
