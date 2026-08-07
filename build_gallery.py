from pathlib import Path
from PIL import Image, ImageOps

# ==========================================================
# CONFIGURATION
# ==========================================================

# Folder containing ORIGINAL photos (outside project)

ORIGINALS = Path(r"D:\Dear Gauri Originals")

# Website folders

GALLERY = Path("assets/gallery")
THUMBS = Path("assets/thumbs")

# Output pages

OUTPUT_HOME = Path("pages/gallery.html")
OUTPUT_FOLDER = Path("pages/gallery")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

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
# CATEGORY TITLES
# ==========================================================

CATEGORY_INFO = {

    "together": {

        "title": "❤️ Together",

        "subtitle": "Every moment we created together."

    },

    "her": {

        "title": "🌸 Just You",

        "subtitle": "The smile I'll always remember."

    }

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

# Stores HTML for every category page

category_pages = []

# ==========================================================
# IMAGE OPTIMIZER
# ==========================================================

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

        print(f"Failed : {source.name}")

        print(e)

# ==========================================================
# START PROCESSING
# ==========================================================

print("\nOptimizing images...\n")

categories = []

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

    categories.append({

        "name": category_name,

        "gallery": gallery_folder,

        "thumbs": thumb_folder,

        "images": sorted(gallery_folder.iterdir())

    })

    # ==========================================================
# GENERATE CATEGORY PAGES
# ==========================================================

for category in categories:

    name = category["name"]

    info = CATEGORY_INFO.get(
        name,
        {
            "title": name.replace("_", " ").title(),
            "subtitle": ""
        }
    )

    gallery_items = ""

    for image in category["images"]:

        gallery_items += f"""
        <a href="../../assets/gallery/{name}/{image.name}"
           class="gallery-item"
           target="_blank">

            <img
                src="../../assets/thumbs/{name}/{image.name}"
                alt="{image.stem}"
                loading="lazy">

        </a>
"""

    html = f"""<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{info["title"]} | Archive</title>

<link rel="preconnect"
href="https://fonts.googleapis.com">

<link rel="preconnect"
href="https://fonts.gstatic.com"
crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap"
rel="stylesheet">

<link rel="stylesheet"
href="../../style.css">

<script src="https://unpkg.com/lucide@latest"></script>

</head>

<body>

<nav class="page-nav">

<a href="../gallery.html"
class="back-link">

<i data-lucide="arrow-left"></i>

Back to Gallery

</a>

</nav>

<main class="page fade-up">

<div class="page-title">

<h1>

{info["title"]}

</h1>

<p>

{info["subtitle"]}

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

<script src="../../script.js"></script>

</body>

</html>
"""

    (OUTPUT_FOLDER / f"{name}.html").write_text(
        html,
        encoding="utf-8"
    )

    # ==========================================================
# GENERATE GALLERY HOME PAGE
# ==========================================================

cards = ""

for category in categories:

    name = category["name"]

    info = CATEGORY_INFO.get(
        name,
        {
            "title": name.replace("_", " ").title(),
            "subtitle": ""
        }
    )

    cards += f"""
    <a href="gallery/{name}.html"
       class="gallery-category-card">

        <div class="gallery-category-icon">

            {info["title"].split()[0]}

        </div>

        <h2>

            {" ".join(info["title"].split()[1:])}

        </h2>

        <p>

            {len(category["images"])} memories

        </p>

        <span class="gallery-open">

            View Collection →

        </span>

    </a>
"""

home_html = f"""<!DOCTYPE html>

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

<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap"
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

Choose a collection.

</p>

</div>

<div class="gallery-home">

{cards}

</div>

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

OUTPUT_HOME.write_text(
    home_html,
    encoding="utf-8"
)

# ==========================================================
# REMOVE OLD OPTIMIZED FILES
# ==========================================================

print("\nCleaning old optimized images...\n")

for category in categories:

    name = category["name"]

    original_folder = ORIGINALS / name
    gallery_folder = GALLERY / name
    thumb_folder = THUMBS / name

    originals = {
        f.name
        for f in original_folder.iterdir()
        if f.is_file()
    }

    for image in list(gallery_folder.iterdir()):

        if image.name not in originals:

            image.unlink()

            print("Removed:", image)

    for thumb in list(thumb_folder.iterdir()):

        if thumb.name not in originals:

            thumb.unlink()

            print("Removed:", thumb)

# ==========================================================
# SUMMARY
# ==========================================================

gallery_count = sum(
    len(category["images"])
    for category in categories
)

gallery_size = sum(
    f.stat().st_size
    for category in categories
    for f in (GALLERY / category["name"]).iterdir()
) / (1024 * 1024)

thumb_size = sum(
    f.stat().st_size
    for category in categories
    for f in (THUMBS / category["name"]).iterdir()
) / (1024 * 1024)

print()
print("=" * 60)
print("Gallery build complete!")
print("=" * 60)

print(f"Categories : {len(categories)}")
print(f"Images     : {gallery_count}")
print(f"Processed  : {processed}")
print(f"Skipped    : {skipped}")
print(f"Failed     : {failed}")

print()
print(f"Gallery Size : {gallery_size:.2f} MB")
print(f"Thumb Size   : {thumb_size:.2f} MB")

print()
print(f"Home Page : {OUTPUT_HOME}")

for category in categories:

    print(f"Created : {OUTPUT_FOLDER / (category['name'] + '.html')}")

print("=" * 60)