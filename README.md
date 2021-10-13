# Swedish learning with sentences

## 🏄‍♀️ Tatoeba to Anki flow 🏄‍♂️
This can potentially work with any language, but i made it for 🇸🇪.

I generated two decks already for SV/DE and SV/EN pairs, more pairs can be generated with the python scripts in the `script` directory. For the pre-made decks open the `data` directory and select the respective language.

## Install
1. Get dependencies from pip

```bash
$ pip install genanki
$ pip install stanza
```

2. Download the language model in python

```python
import stanza; stanza.download('sv')
```

## Generate
1. Get sentence pair data from [tatoeba](https://tatoeba.org/en/downloads). Select Swedish + target language.
2. Make subfolder in `data` directory and move your download there.
3. Edit `script/make.py` and run.
