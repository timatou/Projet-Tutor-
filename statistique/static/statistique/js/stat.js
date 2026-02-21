let myChart;
const BASE_URL = "/statistique/";

//////////////////////////////////////////////////////
// 🔥 CONSTRUCTION URL
//////////////////////////////////////////////////////
function buildURL() {
    const module = document.getElementById('filter-module').value;
    const groupe = document.getElementById('filter-groupe').value;
    const etudiant = document.getElementById('filter-etudiant').value;

    let url = `${BASE_URL}api/globales/?`;

    if (module) url += `module_id=${module}&`;
    if (groupe) url += `groupe_id=${groupe}&`;
    if (etudiant) url += `etudiant_id=${etudiant}&`;

    return url;
}

//////////////////////////////////////////////////////
// 📊 UPDATE CHART
//////////////////////////////////////////////////////
function updateChart(url) {
    console.log("🚀 URL appelée :", url);

    const module = document.getElementById('filter-module').value;
    const groupe = document.getElementById('filter-groupe').value;
    const etudiant = document.getElementById('filter-etudiant').value;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log("✅ Données reçues :", data);

            const canvas = document.getElementById('myChart');
            if (!canvas) {
                console.error("❌ Canvas introuvable !");
                return;
            }

            const ctx = canvas.getContext('2d');

            // 🔥 Détruire ancien graphique
            if (myChart) myChart.destroy();

            let labels = data.labels || [];
            let values = data.moyennes || [];

            //////////////////////////////////////////////////////
            // 🔥 CORRECTION PRINCIPALE
            //////////////////////////////////////////////////////

            // ⚠️ Si étudiant seul → on s'assure qu'on a plusieurs modules
            if (etudiant && !module) {
                console.log("📊 Cas : étudiant seul");

                // sécurité si backend renvoie un seul élément
                if (labels.length === 1 && labels[0] === "Moyenne de l'étudiant") {
                    console.warn("⚠️ Backend ne renvoie pas les modules !");
                }
            }

            // 🔥 Si aucune donnée
            if (!labels.length) {
                labels = ["Aucune donnée"];
                values = [0];
            }

            //////////////////////////////////////////////////////
            // 🎯 LABEL DYNAMIQUE INTELLIGENT
            //////////////////////////////////////////////////////
            let labelTag = "";

            if (etudiant && module) {
                labelTag = "Moyenne de l'étudiant pour ce module";
                labels = ["Moyenne"];
            }
            else if (etudiant && !module) {
                labelTag = `Moyennes par module (${data.identite || "Étudiant"})`;
            }
            else if (!etudiant && module) {
                labelTag = "Moyennes des étudiants";
            }
            else if (groupe) {
                labelTag = "Moyennes du groupe";
            }
            else {
                labelTag = "Moyenne globale par module";
            }

            //////////////////////////////////////////////////////
            // 📊 CREATION CHART
            //////////////////////////////////////////////////////
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: labelTag,
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 20
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("❌ Erreur fetch :", error);
        });
}

//////////////////////////////////////////////////////
// 🎯 EVENTS FILTRES
//////////////////////////////////////////////////////

// 👤 Étudiant
document.getElementById('filter-etudiant').addEventListener('change', function () {
    console.log("🎯 Étudiant :", this.value);

    document.getElementById('filter-groupe').value = "";

    updateChart(buildURL());
});

// 👥 Groupe
document.getElementById('filter-groupe').addEventListener('change', function () {
    console.log("🎯 Groupe :", this.value);

    document.getElementById('filter-etudiant').value = "";

    updateChart(buildURL());
});

// 📚 Module
document.getElementById('filter-module').addEventListener('change', function () {
    console.log("🎯 Module :", this.value);

    updateChart(buildURL());
});

//////////////////////////////////////////////////////
// 🚀 INITIALISATION
//////////////////////////////////////////////////////
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Page chargée");

    updateChart(`${BASE_URL}api/globales/`);
});
