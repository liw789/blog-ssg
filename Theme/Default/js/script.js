// Get the header element
const header = document.getElementById("title-bar");

// The point at which the header starts to scroll (in pixels)
const scrollPoint = 200; // Adjust this value as needed

// Add a scroll event listener
window.addEventListener("scroll", function() {
    if (window.scrollY > scrollPoint) {
        // When the user scrolls down past the scroll point, make the header scroll with the page
        header.style.position = "absolute";
        header.style.top = "200px"; // Keep the header's position relative to the scroll
    } else {
        // When the user scrolls back up, keep the header fixed at the top
        header.style.position = "fixed";
        header.style.top = "0"; // Ensure it stays at the top when fixed
    }
});
