# Readymade: Wall Labels for Ordinary Objects

In this assignment, you will build and deploy a web app that turns any ordinary object into a work of contemporary art. An audience member describes something from their pocket, bag, or desk. Your app uses the OpenAI API to write the object's museum label (a tombstone followed by an extended label interpreting the work) and to generate an image of the object on display in an exhibition.

## Background

Since Marcel Duchamp's _readymades_, context has been able to turn an object into art: the plinth, the lighting, the institution, and the text on the wall. That text has its own dialect. In 2012, the sociologist Alix Rule and the artist David Levine analyzed thousands of exhibition press releases sent out by e-flux, and named the dialect "International Art English" (IAE).

You know this language. You have read it on gallery walls, and you will probably write it in grant applications. In this assignment, you build a machine that speaks it fluently, and in the process you learn to see how it works.

Reading: [Rule, Alix, and David Levine. 2012. "International Art English." _Triple Canopy_, no. 16.](https://tc3.canopycanopycanopy.com/16/international_art_english)

## OpenAI API integration

Use the OpenAI API to generate wall labels for user-submitted objects, and the [OpenAI Images API](https://platform.openai.com/docs/api-reference/images) to generate images of the objects installed as artworks. The API may return images as base64 (`b64_json`), so you may need to convert them for display. Remember to not expose your OpenAI key in your code; use an environment variable instead.

## The wall label

The tombstone must include:

- **Artist:** an invented name and a bio line (e.g., "b. 1997, lives and works between Verdun and the cloud")
- **Title and year**
- **Medium:** real materials and abstractions can mix (e.g., "Polyester, elastic, fatigue")
- **Dimensions**
- **Provenance:** the object's history of ownership (e.g., "Found under a radiator, 2026; private collection of a dépanneur; acquired by the museum after a tense negotiation")
- **Insurance value**
- **Credit line** (e.g., "Gift of the artist's backpack")

The **extended label** is 80–120 words. It must cite one invented theorist and their invented book.

## Prompt design

1. **Study the dialect.** Read Rule and Levine and pick the IAE features your machine will use and exaggerate.
2. **Write the rules.** Your system prompt must define at least three explicit rules your machine always follows.
3. **Stay precise about the object.** The humour comes from the gap between an accurate description of a mundane object and the inflated language around it.
4. **Chain the image to the label.** Don't send the raw description to the image model; write the image prompt from the label itself.
   - **The label sets the scale.** If the dimensions say 600 × 400 cm, the granola bar fills the room. If they say "dimensions variable," the image should show it.
   - **Choose a curatorial setting:** a white cube, a museum vitrine, a lone plinth under a spotlight, a biennale pavilion.
5. **Don't borrow real reputations.** Invent your artists, and don't attribute work or quotes to real artists, critics, or curators. The only reputations in your gallery are the ones your machine makes up.

## User input and output

Users describe an object in a text field. Show the label and the image together the way a gallery would, with the label beside the work.

## Getting started

You can begin with the boilerplate code from [the GitHub repository used in class](https://github.com/CART-ACT/minimal-flask-app/). Test the application thoroughly, and fix any bugs before submission.

## Deliverables

### Web application

A link to a fully functional web app deployed on a suitable platform (e.g., Render, PythonAnywhere, Heroku).

### Code repository

A link to a new public GitHub repository (not the one used for previous assignments) with a commit history showing your development progress. Include a `README.md` in the root of the repository covering:

- which IAE features you chose and how you translated them into prompt rules
- how the image prompt is derived from the label
- a user guide for the web app
- a reflection on this question: why is a language model so fluent in this dialect?
