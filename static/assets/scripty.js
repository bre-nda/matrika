document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded"); // Debugging line

    const title = document.getElementById("about-title");
    
    if (!title) {
        console.error("Element with ID 'about-title' not found.");
        return;
    }

    function checkScroll() {
        const rect = title.getBoundingClientRect();
        
        if (rect.top < window.innerHeight * 0.75 && !title.classList.contains("show")) {
            console.log("Adding 'show' class to the title");
            title.classList.add("show");
            window.removeEventListener("scroll", checkScroll); // Ensures it runs only once
        }
    }

    window.addEventListener("scroll", checkScroll);
});