/* ==========================================================
   ARCHIVE v1.0
   script.js
========================================================== */

/* =========================
   INITIALIZE ICONS
========================= */

lucide.createIcons();

/* =========================
   PAGE LOAD ANIMATION
========================= */

document.addEventListener("DOMContentLoaded", () => {

    document.body.classList.add("fade");

});

/* =========================
   SMOOTH SCROLL
========================= */

const exploreButton = document.querySelector(".explore-btn");

if (exploreButton) {

    exploreButton.addEventListener("click", function (e) {

        const target = this.getAttribute("href");

        if (target.startsWith("#")) {

            e.preventDefault();

            document.querySelector(target).scrollIntoView({

                behavior: "smooth"

            });

        }

    });

}

/* =========================
   ACTIVE PAGE
========================= */

const currentPage = window.location.pathname.split("/").pop();

document.querySelectorAll("a").forEach(link => {

    const href = link.getAttribute("href");

    if (href === currentPage) {

        link.classList.add("active");

    }

});

/* =========================
   CARD HOVER EFFECT
========================= */

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-10px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "";

    });

});

/* =========================
   IMAGE PREVIEW
   (Future Gallery)
========================= */

const galleryImages = document.querySelectorAll(".gallery-item img");

galleryImages.forEach(image => {

    image.addEventListener("click", () => {

        // Lightbox coming in v1.1

        console.log("Image clicked");

    });

});

/* =========================
   SONG BUTTON
========================= */

const playButton = document.querySelector(".song-button");

if (playButton) {

    playButton.addEventListener("click", () => {

        console.log("Song Player Coming Soon");

    });

}

/* =========================
   FUTURE FEATURES

   Search
   Timeline Animation
   Music Player
   Lightbox
   Journal Filter

========================= */

console.log("Archive v1.0 Loaded");