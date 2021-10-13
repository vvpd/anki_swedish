import pickle
import os
import genanki

class Ankigen:
    STYLE = """
    .card {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        background-color: var(--bg-color);
        color: var(--text-color);
        --bg-color: #eee;
        --text-color: #000;
        font-size: 50px;
    }

    .mobile .card {
        font-size: 35px;
    }

    .front, .back {
        margin: 5% auto;
        width: 85%;
        border: 0px solid lightgray;
        padding: 0px;
        text-align: center;
        font-size: 1.0em;

    }

    .backside-front {
        display:none;
        font-size: 0.4em;
        letter-spacing: 0.2px;
    }

    .word {
        text-align: center;
        font-size: 0.5em;
    }

    .word a {
        font-family: monospace;
        border-bottom: 2px dotted black;
    }


    #links {
        margin: 80px auto 20px auto;
        width: 70%;
        border: 3px solid lightgray;
        padding: 10px;
        text-align: left;
        font-size: 1.0em;
        border-radius:10px;
    }


    #button {
        margin: 80px auto 20px auto;
        width: 200px;
        border: 2px solid lightgray;
        padding: 10px;
        text-align: center;
        font-size: 1.5em;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        border-radius:25px;
            color: var(--text-color);
            letter-spacing: 0.7px;
    }

    .mobile #links {
        margin: 50px auto 10px auto;
        font-size: 1.5em;
    width: 90%;

    }

    .mobile #button {
        margin: 50px auto 10px auto;

        font-size: 1.2em;
    }

    """

    FRONTSIDE = """
            <div class="front">{{Sentence (translated)}}</div>
    """

    BACKSIDE = """

        <div class="front backside-front">{{Sentence (translated)}}</div>

        <div class="back" id="answer">{{Sentence (original)}}</div>

        <div class="word"><a href="https://en.wiktionary.org/wiki/{{word}}#Swedish">{{word_marker}} {{word}}</a></div>

        <div style='font-family: serif; font-size: 12px; Color: Gray'>
            <div id="button" onMouseOver="show('links')">Show more</div>
        </div>

        <div id="links" style='display: none; text-align: center;'>
            <div style='font-family: monospace; font-size: 0.35em; margin: 5px ;'>
                <div id="lemmas" style='display: none;'>{{lemmas}}</div>
                <div>
                                        <span style="font-size: 0.8em">Lemmas (auto-generated, might contain errors)</span>
                    <div style="margin-top: 15px;">W: <div id="wiki" style="display: inline;"></div></div>
                    <div style="margin-top: 15px;">S: <div id="svenska" style="display: inline;"></div></div>
                </div>
									<div style="font-size: .9em; margin-top:20px; margin-bottom:5px;"><a href="https://tatoeba.org/en/sentences/show/{{tatoeba_id}}">↗ view source</a>
            </div>
        </div>

        <script>
            function show(id) {
                document.getElementById(id).style.display = "block";
                document.getElementById('button').style.display = "none";
            }

            function hide(id) {
                document.getElementById(id).style.display = "none";
            }

            var content = document.getElementById("lemmas").innerHTML.replace("'"," ");

            var punctuationless = content.replace(/[.,\/#!?$%\^&\*;:{}=\-_`~()]/g, "");
            var mixedCase = punctuationless.replace(/\s{2,}/g, " ");
            var finalString = mixedCase.toLowerCase();

            var words = (finalString).split(" ");

            var wiki_text = "";
            for (i = 0; i < words.length; i++) {
                wiki_text += "<a href = 'https://en.wiktionary.org/wiki/" + words[i] + "#Swedish'>";
                wiki_text += words[i];
                wiki_text += "</a> ";
            }

            document.getElementById("wiki").innerHTML = wiki_text;

            var sv_text = "";
            for (i = 0; i < words.length; i++) {
                sv_text += "<a href ='https://svenska.se/tre/?sok=" + words[i] + "'>";
                sv_text += words[i];
                sv_text += "</a> ";
            }

            document.getElementById("svenska").innerHTML = sv_text;

        </script>

    """

    MODEL_ID = 1712164860

    def __init__(self, title, deck_id, ref_lang) -> None:
        self.REF_LANG: str = ref_lang
        self.DECK_ID: int = deck_id
        self.DECK_TITLE: str = title
        self.model = genanki.Model(
            self.MODEL_ID,
            'Sentence Learning',
            fields=[
                {'name': 'Sentence (original)'},
                {'name': 'Sentence (translated)'},
                {'name': 'Language code (original)'},
                {'name': 'Language code (translated)'},
                {'name': 'word'},
                {'name': 'word_marker'},
                {'name': 'lemmas'},
                {'name': 'CEFR'},
                {'name': 'CEFR_level'},
                {'name': 'tatoeba_id'},
            ],
            templates=[
                {
                    'name': 'Translation -> Original',
                    'qfmt': self.FRONTSIDE,
                    'afmt': self.BACKSIDE,
                },
            ],
            css=self.STYLE
        )

        self.deck = genanki.Deck(
            self.DECK_ID,
            self.DECK_TITLE
        )
        self.DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        self.sorted_pickle_path = os.path.join(self.DATA_FOLDER, self.REF_LANG, "sorted_pickle.dat")


    def generate(self):
        sentences = []

        with open(self.sorted_pickle_path, "rb") as f:
            sentences = pickle.load(f)
            print(f"loaded {len(sentences)} from pickle")

        for sentence in sentences:
            self.deck.add_note(genanki.Note(
                model=self.model,
                fields=[
                    str(sentence.text.original),
                    str(sentence.text.translation),
                    str(sentence.text.from_lang),
                    str(sentence.text.to_lang),
                    str(sentence.hardest_word.item),
                    str(sentence.hardest_word.marker),
                    str(" ".join(sentence.lemmas)),
                    str(sentence.cefr),
                    str(sentence.cefr_level),
                    str(sentence.text.tatoeba_id)
                ],
                guid=sentence.text.tatoeba_id,
                tags=[sentence.cefr]
                )
            )

        genanki.Package(self.deck).write_to_file(os.path.join(self.DATA_FOLDER, self.REF_LANG, f"sv_{self.REF_LANG}_cards.apkg"))

        print(f"Exported anki deck as sv_{self.REF_LANG}_cards.apkg")
