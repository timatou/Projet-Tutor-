let myChart;
const BASE_URL = "/statistique/";

//////////////////////////////////////////////////////
// 🔥 CONSTRUCTION URL
//////////////////////////////////////////////////////
function buildURL() {
    const params = new URLSearchParams();
    const fields = {
        'module_id': 'filter-module',
        'groupe_id': 'filter-groupe',
        'etudiant_id': 'filter-etudiant',
        'promotion_id': 'filter-promotion'
    };

    for (const [param, id] of Object.entries(fields)) {
        const val = document.getElementById(id).value;
        if (val) params.append(param, val);
    }
    return `${BASE_URL}api/globales/?${params.toString()}`;
}

//////////////////////////////////////////////////////
// 📊 UPDATE CHART
//////////////////////////////////////////////////////
function updateChart(url) {
    fetch(url)
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('myChart').getContext('2d');
            if (myChart) myChart.destroy();

            let labels = data.labels || [];
            let values = data.moyennes || [];

            if (!labels.length) {
                labels = ["Aucune donnée"];
                values = [0];
            }

            const etudiant = document.getElementById('filter-etudiant').value;
            let labelTag = "Moyenne globale";

            if (etudiant) labelTag = `Stats de ${data.identite || 'l\'étudiant'}`;
            else if (document.getElementById('filter-groupe').value) labelTag = "Moyennes du groupe";
            else if (document.getElementById('filter-promotion').value) labelTag = "Moyennes de la promotion";

            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: labelTag,
                        data: values,
                        backgroundColor: values.map(v => v >= 10 ? 'rgba(54, 162, 235, 0.7)' : 'rgba(255, 99, 132, 0.7)')
                    }]
                },
                options: { 
                    responsive: true, 
                    scales: { y: { beginAtZero: true, max: 20 } } 
                }
            });
        })
        .catch(err => console.error("Erreur Chart:", err));
}

//////////////////////////////////////////////////////
// 🎯 CHARGEMENT DYNAMIQUE
//////////////////////////////////////////////////////

function loadGroupes(promotionId) {
    const groupeSelect = document.getElementById('filter-groupe');
    groupeSelect.innerHTML = `<option value="">Tous les groupes</option>`;
    
    if (!promotionId) return;

    fetch(`${BASE_URL}api/groupes/?promotion_id=${promotionId}`)
        .then(res => res.json())
        .then(data => {
            data.groupes.forEach(g => {
                groupeSelect.innerHTML += `<option value="${g.id}">${g.nom}</option>`;
            });
        });
}

/**
 * Charge les étudiants selon la promo ET/OU le groupe
 */
function loadEtudiants(promotionId, groupeId) {
    const etudiantSelect = document.getElementById('filter-etudiant');
    etudiantSelect.innerHTML = `<option value="">Choisir un étudiant...</option>`;

    // On construit l'URL de recherche
    let query = new URLSearchParams();
    if (promotionId) query.append('promotion_id', promotionId);
    if (groupeId) query.append('groupe_id', groupeId);

    if (query.toString() === "") return;

    fetch(`${BASE_URL}api/etudiants/?${query.toString()}`) 
        .then(res => res.json())
        .then(data => {
            if (data.etudiants) {
                data.etudiants.forEach(e => {
                    etudiantSelect.innerHTML += `<option value="${e.id}">${e.nom}</option>`;
                });
            }
        })
        .catch(err => console.error("Erreur LoadEtudiants:", err));
}

//////////////////////////////////////////////////////
// 🎯 EVENTS
//////////////////////////////////////////////////////

// 🎓 Changement de Promotion
document.getElementById('filter-promotion').addEventListener('change', function () {
    const promotionId = this.value;

    // Reset des menus dépendants
    document.getElementById('filter-groupe').value = "";
    
    // 1. Recharge les groupes de cette promo
    loadGroupes(promotionId);
    
    // 2. Recharge TOUS les étudiants de cette promo
    loadEtudiants(promotionId, null);

    updateChart(buildURL());
});

// 👥 Changement de Groupe
document.getElementById('filter-groupe').addEventListener('change', function () {
    const promotionId = document.getElementById('filter-promotion').value;
    const groupeId = this.value;

    // Recharge les étudiants filtrés par le groupe sélectionné
    loadEtudiants(promotionId, groupeId);

    updateChart(buildURL());
});

// 👤 Changement d'Étudiant
document.getElementById('filter-etudiant').addEventListener('change', function () {
    updateChart(buildURL());
});

// 📚 Changement de Module
document.getElementById('filter-module').addEventListener('change', function () {
    updateChart(buildURL());
});

// Initialisation
document.addEventListener("DOMContentLoaded", () => updateChart(buildURL()));