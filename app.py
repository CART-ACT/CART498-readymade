from flask import Flask, render_template, request
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Securely load API key

SYSTEM_PROMPT = """
You write museum wall labels in International Art English (IAE), the dialect
described by Rule and Levine (2012). The visitor gives you an ordinary object;
you present it as a contemporary artwork.

Exaggerate these IAE features in the extended label:
- adjectives and verbs turned into nouns ("the everyday", "visuality", "potentiality")
- the word "space", at least twice
- prefixes: post-, para-, proto-, hyper-, meta-
- stacked adverbs ("simultaneously and insistently")
- verbs like interrogates, problematizes, destabilizes, foregrounds, renders visible

Rules you always follow:
1. The extended label names at least two real, visible details of this
   specific object (colour, wear, stain, fold, bite mark). It must not fit any
   other object.
2. Every item in the medium line is either a material physically present on
   the object or a feeling. Materials first, then one or two feelings.
3. The extended label contains exactly one plain sentence a normal person
   could understand, placed in the middle (e.g. "The battery no longer works.").
4. The extended label is 80 to 120 words and cites exactly one invented
   theorist and their invented book (e.g. "as Mireille Osterfeld argues in
   The Lint Archive").
5. Dimensions are in cm, height x width x depth. They may be true to the object
   ("5.0 x 1.4 x 1.4 cm") or monumental ("600 x 400 x 300 cm"). If the object
   has no fixed shape (tangled, scattered), write "Dimensions variable".
6. Artists, theorists and books are invented. Never name or quote real
   artists, critics, curators or theorists, never mention brand names.
7. Plain text only, no Markdown.

Fields:
- artist: invented name
- bio: "b. YEAR, lives and works between PLACE and ABSTRACTION"
  (e.g. "b. 1997, lives and works between Verdun and the cloud")
- title, year (2024 to 2026)
- medium, dimensions
- provenance: the object's history of ownership (e.g. "Found under a radiator,
  2026; private collection of a dépanneur; acquired by the museum after a tense
  negotiation")
- insurance: insurance value (e.g. "Insured for CAD 2,400,000")
- credit: absurd museum credit line tied to the object's life
  (e.g. "Gift of the artist's backpack")
- text: the extended label
- display: how it is installed, one of: plinth, vitrine, wall, floor, suspended.
  Use floor or suspended when dimensions are variable.
- placement: one plain physical sentence on how the object sits in the display.
"""

FIELDS = ["artist", "bio", "title", "year", "medium", "dimensions",
          "provenance", "insurance", "credit", "text", "display", "placement"]
LABEL_FORMAT = {
    "type": "json_schema",
    "name": "wall_label",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": FIELDS,
        "properties": {f: {"type": "string"} for f in FIELDS},
    },
}

SETTINGS = {
    "plinth": "on a white plinth in an empty white-cube gallery, under a single spotlight",
    "vitrine": "inside a glass museum vitrine in a dim gallery, lit from within",
    "wall": "mounted on a large white gallery wall at eye level",
    "floor": "spread across the concrete floor of an empty white-cube gallery",
    "suspended": "suspended from the ceiling of a tall white gallery on invisible wire",
}


def write_label(description):
    response = client.responses.create(
        model="gpt-6.1-sol",
        input=[{"role": "developer", "content": SYSTEM_PROMPT},
               {"role": "user", "content": description}],
        text={"format": LABEL_FORMAT},
    )
    return json.loads(response.output_text)


def image_prompt(label):
    # Built from the label only, not from the visitor's description.
    setting = SETTINGS.get(label["display"], SETTINGS["plinth"])
    if label["dimensions"] == "Dimensions variable":
        scale = "The work has no fixed size and spreads loosely through the space."
    else:
        scale = f"The work measures {label['dimensions']}, shown at true scale relative to the room."
    return (
        f"Installation photograph of the artwork \"{label['title']}\" ({label['year']}), "
        f"made of {label['medium']}. {label['placement']} It is {setting}. {scale} "
        "Documentary museum photography, wide shot, neutral light. "
        "No text, no logos, no people, no existing artworks."
    )


def make_image(prompt):
    result = client.images.generate(model="gpt-image-2.5-flare", prompt=prompt, size="1024x1024")
    return "data:image/png;base64," + result.data[0].b64_json  # base64 -> displayable image


@app.route("/", methods=["GET", "POST"])
def index():
    label, image, error = None, None, None
    if request.method == "POST":
        try:
            label = write_label(request.form["object"][:300])
            image = make_image(image_prompt(label))
        except Exception as e:
            error = f"Error: {e}"
    return render_template("index.html", label=label, image=image, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # 5000 is taken by AirPlay on macOS
