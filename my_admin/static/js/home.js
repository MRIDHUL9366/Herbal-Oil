document.addEventListener("DOMContentLoaded", function() {
    // Select the heading
    let heading = document.querySelector("h1");

    // On mouse over
    heading.addEventListener("mouseover", function() {
        heading.style.color = "red";
    });

    // On mouse out
    heading.addEventListener("mouseout", function() {
        heading.style.color = "yellow";
    });
});
