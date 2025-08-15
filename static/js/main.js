//  FOOTER
document.getElementById("current-year").textContent = new Date().getFullYear();
document
  .getElementById("back-to-top-btn")
  .addEventListener("click", function (e) {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
window.addEventListener("scroll", () => {
  const backToTopBtn = document.getElementById("back-to-top-btn");
  if (window.pageYOffset > 300) {
    backToTopBtn.style.opacity = "1";
    backToTopBtn.style.visibility = "visible";
  } else {
    backToTopBtn.style.opacity = "0";
    backToTopBtn.style.visibility = "hidden";
  }
});

// Form validation in Payment app
(function () {
  "use strict";

  const forms = document.querySelectorAll(".needs-validation");

  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();
