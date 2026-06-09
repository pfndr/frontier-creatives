# Evolving Agentic Workflows

A lightning-talk deck for **Frontier Creatives · Pioneer Square Labs · Jun 9, 2026**.

Built by [Marc Krejci](mailto:marc@pfndr.co) at [Pathfinder Foundry](https://protovibing.ai). The talk traces how design thinking keeps evolving, why jumping straight to a vibe-coded "solution" is a trap, and how a validation loop (ProtoVibing) lets one person take an idea to a validated prototype. *Design thinking, rebuilt for agents.*

It is a single self-contained HTML file (React via Babel standalone, no build step), keyboard-driven for clean projector use, with a live `protovibing.ai` demo and a `prebeta.club` close.

---

## Quick start

Double-click `index.html`, or drag it into any modern browser. No build step, no server required.

For the best experience (the embedded live sites and the fullscreen browser overlay behave best over a real origin), serve locally:

```bash
cd frontier-creatives
python3 -m http.server 8000
# then open http://localhost:8000
```

**Keyboard:** `→` / `Space` advances, `←` goes back, `Home` / `End` jump to the first/last slide. Toggle light/dark and fullscreen from the top-right. A `.png`/`.jpeg` set under `images/` powers the diagrams, headshot, and screenshot fallbacks.

---

## Deploy to GitHub Pages

This deck is a static site, so Pages can serve it as-is. Every asset path is relative (`images/...`, `styles.css`, `./og-image.png`), so it works at any base URL.

1. Put the **contents of this `frontier-creatives` folder** at the root of a repo (or in a `/docs` folder of one).
2. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, then pick `main` and `/ (root)` (or `/docs`).
3. The deck goes live at `https://<user>.github.io/<repo>/`.

Notes:
- A `.nojekyll` file is not required here (no asset paths begin with an underscore). Add an empty one only if that changes.
- The social preview uses a **relative** `og:image` (`./og-image.png`), which most crawlers resolve. For the richest previews on Slack and iMessage, swap `og:image` and `twitter:image` in `index.html` to the **absolute** URL once you know it, for example `https://<user>.github.io/<repo>/og-image.png`.

---

## Deck structure (10 slides)

| #  | Slide | What it covers |
|----|-------|----------------|
| 1  | Title | Evolving Agentic Workflows. Hook, eyebrow, headshot. |
| 2  | The Shift | Reach (1:1 → 1:Few → 1:Many) vs. builders it takes (solo → full XFN), with 2016 vs 2026 markers. |
| 3  | The Lineage | Design has always been a loop: Double Diamond, Stingray, ProtoVibing. |
| 4  | The Trap | Vibe-coding fantasy vs reality, plus the over-building proof ($29.5B / only 6.4% used). |
| 5  | The Loop | The ProtoVibing loop: Idea, Plan, Create, Test, then synthesize and repeat. |
| 6  | The Build | The Human-Driven Agentic Flywheel: custom GPTs, then a Claude skill, then the product. |
| 7  | Live Demo | Embedded `protovibing.ai` project (screenshot fallback if framing is blocked). |
| 8  | The Mindset | Gardening, Not Architecture. Iterate and throw away the bad ideas. |
| 9  | Maven | "Join the Cohort" CTA. PMF Without Guessing, promo code PROTOVIBING, starts July 29. |
| 10 | Closing | Open invitation, with `prebeta.club` embedded live. |

Speaker notes for every slide live in [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) (kept out of the deck so the file stays lean).

---

## Embedded sites and screenshot fallback

The Live Demo and Closing slides embed real sites in a browser-chrome card. Some sites (claude.ai, app dashboards) send framing headers that block iframes, so those cards use a **screenshot mode**: the card shows a captured image and the chrome's "open in new tab" button (or a click) goes to the live site. The screenshots live in `images/`:

- `images/therapist-buddy.png` (the demo project)
- `images/demo-agent.png`, `images/preview-setup.png` (the build-step links)

If a card shows a "Screenshot not found" panel, drop the named PNG into `images/`.

---

## Regenerating the social image

`og-image.png` (1200x630) is generated from `scripts/build-og-image.py` using Pillow, composited from `images/bkg.png` and the headshot with the Pathfinder lockup, headline, and tagline.

```bash
cd frontier-creatives
python3 -m pip install pillow   # if needed
python3 scripts/build-og-image.py
```

Edit the headline, eyebrow, tagline, date, or colors near the top and in `build()` of that script, then re-run.

---

## Project layout

```
frontier-creatives/
├── index.html              # The entire deck (React via Babel standalone, single file)
├── styles.css              # Base styles, background, animation keyframes
├── og-image.png            # Social share preview (1200x630)
├── README.md
├── SPEAKER_NOTES.md         # Per-slide speaker notes
├── scripts/
│   └── build-og-image.py   # Regenerates og-image.png (Pillow)
└── images/
    ├── bkg.png                              # Background texture (also used by the OG image)
    ├── MKrejci - CircleAvatar - WhiteBorder.png
    ├── logo + wordmark _ white.png
    ├── DoubleDiamond.png, StingrayModel.png, ProtoVibingLoop.png   # Lineage diagrams
    ├── MavenCohort.png                      # Maven CTA visual
    ├── live-jazz.jpeg                       # Gardening slide photo
    ├── feature-bloat.png                    # Reference for the over-building viz
    └── therapist-buddy.png, demo-agent.png, preview-setup.png      # Screenshot fallbacks
```

---

## Credits

- **Talk and slides:** Marc Krejci · [protovibing.ai](https://protovibing.ai) · [pfndr.co](https://pfndr.co)
- **Venue:** Frontier Creatives at Pioneer Square Labs
- **Stat:** Pendo, 2019 Feature Adoption Report and 2024 Product Benchmarks

For more agent tools, prompts, and the cohort, visit [protovibing.ai](https://protovibing.ai).
