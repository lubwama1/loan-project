//  LOAN APPLICATION
document.addEventListener("DOMContentLoaded", function () {
  // Form elements
  const step1 = document.getElementById("step1");
  const step2 = document.getElementById("step2");
  const step3 = document.getElementById("step3");
  const progressBar = document.getElementById("progress-bar");
  const currentStep = document.getElementById("current-step");
  const form = document.getElementById("loanForm");

  // Navigation buttons
  const nextBtn = document.getElementById("nextBtn");
  const middleBtn = document.getElementById("middleBtn");
  const backBtn = document.getElementById("backBtn");
  const step3BackBtn = document.getElementById("step3BackBtn");

  // Terms and submit
  const termsCheckbox = document.getElementById("terms");
  const submitBtn = document.getElementById("submitBtn");

  // Check if required elements exist
  if (!step1 || !step2 || !step3 || !progressBar || !currentStep || !form) {
    console.error("One or more required form elements are missing");
    return;
  }

  // Check for saved step in localStorage
  const savedStep = localStorage.getItem("loanApplicationStep");
  const initialStep = savedStep || "1";

  // Initialize form steps
  function initializeStep() {
    [step1, step2, step3].forEach((step) => step.classList.remove("active"));

    // Show the appropriate step
    if (initialStep === "1") {
      step1.classList.add("active");
      currentStep.textContent = "1";
      progressBar.style.width = "33%";
    } else if (initialStep === "2") {
      step2.classList.add("active");
      currentStep.textContent = "2";
      progressBar.style.width = "66%";
    } else {
      step3.classList.add("active");
      currentStep.textContent = "3";
      progressBar.style.width = "100%";
    }
  }

  // Validate current step before proceeding
  function validateStep(step) {
    if (step === 1) {
      const requiredFields = [
        document.getElementById("id_first_name"),
        document.getElementById("id_last_name"),
        document.getElementById("id_email"),
        document.getElementById("id_phone_number"),
      ];

      return requiredFields.every(
        (field) => field && field.value.trim() !== ""
      );
    } else if (step === 2) {
      const amountField = document.getElementById("id_amount");
      const purposeField = document.getElementById("id_purpose");

      return (
        amountField &&
        amountField.value.trim() !== "" &&
        purposeField &&
        purposeField.value.trim() !== ""
      );
    }
    return true;
  }

  // Navigation handlers
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      if (validateStep(1)) {
        step1.classList.remove("active");
        step2.classList.add("active");
        currentStep.textContent = "2";
        progressBar.style.width = "66%";
        localStorage.setItem("loanApplicationStep", "2");
      } else {
        alert("Please fill in all required fields before proceeding.");
      }
    });
  }

  if (middleBtn) {
    middleBtn.addEventListener("click", () => {
      if (validateStep(2)) {
        step2.classList.remove("active");
        step3.classList.add("active");
        currentStep.textContent = "3";
        progressBar.style.width = "100%";
        localStorage.setItem("loanApplicationStep", "3");
      } else {
        alert("Please fill in all required fields before proceeding.");
      }
    });
  }

  if (backBtn) {
    backBtn.addEventListener("click", () => {
      step2.classList.remove("active");
      step1.classList.add("active");
      currentStep.textContent = "1";
      progressBar.style.width = "33%";
      localStorage.setItem("loanApplicationStep", "1");
    });
  }

  if (step3BackBtn) {
    step3BackBtn.addEventListener("click", () => {
      step3.classList.remove("active");
      step2.classList.add("active");
      currentStep.textContent = "2";
      progressBar.style.width = "66%";
      localStorage.setItem("loanApplicationStep", "2");
    });
  }

  if (termsCheckbox && submitBtn) {
    termsCheckbox.addEventListener("change", function () {
      submitBtn.disabled = !this.checked;
      if (!this.checked) {
        alert("Please accept the terms and conditions to proceed.");
      }
    });
  }

  if (form) {
    form.addEventListener("submit", function () {
      localStorage.removeItem("loanApplicationStep");
    });
  }

  // Initialize the form
  initializeStep();
});
