import os
import csv
import pickle

from sanitize import Sanitizer
from grade import Grader
from sort import Sorter
from ankigen import Ankigen
from models import AugmentedSentence

class AnkiMachine:
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    def __init__(self, title:str, ref_lang: str, raw_file_name: str, deck_id: int) -> None:
        self.TITLE = title
        self.DECK_ID = deck_id
        self.REF_LANG = ref_lang
        self.raw_file_path = os.path.join(self.DATA_FOLDER, self.REF_LANG, raw_file_name)
        # standard naming
        self.STUDY_LANG = "sv"
        self.frequency_file_path = os.path.join(self.DATA_FOLDER,"sv_frequency_8000.tsv")
        self.ignore_file_path = os.path.join(self.DATA_FOLDER, "ignores.json")
        self.augmented_pickle_path = os.path.join(self.DATA_FOLDER, self.REF_LANG, "augmented_pickle.dat")
        self.sorted_pickle_path = os.path.join(self.DATA_FOLDER, self.REF_LANG, "sorted_pickle.dat")
        self.sorted_tsv_path = os.path.join(self.DATA_FOLDER, self.REF_LANG, "sorted_sentences.tsv")

    def sanitize_and_augment(self) -> None:
        sani = Sanitizer(self.STUDY_LANG, self.REF_LANG, self.ignore_file_path)
        sentences = sani.process_list(self.raw_file_path)

        print(f"Loaded {len(sentences)} sentences after sanitize.")

        grader = Grader(self.STUDY_LANG, self.frequency_file_path)
        augmented_sentences_list = grader.grade_list(sentences)

        with open(self.augmented_pickle_path, "wb") as f:
            pickle.dump(augmented_sentences_list, f)

        print(f"Dumped {len(augmented_sentences_list)} sentences into a pickle.")

    def generate(self) -> None:
        augmented_sentences: list[AugmentedSentence] = []

        if not os.path.isfile(self.augmented_pickle_path):
            self.sanitize_and_augment()

        with open(self.augmented_pickle_path, "rb") as f:
            augmented_sentences = pickle.load(f)

        print(f"Loaded {len(augmented_sentences)} sentences from a pickle.")

        sorti = Sorter()
        sorted_sentences = sorti.sort_and_skim(augmented_sentences)

        print(f"Remaining {len(sorted_sentences)} sentences after sorting and skimming.")

        with open(self.sorted_tsv_path, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            for sentence in sorted_sentences:
                writer.writerow([sentence.text.from_lang, sentence.text.original, sentence.text.to_lang, sentence.text.translation, sentence.hardest_word.item])

        print(f"Wrote skimmed sentences to tsv.")

        with open(self.sorted_pickle_path, "wb") as f:
            pickle.dump(sorted_sentences, f)

        print(f"Dumped {len(sorted_sentences)} sorted sentences into a pickle.")

    def export(self):
        ex = Ankigen(self.TITLE, self.DECK_ID, self.REF_LANG)
        ex.generate()

    def make(self):
        self.generate()
        self.export()
