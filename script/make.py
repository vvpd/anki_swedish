from process import AnkiMachine

DE_DECK_ID = 1382158747
EN_DECK_ID = 1959245867

de = AnkiMachine("Schwedisch Sätze (1300+)", "de", "SvDeDump.tsv", DE_DECK_ID)
en = AnkiMachine("Swedish sentences (3000+)", "en", "SvEnDump.tsv", EN_DECK_ID)

de.make()
en.make()
