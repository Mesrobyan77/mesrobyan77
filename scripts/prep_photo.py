"""Prep a portrait for ASCII conversion.

Crops head + shoulders, removes the background (the mask is kept as alpha),
boosts local contrast (CLAHE) and saves a grayscale+alpha PNG.

Usage: python scripts/prep_photo.py source-photo.jpg [out.png]
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

# ---- tunables ---------------------------------------------------------------
CROP_ASPECT = 3 / 4   # width / height of the crop, anchored to the top of the photo
CLAHE_CLIP = 2.5      # local contrast strength
MAX_SIDE = 1100       # downscale big photos (keeps memory low)
# -----------------------------------------------------------------------------

src = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("source-prepped.png")

photo = Image.open(src).convert("RGB")
h = min(photo.height, int(photo.width / CROP_ASPECT))
photo = photo.crop((0, 0, photo.width, h))
photo.thumbnail((MAX_SIDE, MAX_SIDE))

session = new_session("u2net_human_seg")  # small portrait model
alpha = np.array(remove(photo, session=session).convert("RGBA"))[..., 3]

gray = cv2.cvtColor(np.array(photo), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=(8, 8)).apply(gray)

Image.fromarray(np.dstack([gray, alpha]), "LA").save(out)
print(f"wrote {out} {photo.size}")
