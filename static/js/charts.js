document.addEventListener("DOMContentLoaded", function () {

  // =============================
  // DASHBOARD - Moyenne globale
  // =============================
  const chartGlobal = document.getElementById("chartGlobal");
  if (chartGlobal) {
    new Chart(chartGlobal, {
      type: "bar",
      data: {
        labels: ["Algo", "BD", "Réseaux"],
        datasets: [{
          label: "Moyenne par module",
          data: [12, 14, 10],
          backgroundColor: ["#3498db", "#e67e22", "#2ecc71"]
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 20 } }
      }
    });
  }

  // =============================
  // ABSENCES - Répartition
  // =============================
  const chartAbsences = document.getElementById("chartAbsences");
  if (chartAbsences) {
    new Chart(chartAbsences, {
      type: "pie",
      data: {
        labels: ["Justifiées", "Non justifiées"],
        datasets: [{
          data: [65, 35],
          backgroundColor: ["#2ecc71", "#e74c3c"]
        }]
      }
    });
  }

  // =============================
  // STATISTIQUES - Moyenne étudiants
  // =============================
  const chartEtudiants = document.getElementById("chartEtudiants");
  if (chartEtudiants) {
    new Chart(chartEtudiants, {
      type: "bar",
      data: {
        labels: ["ET001", "ET002", "ET003", "ET004"],
        datasets: [{
          label: "Moyenne",
          data: [15, 13, 12, 16],
          backgroundColor: "#667eea"
        }]
      },
      options: {
        scales: { y: { beginAtZero: true, max: 20 } },
        plugins: { legend: { display: false } }
      }
    });
  }

});
