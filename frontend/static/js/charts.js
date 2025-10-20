const ctx = document.getElementById('graph');
if (ctx) {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Module A', 'Module B', 'Module C'],
      datasets: [{
        label: 'Moyenne',
        data: [12, 14, 10],
      }]
    }
  });
}
