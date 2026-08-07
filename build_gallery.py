from pathlib import Path
from PIL import Image, ImageOps

# ==========================================================
# CONFIGURATION
# ==========================================================

ORIGINALS = Path(r"D:\Dear Gauri Originals")

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
# CREATE OUTPUT FOLDERS
# ==========================================================

GALLERY.mkdir(parents=True, exist_ok=True)
THUMBS.mkdir(parents=True, exist_ok=True)

# ==========================================================
# CATEGORY TITLES
# ==========================================================

CATEGORY_NAMES = {

    "together": "❤️ Together",

    "her": "🌸 Just You"

}

# ==========================================================
# IMAGE OPTIMIZER
# ==========================================================

processed = 0
skipped = 0
failed = 0


def optimize_image(source, gallery_dest, thumb_dest):

    global processed
    global skipped
    global failed

    if gallery_dest.exists() and thumb_dest.exists():

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
            gallery_dest,
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
            thumb_dest,
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
# PROCESS CATEGORIES
# ==========================================================

print("\nOptimizing images...\n")

sections_html = ""

for category in sorted(ORIGINALS.iterdir()):

    if not category.is_dir():

        continue

    category_name = category.name.lower()

    gallery_folder = GALLERY / category_name
    thumb_folder = THUMBS / category_name

    gallery_folder.mkdir(parents=True, exist_ok=True)
    thumb_folder.mkdir(parents=True, exist_ok=True)

    for image in sorted(category.iterdir()):

        if image.suffix.lower() not in SUPPORTED:

            continue

        optimize_image(
            image,
            gallery_folder / image.name,
            thumb_folder / image.name
        )

    images = sorted(gallery_folder.iterdir())

    gallery_items = ""

    for image in images:

        gallery_items += f"""
        <a href="../assets/gallery/{category_name}/{image.name}"
           class="gallery-item"
           target="_blank">

            <img
                src="../assets/thumbs/{category_name}/{image.name}"
                alt="{image.stem}"
                loading="lazy">

        </a>
"""

    title = CATEGORY_NAMES.get(
        category_name,
        category.name.replace("_", " ").title()
    )

    sections_html += f"""

<section class="gallery-section">

    <div class="gallery-heading">

        <h2>{title}</h2>

        <p>{len(images)} memories</p>

    </div>

    <div class="gallery-grid">

        {gallery_items}

    </div>

</section>

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

Every photograph has a story.

</p>

</div>

{sections_html}

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
# WRITE GALLERY PAGE
# ==========================================================

OUTPUT_HTML.write_text(
    html,
    encoding="utf-8"
)

# ==========================================================
# CLEAN OLD FILES
# Removes optimized images that no longer exist
# ==========================================================

print("\nCleaning old optimized images...\n")

for folder in sorted(GALLERY.iterdir()):

    if not folder.is_dir():
        continue

    original_folder = ORIGINALS / folder.name

    if not original_folder.exists():
        continue

    originals = {f.name for f in original_folder.iterdir() if f.is_file()}

    # -------- Gallery --------

    for image in folder.iterdir():

        if image.name not in originals:

            image.unlink()

            print("Removed:", image)

    # -------- Thumbnails --------

    thumb_folder = THUMBS / folder.name

    for thumb in thumb_folder.iterdir():

        if thumb.name not in originals:

            thumb.unlink()

            print("Removed:", thumb)

# ==========================================================
# SUMMARY
# ==========================================================

gallery_count = sum(
    len(list(folder.iterdir()))
    for folder in GALLERY.iterdir()
    if folder.is_dir()
)

thumb_count = sum(
    len(list(folder.iterdir()))
    for folder in THUMBS.iterdir()
    if folder.is_dir()
)

gallery_size = sum(
    f.stat().st_size
    for folder in GALLERY.iterdir()
    if folder.is_dir()
    for f in folder.iterdir()
) / (1024 * 1024)

thumb_size = sum(
    f.stat().st_size
    for folder in THUMBS.iterdir()
    if folder.is_dir()
    for f in folder.iterdir()
) / (1024 * 1024)

print("\n" + "=" * 60)

print("Gallery successfully built!")

print("=" * 60)

print(f"Processed : {processed}")
print(f"Skipped   : {skipped}")
print(f"Failed    : {failed}")

print()

print(f"Gallery Images : {gallery_count}")
print(f"Thumbnails     : {thumb_count}")

print()

print(f"Gallery Size : {gallery_size:.2f} MB")
print(f"Thumb Size   : {thumb_size:.2f} MB")

print()

print(f"Output HTML : {OUTPUT_HTML}")

print("=" * 60)