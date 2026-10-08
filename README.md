# Readymade

A Flask app (CART 498 assignment that turns an ordinary object into a work of contemporary art. You describe an object, and the app writes its museum label (tombstone and extended label) in International Art English (IAE) and generates a photograph of the object installed in a gallery.


## IAE features and prompt rules

From Rule and Levine (2012), the system prompt (`app.py`, `SYSTEM_PROMPT`) asks the model to exaggerate:

- nominalisation: "the everyday", "visuality", "potentiality"
- the word "space", at least twice
- the prefixes post-, para-, proto-, hyper- and meta-
- stacked adverbs: "simultaneously and insistently"
- critical verbs: interrogates, problematizes, destabilizes, foregrounds

It also defines explicit rules the model always follows:

1. **Precision:** the text names at least two real, visible details of this specific object.
2. **Honest medium:** every material is either physically on the object or a feeling.
3. **One plain sentence:** exactly one sentence a normal person could understand, placed in the middle ("The battery no longer works.").
4. **Length and theory:** the extended label is 80 to 120 words and cites one invented theorist and their invented book.
5. **Dimensions:** in cm, either true to the object or monumental (600 x 400 x 300 cm), or "Dimensions variable" for shapeless objects.
6. **No borrowed reputations:** invented artists, theorists and books only, with no real critics, quotes or brands.

The label comes back as JSON with fixed fields (artist, bio, title, year, medium, dimensions, provenance, insurance, credit, text, display, placement), so every label contains all the required parts.

## How the image prompt is derived from the label

The visitor's description never reaches the image model. `image_prompt()` builds the prompt from the label:

- **title and year:** the artwork
- **medium:** what it is made of (feelings included, which nudges the mood)
- **placement:** a plain sentence the model writes about how the object sits
- **display:** one of plinth, vitrine, wall, floor or suspended. Each maps to a fixed gallery setting.
- **dimensions:** the label sets the scale. The size is rendered "at true scale relative to the room", so a battery is tiny and a 600 x 400 cm granola bar fills the gallery. "Dimensions variable" becomes "spreads loosely through the space", and the label must then use floor or suspended.

The prompt ends with "No text, no logos, no people, no existing artworks."

Example (`docs/examples/battery.json`):

> Installation photograph of the artwork "Afterlife of a Cell" (2025), made of metal, unease. It lies horizontally on the plinth with the dented negative end facing left. It is on a white plinth in an empty white-cube gallery, under a single spotlight. The work measures 5.0 x 1.4 x 1.4 cm, shown at true scale relative to the room. …

## User guide

1. Type a short description of an object, for example "a single blue sock with a hole in the heel". Specific details give better labels.
2. Click **Accession** and wait about 30–60 seconds.
3. The installation view appears with the wall label beside it. On a phone, the label sits below the image.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env-bup .env   # then put your OPENAI_API_KEY in .env
python3 app.py     # http://127.0.0.1:5001
```

## Deploy (Render)

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --timeout 240` (image generation takes longer than the 30-second default)
- Environment variable: `OPENAI_API_KEY`. The key is never committed, because `.env` is in `.gitignore`.

## Testing

Final outputs (label JSON, image prompt and image) are in `docs/examples/`:

- a dead AA battery, dented at the negative end (from the bank)
- a single blue sock with a hole in the heel (from the bank)
- a crumpled dépanneur receipt (from the bank)

Earlier versions were also tested with a tangled phone charger, a half-eaten granola bar, a dried-out marker and house keys on a red carabiner. I also tested the full form submission end to end with "a dried-out marker".

## Process: challenges and fixes

- **Every work went on a plinth.** I added a `display` field with clear rules for when to use each setting.
- **"Dimensions variable" was never used.** The tangled charger got "17.0 x 12.0 x 5.0 cm (approximate)". Making the rule explicit ("no fixed shape → Dimensions variable → floor or suspended") fixed it, and the charger now lies spread across the gallery floor.
- **The plain sentence was always "It is a [object]." at the end.** Asking for a mundane fact in the middle of the text makes it interrupt the register, which is funnier.
- **The image model drew fake, garbled text** on the wall label in the picture. The prompt now says "no text".
- **Markdown italics** (`_Title_`) appeared in the label. I added a plain-text rule.
- **Artist names borrowed famous surnames** (e.g. Pirandello). This is covered by the no-real-people rule.
- **Simplicity.** An earlier version had separate API endpoints, retry loops and extra UI. I cut it back to one form, one route and two API calls.

## Reflection

The label works when the model looks at the object closely. The jargon is easy to produce, so the precise physical details ("the inward dent at the negative end", "the raised positive nub") carry the comedy. Linking the image prompt to the label instead of the raw description makes the picture show the *artwork*: its title, scale and installation, not just the object.

**Why is a language model so fluent in this dialect?** IAE is extremely formulaic: a small vocabulary of prefixes, nominalisations and critical verbs, recombined in predictable ways. Language models learn exactly that kind of statistical pattern. Rule and Levine traced IAE through e-flux press releases, which reach tens of thousands of readers and were published openly online for years, so the dialect is heavily represented in training data. IAE is also a register in which sounding right matters more than meaning something specific, and that is the thing a language model does by default. The difficult part is the opposite: making the model stay accurate about a dead battery.

## Reference

Rule, Alix, and David Levine. 2012. "International Art English." *Triple Canopy*, no. 16.
