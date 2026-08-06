from pathlib import Path
from PIL import Image, ImageOps
import shutil

# ==========================================================
# CONFIGURATION
# ==========================================================

ORIGINALS = Path("assets/originals")
GALLERY = Path("assets/gallery")
THUMBS = Path("assets/thumbs")
OUTPUT_HTML = Path("pages/gallery.html")

MAX_IMAGE_SIZE = 1920
THUMB_SIZE = 500

JPEG_QUALITY = 90
THUMB_QUALITY = 80

SUPPORTED = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif"
}

# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

GALLERY.mkdir(parents=True, exist_ok=True)
THUMBS.mkdir(parents=True, exist_ok=True)

# ==========================================================
# STATISTICS
# ==========================================================

processed = 0
skipped = 0
failed = 0

gallery_items = ""

# ==========================================================
# IMAGE OPTIMIZER
# ==========================================================

def optimize_image(source_path: Path):

    global processed
    global skipped
    global failed

    output_path = GALLERY / source_path.name
    thumb_path = THUMBS / source_path.name

    # Skip files already processed
    if output_path.exists() and thumb_path.exists():

        skipped += 1
        return

    try:

        image = Image.open(source_path)

        # Correct phone orientation
        image = ImageOps.exif_transpose(image)

        # Convert to RGB if necessary
        if image.mode not in ("RGB", "L"):

            image = image.convert("RGB")

        # --------------------------------------------------
        # OPTIMIZED IMAGE
        # --------------------------------------------------

        full = image.copy()

        full.thumbnail(
            (MAX_IMAGE_SIZE, MAX_IMAGE_SIZE),
            Image.Resampling.LANCZOS
        )

        full.save(
            output_path,
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True
        )

        # --------------------------------------------------
        # THUMBNAIL
        # --------------------------------------------------

        thumb = image.copy()

        thumb.thumbnail(
            (THUMB_SIZE, THUMB_SIZE),
            Image.Resampling.LANCZOS
        )

        thumb.save(
            thumb_path,
            quality=THUMB_QUALITY,
            optimize=True,
            progressive=True
        )

        processed += 1

    except Exception as e:

        failed += 1

        print(f"Failed: {source_path.name}")

        print(e)

        # ==========================================================
# PROCESS EVERY IMAGE
# ==========================================================

print("\nOptimizing images...\n")

for file in sorted(ORIGINALS.iterdir()):

    if file.suffix.lower() in SUPPORTED:

        optimize_image(file)

print("Finished image optimization.\n")

# ==========================================================
# BUILD GALLERY HTML
# ==========================================================

optimized_images = sorted(GALLERY.iterdir())

for image in optimized_images:

    thumb = THUMBS / image.name

    gallery_items += f"""
    <a href="../assets/gallery/{image.name}"
       class="gallery-item"
       target="_blank">

        <img
            src="../assets/thumbs/{thumb.name}"
            alt="{image.stem}"
            loading="lazy">

    </a>
"""

# ==========================================================
# COMPLETE HTML PAGE
# ==========================================================

html = f"""<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Gallery | Archive</title>

<link rel="preconnect"
href="https://fonts.googleapis.com">

<link rel="preconnect"
href="https://fonts.gstatic.com"
crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap"
rel="stylesheet">

<link rel="stylesheet"
href="../style.css">

<script src="https://unpkg.com/lucide@latest"></script>

</head>

<body>

<nav class="page-nav">

<a href="../index.html"
class="back-link">

<i data-lucide="arrow-left"></i>

Back to Archive

</a>

</nav>

<main class="page fade-up">

<div class="page-title">

<h1>

Gallery

</h1>

<p>

{len(optimized_images)} memories preserved.

</p>

</div>

<section class="gallery-grid">

{gallery_items}

</section>

</main>

<footer>

<h3>

Archive

</h3>

<p>

Every memory has a place.

</p>

</footer>

<script>

lucide.createIcons();

</script>

<script src="../script.js"></script>

</body>

</html>
"""