// Mobile Menu Helper
document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.getElementById("nav-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const menuIcon = navToggle.querySelector("svg:first-child");
  const closeIcon = navToggle.querySelector("svg:last-child");

  function openMenu() {
    mobileMenu.classList.remove("-translate-x-full");
    navToggle.setAttribute("aria-expanded", "true");
    menuIcon.classList.add("opacity-0");
    closeIcon.classList.remove("opacity-0");
  }

  function closeMenu() {
    mobileMenu.classList.add("-translate-x-full");
    navToggle.setAttribute("aria-expanded", "false");
    menuIcon.classList.remove("opacity-0");
    closeIcon.classList.add("opacity-0");
  }

  navToggle.addEventListener("click", function (e) {
    e.stopPropagation();
    if (mobileMenu.classList.contains("-translate-x-full")) {
      openMenu();
    } else {
      closeMenu();
    }
  });

  document.addEventListener("click", function (event) {
    if (
      !mobileMenu.contains(event.target) &&
      !navToggle.contains(event.target)
    ) {
      closeMenu();
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth >= 1024) {
      closeMenu();
    }
  });
});

// Service worker register
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/static/service-worker.js").then(
      function (registration) {
        console.log(
          "ServiceWorker registration successful with scope: ",
          registration.scope
        );
      },
      function (err) {
        console.log("ServiceWorker registration failed: ", err);
      }
    );
  });
}

// App install prompt
let deferredPrompt;

      window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault();
        deferredPrompt = e;
        // Show your custom "Add to Home Screen" button or banner here
        // For example:
        // document.getElementById('installButton').style.display = 'block';
      });

      // Function to show install prompt
      function showInstallPrompt() {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === "accepted") {
              console.log("User accepted the A2HS prompt");
            }
            deferredPrompt = null;
          });
        }
      }

// Offline sync trigger when back online
window.addEventListener("online", () => {
  navigator.serviceWorker.ready.then((swRegistration) => {
    return swRegistration.sync.register("sync-ideas");
  });
});
