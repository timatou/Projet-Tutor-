// stat.js - VERSION FINALE CORRIGÉE

document.addEventListener('DOMContentLoaded', function () {
    console.log("✅ DOM chargé, initialisation...");

    // ══════════════════════════════════════════════
    // VARIABLES GLOBALES
    // ══════════════════════════════════════════════
    let myChart = null;
    let distChart = null;
    const BASE_URL = "/statistique/";

    // ══════════════════════════════════════════════
    // 🔧 FONCTION CLEF : CONSTRUCTION URL AVEC FILTRES
    // ══════════════════════════════════════════════
    function buildURL() {
        const params = new URLSearchParams();
        
        // Récupérer les valeurs des filtres
        const promotionId = document.getElementById("filter-promotion")?.value || "";
        const groupeId = document.getElementById("filter-groupe")?.value || "";
        const moduleId = document.getElementById("filter-module")?.value || "";
        const etudiantId = document.getElementById("filter-etudiant")?.value || "";

        // ✅ Ajouter UNIQUEMENT si non-vide
        if (promotionId) params.append("promotion_id", promotionId);
        if (groupeId) params.append("groupe_id", groupeId);
        if (moduleId) params.append("module_id", moduleId);
        if (etudiantId) params.append("etudiant_id", etudiantId);

        const url = `${BASE_URL}api/globales/?${params.toString()}`;
        console.log("🔗 URL générée:", url);
        return url;
    }

    // ══════════════════════════════════════════════
    // 🔄 GESTION PROMOTION → GROUPE → ÉTUDIANT
    // ══════════════════════════════════════════════
    async function updateFiltersOnPromoChange() {
        const promotionId = document.getElementById("filter-promotion")?.value;
        console.log("📌 Promotion changée:", promotionId);

        // Réinitialiser les dépendants
        document.getElementById("filter-groupe").value = "";
        document.getElementById("filter-etudiant").value = "";
        document.getElementById("filter-etudiant").innerHTML = '<option value="">Choisir un étudiant...</option>';

        if (!promotionId) {
            document.getElementById("groupe-container").style.display = "none";
            document.getElementById("filter-groupe").innerHTML = '<option value="">Tous les groupes</option>';
            return;
        }

        // Charger les groupes pour cette promotion
        try {
            const response = await fetch(`${BASE_URL}api/groupes/?promotion_id=${promotionId}`);
            const data = await response.json();
            
            console.log("✅ Groupes reçus:", data.groupes);
            
            if (data.groupes && data.groupes.length > 0) {
                // Afficher le conteneur groupe
                document.getElementById("groupe-container").style.display = "block";
                
                let html = '<option value="">Tous les groupes</option>';
                data.groupes.forEach(g => {
                    html += `<option value="${g.id}">${g.nom}</option>`;
                });
                document.getElementById("filter-groupe").innerHTML = html;
                
                // Charger automatiquement les étudiants de la promotion
                loadEtudiants(promotionId, null);
            } else {
                document.getElementById("groupe-container").style.display = "none";
                loadEtudiants(promotionId, null);
            }
        } catch (error) {
            console.error("❌ Erreur chargement groupes:", error);
        }
    }

    async function updateEtudiantsOnGroupeChange() {
        const promotionId = document.getElementById("filter-promotion")?.value;
        const groupeId = document.getElementById("filter-groupe")?.value;
        
        console.log("👥 Groupe changé - Promo:", promotionId, "Groupe:", groupeId);

        if (!promotionId) {
            return;
        }

        loadEtudiants(promotionId, groupeId || null);
    }

    async function loadEtudiants(promotionId, groupeId) {
        console.log("📥 Chargement étudiants - Promo:", promotionId, "Groupe:", groupeId);

        try {
            // ✅ URL correcte selon les urls.py
            let url = `${BASE_URL}api/etudiants/groupe/?promotion_id=${promotionId}`;
            if (groupeId) {
                url += `&groupe_id=${groupeId}`;
            }

            console.log("🔗 URL appelée:", url);

            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log("📊 Étudiants reçus:", data);
            
            let html = '<option value="">Choisir un étudiant...</option>';
            
            if (data.etudiants && data.etudiants.length > 0) {
                data.etudiants.forEach(e => {
                    html += `<option value="${e.id}">${e.nom}</option>`;
                });
                console.log("✅ Étudiants chargés:", data.etudiants.length);
            } else {
                console.warn("⚠️ Aucun étudiant trouvé");
            }
            
            document.getElementById("filter-etudiant").innerHTML = html;
        } catch (error) {
            console.error("❌ Erreur chargement étudiants:", error);
            document.getElementById("filter-etudiant").innerHTML = '<option value="">Erreur lors du chargement</option>';
        }
    }

    // ══════════════════════════════════════════════
    // 📡 CHARGEMENT DONNÉES + MAJ GRAPHIQUES
    // ══════════════════════════════════════════════
    function updateCharts(url) {
        console.log("📊 Mise à jour des graphiques avec:", url);

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                console.log("✅ Données reçues:", data);
                
                if (!data) throw new Error("Données vides");

                updateNumericStats(data);
                updateBarChart(data);
                updateDistributionChart(data);
                updatePieChart3D(data);
            })
            .catch(error => {
                console.error("❌ Erreur:", error);
                showErrorMessage("Erreur lors du chargement des données");
            });
    }

    // ══════════════════════════════════════════════
    // 📊 STATS NUMÉRIQUES (KPI)
    // ══════════════════════════════════════════════
    function updateNumericStats(data) {
        if (!data.stats) {
            console.warn("⚠️ Pas de stats");
            return;
        }

        const stats = data.stats;
        setElementText("stat-moyenne", (stats.moyenne_globale || 0).toFixed(2));
        setElementText("stat-min", (stats.note_min || 0).toFixed(2));
        setElementText("stat-max", (stats.note_max || 0).toFixed(2));
        setElementText("stat-taux", stats.taux_reussite?.toFixed(1) || 0);

        // Tableau aussi
        setElementText("tbl-moyenne", (stats.moyenne_globale || 0).toFixed(2));
        setElementText("tbl-min", (stats.note_min || 0).toFixed(2));
        setElementText("tbl-max", (stats.note_max || 0).toFixed(2));
        setElementText("tbl-mediane", (stats.mediane || 0).toFixed(2));

        console.log("✅ Stats numériques mises à jour");
    }

    function setElementText(id, text) {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    }

    // ══════════════════════════════════════════════
    // 📈 GRAPHIQUE EN BARRES (Min/Médiane/Max)
    // ══════════════════════════════════════════════
    function updateBarChart(data) {
        const canvas = document.getElementById('myChart');
        if (!canvas) {
            console.error("❌ Canvas myChart introuvable");
            return;
        }

        const ctx = canvas.getContext('2d');
        if (myChart) myChart.destroy();

        const mStats = data.modules_stats || {
            labels: [],
            mins: [],
            medianes: [],
            maxs: []
        };

        // Si pas de données
        if (!mStats.labels || mStats.labels.length === 0) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#999';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Aucune donnée disponible', canvas.width / 2, canvas.height / 2);
            return;
        }

        myChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: mStats.labels,
                datasets: [
                    {
                        label: "Minimum",
                        data: mStats.mins,
                        backgroundColor: "#c084fc",
                        borderColor: "#a855f7",
                        borderWidth: 1
                    },
                    {
                        label: "Médiane",
                        data: mStats.medianes,
                        backgroundColor: "#7c3aed",
                        borderColor: "#6b21a8",
                        borderWidth: 1
                    },
                    {
                        label: "Maximum",
                        data: mStats.maxs,
                        backgroundColor: "#1e3a8a",
                        borderColor: "#1e3a8a",
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { size: 12 } }
                    },
                    title: {
                        display: true,
                        text: 'Min, Médiane et Max par module'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 20,
                        ticks: { stepSize: 2 }
                    }
                }
            }
        });

        console.log("✅ Graphique en barres créé");
    }

    // ══════════════════════════════════════════════
    // 📊 DISTRIBUTION (histogramme)
    // ══════════════════════════════════════════════
    function updateDistributionChart(data) {
        const canvas = document.getElementById('distChart');
        if (!canvas) {
            console.error("❌ Canvas distChart introuvable");
            return;
        }

        const ctx = canvas.getContext('2d');
        if (distChart) distChart.destroy();

        const dist = data.distribution || {
            labels: ['0-5', '5-10', '10-15', '15-20'],
            data: [0, 0, 0, 0]
        };

        distChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: dist.labels,
                datasets: [{
                    label: "Nombre d'étudiants",
                    data: dist.data,
                    backgroundColor: "#16a34a",
                    borderColor: "#0f7b3a",
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Distribution des notes' }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });

        console.log("✅ Distribution mise à jour");
    }

    // ══════════════════════════════════════════════
    // 🍩 CAMEMBERT 3D (Highcharts)
    // ══════════════════════════════════════════════
    function updatePieChart3D(data) {
        const container = document.getElementById('pieChart');
        if (!container) {
            console.error("❌ Container pieChart introuvable");
            return;
        }

        if (typeof Highcharts === 'undefined') {
            console.error("❌ Highcharts non chargé");
            return;
        }

        // Préparer les données
        let chartData = [];
        if (data?.distribution?.labels && data?.distribution?.data) {
            for (let i = 0; i < data.distribution.labels.length; i++) {
                if (data.distribution.data[i] > 0) {
                    chartData.push({
                        name: data.distribution.labels[i],
                        y: data.distribution.data[i]
                    });
                }
            }
        }

        // Aucune donnée
        if (chartData.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:50px; color:#999;">Aucune donnée</div>';
            return;
        }

        // Créer le graphique
        try {
            if (container.highcharts) container.highcharts.destroy();
            container.innerHTML = '';

            const chart = Highcharts.chart('pieChart', {
                chart: {
                    type: 'pie',
                    options3d: {
                        enabled: true,
                        alpha: 45,
                        beta: 0,
                        depth: 45
                    }
                },
                title: { text: 'Répartition des notes' },
                tooltip: {
                    pointFormat: '<b>{point.name}</b><br/>{point.y} étudiant(s) ({point.percentage:.1f}%)'
                },
                plotOptions: {
                    pie: {
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b><br/>{point.percentage:.0f}%'
                        },
                        depth: 45
                    }
                },
                series: [{
                    name: 'Étudiants',
                    data: chartData,
                    colors: ['#ef4444', '#f97316', '#eab308', '#22c55e']
                }],
                credits: { enabled: false }
            });

            console.log("✅ Camembert 3D créé");
        } catch (error) {
            console.error("❌ Erreur camembert:", error);
        }
    }

    function showErrorMessage(message) {
        const container = document.getElementById('pieChart');
        if (container) {
            container.innerHTML = `<div style="text-align:center; padding:50px; color:#666;">${message}</div>`;
        }
    }

    // ══════════════════════════════════════════════
    // 🚀 INITIALISATION ET ÉVÉNEMENTS
    // ══════════════════════════════════════════════
    console.log("🚀 Initialisation...");

    // Événements des filtres
    const promotionEl = document.getElementById("filter-promotion");
    const groupeEl = document.getElementById("filter-groupe");
    const moduleEl = document.getElementById("filter-module");
    const etudiantEl = document.getElementById("filter-etudiant");

    if (promotionEl) {
        promotionEl.addEventListener("change", () => {
            console.log("🔄 Filtre promotion changé");
            updateFiltersOnPromoChange();
            updateCharts(buildURL());
        });
    }

    if (groupeEl) {
        groupeEl.addEventListener("change", () => {
            console.log("🔄 Filtre groupe changé");
            updateEtudiantsOnGroupeChange();
            updateCharts(buildURL());
        });
    }

    if (moduleEl) {
        moduleEl.addEventListener("change", () => {
            console.log("🔄 Filtre module changé");
            updateCharts(buildURL());
        });
    }

    if (etudiantEl) {
        etudiantEl.addEventListener("change", () => {
            console.log("🔄 Filtre étudiant changé");
            updateCharts(buildURL());
        });
    }

    // Chargement initial
    setTimeout(() => {
        console.log("📊 Chargement initial des données...");
        updateCharts(buildURL());
    }, 500);
});