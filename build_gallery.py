from pathlib import Path
from PIL import Image, ImageOps

# ==========================================================
# CONFIGURATION
# ==========================================================

# Folder containing your ORIGINAL full-quality photos.
# This can be anywhere on your computer.

ORIGINALS = Path(r"D:\originals")

# Output folders (inside website)

GALLERY = Path("assets/gallery")
THUMBS = Path("assets/thumbs")

# Gallery page

OUTPUT_HTML = Path("pages/gallery.html")

# ==========================================================
# IMAGE SETTINGS
# ==========================================================

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
# CREATE OUTPUT FOLDERS
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
# OPTIMIZE SINGLE IMAGE
# ==========================================================

def optimize_image(source: Path):

    global processed
    global skipped
    global failed

    gallery_file = GALLERY / source.name
    thumb_file = THUMBS / source.name

    if gallery_file.exists() and thumb_file.exists():

        skipped += 1
        return

    try:

        image = Image.open(source)

        image = ImageOps.exif_transpose(image)

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
            gallery_file,
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
            thumb_file,
            quality=THUMB_QUALITY,
            optimize=True,
            progressive=True
        )

        processed += 1

    except Exception as e:

        failed += 1

        print(f"Failed: {source.name}")

        print(e)

# ==========================================================
# PROCESS ALL IMAGES
# ==========================================================

print("\nOptimizing images...\n")

for file in sorted(ORIGINALS.iterdir()):

    if file.suffix.lower() in SUPPORTED:

        optimize_image(file)

print("\nFinished optimizing images.\n")
print(f"Processed : {processed}")
print(f"Skipped   : {skipped}")
print(f"Failed    : {failed}")

# ==========================================================
# BUILD GALLERY HTML
# ==========================================================

optimized_images = sorted(GALLERY.iterdir())

gallery_items = ""

for image in optimized_images:

    gallery_items += f"""
    <a href="../assets/gallery/{image.name}"
       class="gallery-item"
       target="_blank">

        <img
            src="../assets/thumbs/{image.name}"
            alt="{image.stem}"
            loading="lazy">

    </a>
"""

    # ==========================================================
# GENERATE HTML
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

# ==========================================================
# WRITE HTML FILE
# ==========================================================

OUTPUT_HTML.write_text(
    html,
    encoding="utf-8"
)

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("=" * 60)
print("Gallery successfully generated!")
print("=" * 60)

print(f"Gallery HTML : {OUTPUT_HTML}")
print(f"Images       : {len(optimized_images)}")
print(f"Processed    : {processed}")
print(f"Skipped      : {skipped}")
print(f"Failed       : {failed}")

gallery_size = sum(f.stat().st_size for f in GALLERY.iterdir()) / (1024 * 1024)
thumb_size = sum(f.stat().st_size for f in THUMBS.iterdir()) / (1024 * 1024)

print(f"Gallery Size : {gallery_size:.2f} MB")
print(f"Thumb Size   : {thumb_size:.2f} MB")

print("=" * 60)