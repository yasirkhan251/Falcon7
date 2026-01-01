
    // Mobile Menu Toggle
    const menuBtn = document.getElementById("menu-btn");
    const nav = document.getElementById("nav");

    menuBtn.addEventListener("click", () => {
      nav.classList.toggle("open");
      menuBtn.classList.toggle("open"); // Hamburger transforms to X
    });

    // Theme Toggle
    const themeToggle = document.getElementById("theme-toggle");
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (savedTheme) {
      document.documentElement.setAttribute("data-theme", savedTheme);
      themeToggle.textContent = savedTheme === "dark" ? "☀️" : "🌙";
    } else if (prefersDark) {
      document.documentElement.setAttribute("data-theme", "dark");
      themeToggle.textContent = "☀️";
    }

    themeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
      themeToggle.textContent = newTheme === "dark" ? "☀️" : "🌙";
    });
  

  // Smooth Scroll Implementation
function smoothScroll(target, duration) {
    const element = document.querySelector(target);
    const startPosition = window.pageYOffset;
    const targetPosition = element.getBoundingClientRect().top;
    const startTime = performance.now();

    function animation(currentTime) {
        const elapsed = currentTime - startTime;
        const ease = easeInOutQuad(elapsed, startPosition, targetPosition, duration);

        window.scrollTo(0, ease);

        if (elapsed < duration) requestAnimationFrame(animation);
    }

    function easeInOutQuad(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return (c / 2) * t * t + b;
        t--;
        return (-c / 2) * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

// Attach to link
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("a[href='#category-section']").onclick = function (e) {
        e.preventDefault();
        smoothScroll('#category-section', 500);  // ← change 500ms to slower/faster
    };
});

