from models import AugmentedSentence

class Sorter:
    lemma_occurances: "dict[str, int]" = {}
    sentence_data: "list[AugmentedSentence]" = []
    skimmed_data: "list[AugmentedSentence]" = []

    def __init__(self):
        pass

    def sort_and_skim(self, sentence_data) -> "list[AugmentedSentence]":
        self.sentence_data = sentence_data
        self.lemma_occurances = {}
        self.skimmed_data = []
        self.sentence_data.sort(key=lambda x: x.average_wpm, reverse=True)
        self.count_lemmas()
        self.skim_list()

        return self.skimmed_data

    def count_lemmas(self):
        for sentence in self.sentence_data:
            for lemma in sentence.lemmas:
                if lemma in self.lemma_occurances:
                    self.lemma_occurances[lemma] += 1
                else:
                    self.lemma_occurances[lemma] = 1

    def skim_list(self):
        for sentence in self.sentence_data:
            skip = False
            repetitions = 0
            total_occurances = 0
            rarest_word = 50

            for lemma in sentence.lemmas:
                lemma_count = self.lemma_occurances[lemma]
                total_occurances += lemma_count
                if lemma_count > 2:
                    repetitions += 1
                if lemma_count < rarest_word:
                    rarest_word = lemma_count

            repeating_percent = (repetitions / max(len(sentence.lemmas), 1) ) * 100
            repeating_avg = (total_occurances / max(len(sentence.lemmas), 1) )

            if rarest_word > 20: skip = True
            if repeating_avg > 100 and sentence.cefr_level < 2: skip = True
            if sentence.cefr_level == 0 and len(sentence.lemmas) < 5: skip = True
            if sentence.cefr_level == 1 and len(sentence.lemmas) < 4: skip = True
            if sentence.cefr_level == 2 and len(sentence.lemmas) < 3: skip = True
            if repeating_avg > 150: skip = True
            if sentence.cefr_level >= 3: skip = False

            if skip:
                for lemma in sentence.lemmas:
                    self.lemma_occurances[lemma] -= 1
                continue

            self.skimmed_data.append(sentence)
