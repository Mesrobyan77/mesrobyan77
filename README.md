# Khachik Mesrobyan — Animated GitHub Profile

My GitHub profile is built from a few small Python scripts and self-contained SVGs: a monochrome ASCII portrait that types itself in, a terminal-style info card, and a contribution heatmap that animates into view and refreshes daily.

The README only embeds the SVGs. All motion lives inside the SVG files, using SVG animation and CSS keyframes rather than JavaScript.

## What’s in this repository

- `avi-ascii.svg` — a photo converted to monochrome ASCII art, revealed one row at a time.
- `info-card.svg` — a neofetch-inspired card with my profile, stack, and contact details.
- `contrib-heatmap.svg` — a 53-week contribution calendar with contribution totals and streaks.
- `scripts/` — scripts to prepare the portrait, generate the card, fetch contribution data, and render the heatmap.
- `data/contributions.json` — the contribution data used to render the heatmap.
- `.github/workflows/update-profile-art.yml` — a scheduled workflow that refreshes the heatmap daily.

## Requirements

Use Python 3. The contribution workflow needs only `requests` and `beautifulsoup4`; the additional packages in `scripts/requirements.txt` are for the local portrait pipeline.

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r scripts/requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`.

## Generate the portrait

The portrait pipeline has two stages. First, prepare a local photo by cropping it, removing its background, and applying local contrast. The photo and generated intermediate image are excluded by `.gitignore`.

```powershell
python scripts/prep_photo.py source-photo.jpg
```

Then convert the prepared grayscale image into the animated SVG:

```powershell
python scripts/make_ascii_svg.py
```

By default, this reads `source-prepped.png` and writes `avi-ascii.svg`. Set `STATIC=1` to generate a non-animated preview; `COLS` controls the character-grid width.

## Generate the info card

The content for the card is defined near the top of `scripts/make_info_card.py`. Update the sections there when your profile details change, then run:

```powershell
python scripts/make_info_card.py
```

This writes `info-card.svg`. Set `STATIC=1` for a frozen preview.

## Refresh the contribution heatmap

The fetch script reads GitHub’s public contribution calendar, so it does not need a personal access token. It writes the daily counts and derived statistics to `data/contributions.json`.

```powershell
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

`GH_USER` optionally selects the GitHub account to fetch; the default is `mesrobyan77`. The renderer writes `contrib-heatmap.svg`, including the calendar, contribution total, current and longest streaks, best day, and color legend.

## Add the artwork to a profile README

To display the artwork on your GitHub profile, embed the heatmap above the portrait and info card. A table keeps the two lower images side by side on GitHub:

```html
<img src="./contrib-heatmap.svg" width="860" alt="Contribution heatmap" />

<table>
  <tr>
    <td valign="top"><img src="./avi-ascii.svg" width="420" alt="ASCII portrait" /></td>
    <td valign="top"><img src="./info-card.svg" width="440" alt="Profile info card" /></td>
  </tr>
</table>
```

The heatmap is 860 pixels wide, matching the combined 420-pixel and 440-pixel columns.

## Daily automation

The GitHub Actions workflow runs every day at 06:17 UTC and can also be started manually from the Actions tab. It fetches the public contribution calendar, renders the SVG, and commits the refreshed data and image. Its permissions include `contents: write` so the workflow can push its update.

The workflow installs only the two packages needed for fetching contributions; it does not install the portrait-only image-processing dependencies.

## Notes

- The contribution fetcher depends on GitHub’s public calendar HTML. It fails if GitHub returns an error or the expected contribution cells are missing.
- GitHub sanitizes scripts and much inline styling in README content. Embedding SVG files as images keeps the animation self-contained and avoids JavaScript in the README.
- Portrait input and generated intermediate files are ignored; do not commit a personal source photo unless you intend to publish it.
