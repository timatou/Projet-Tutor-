// ------------------------------
// GESTION DES FORMULAIRES
// ------------------------------

// Fonction pour ouvrir / fermer les formulaires d'ajout
const formsToggle = [
  { btn: "btn-add-note", form: "form-note" },
  { btn: "btn-add-student", form: "form-student" },
  { btn: "btn-add-module", form: "form-module" },
  { btn: "btn-add-absence", form: "form-absence" }
];

formsToggle.forEach(({ btn, form }) => {
  const b = document.getElementById(btn);
  const f = document.getElementById(form);
  if (b && f) {
    b.addEventListener("click", () => {
      f.classList.toggle("hidden");
    });
  }
});

// ------------------------------
// VALIDATION DE FORMULAIRES
// ------------------------------
document.addEventListener("submit", function(e) {
  if (e.target.tagName === "FORM") {
    e.preventDefault();
    alert("✅ Formulaire enregistré (simulation test)");
  }
});
