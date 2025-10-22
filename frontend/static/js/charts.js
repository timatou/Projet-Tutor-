// ------------------------------
// DASHBOARD - Moyenne par module
// ------------------------------
const chart1 = document.getElementById('chartGlobal');
if (chart1) {
  new Chart(chart1, {
    type: 'bar',
    data: {
      labels: ['Algo', 'BD', 'Réseaux'],
      datasets: [{
        label: 'Moyenne par module',
        data: [12, 14, 10],
        backgroundColor: ['#3498db', '#e67e22', '#2ecc71']
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true, max: 20 } }
    }
  });
}

// ------------------------------
// ABSENCES - Justifiées / Non justifiées
// ------------------------------
const chart2 = document.getElementById('chartAbsences');
if (chart2) {
  new Chart(chart2, {
    type: 'pie',
    data: {
      labels: ['Justifiées', 'Non justifiées'],
      datasets: [{
        data: [65, 35],
        backgroundColor: ['#2ecc71', '#e74c3c']
      }]
    },
    options: {
      responsive: true
    }
  });
}
