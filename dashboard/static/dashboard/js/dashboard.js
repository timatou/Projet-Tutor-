document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Dashboard Administratif chargé');
    
    updateDateTime();
    loadDashboardData();
    
    function updateDateTime() {
        const dateElement = document.getElementById('currentDateTime');
        if (dateElement) {
            const now = new Date();
            dateElement.textContent = now.toLocaleDateString('fr-FR', {
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
            });
        }
    }
    
    async function loadDashboardData() {
        try {
            const response = await fetch('/dashboard/api/stats/');
            const data = await response.json();
            
            // KPI
            updateKPI(data.kpi);
            
            // Alertes
            updateAlerts(data.alertes);
            
            // Graphiques
            createPromoChart(data.repartition_promotions);
            createAbsencesChart(data.evolution_absences);
            createAcademicChart(data.statut_academique);
            createPieChartAbsences(data.absences_par_module);
            
        } catch (error) {
            console.error('Erreur chargement:', error);
        }
    }
    
    function updateKPI(kpi) {
        document.getElementById('totalEtudiants').textContent = kpi.etudiants.total;
        const varEtu = document.getElementById('variationEtudiants');
        varEtu.textContent = `${kpi.etudiants.variation >= 0 ? '+' : ''}${kpi.etudiants.variation} cette semaine`;
        varEtu.className = `kpi-variation ${kpi.etudiants.variation >= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('totalModules').textContent = kpi.modules.total;
        document.getElementById('variationModules').textContent = `Dont ${kpi.modules.nouveaux} nouveaux`;
        
        document.getElementById('totalAbsences').textContent = kpi.absences.total;
        const varAbs = document.getElementById('variationAbsences');
        varAbs.textContent = `${kpi.absences.variation >= 0 ? '+' : ''}${kpi.absences.variation} cette semaine`;
        varAbs.className = `kpi-variation ${kpi.absences.variation <= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('totalAlertes').textContent = kpi.alertes.total;
        document.getElementById('totalAlertesBadge').textContent = `${kpi.alertes.total} alertes`;
    }
    
    function updateAlerts(alertes) {
        document.getElementById('alertesImmediates').textContent = alertes.immediates;
        document.getElementById('etudiantsRisqueCount').textContent = alertes.etudiants_risque.length;
        
        const etudiantsContainer = document.getElementById('etudiantsRisque');
        if (alertes.etudiants_risque.length > 0) {
            etudiantsContainer.innerHTML = alertes.etudiants_risque.map(e => `
                <div class="alert-subitem">
                    <i class="fas fa-user"></i> ${e.matricule} - ${e.raison}
                </div>
            `).join('');
        } else {
            etudiantsContainer.innerHTML = '<div class="alert-subitem">Aucun étudiant en risque</div>';
        }
        
        document.getElementById('modulesEchecCount').textContent = alertes.modules_echec.length;
        const modulesEchec = document.getElementById('modulesEchec');
        modulesEchec.textContent = alertes.modules_echec.length > 0 ? 
            alertes.modules_echec.join(' et ') : 'Aucun module en échec';
        
        document.getElementById('retardsSaisie').textContent = alertes.retards_saisie;
    }
    
    function createPromoChart(data) {
        const ctx = document.getElementById('promoChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: '#0f2d5c',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    
    function createAbsencesChart(data) {
        const ctx = document.getElementById('absencesChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Absences',
                    data: data.values,
                    borderColor: '#f44336',
                    backgroundColor: 'rgba(244, 67, 54, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    
    function createAcademicChart(data) {
        const ctx = document.getElementById('academicChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Réussite',
                        data: data.reussite,
                        borderColor: '#4caf50',
                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'En difficulté',
                        data: data.difficile,
                        borderColor: '#f44336',
                        backgroundColor: 'rgba(244, 67, 54, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    
    function createPieChartAbsences(modules) {
        const ctx = document.getElementById('pieChartAbsences').getContext('2d');
        
        if (window.pieChartInstance) {
            window.pieChartInstance.destroy();
        }
        
        const labels = modules.map(m => m.libelle || m.code);
        const values = modules.map(m => m.total);
        const colors = ['#0f2d5c', '#1e478c', '#2c61ba', '#3a7be8', '#4e8ff5'];
        
        window.pieChartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderWidth: 1,
                    borderColor: 'white'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { boxWidth: 12, font: { size: 11 } } },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percent = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${context.label}: ${value} absences (${percent}%)`;
                            }
                        }
                    }
                }
            }
        });
        
        updateModuleList(modules);
    }
    
    function updateModuleList(modules) {
        const container = document.getElementById('moduleAbsencesList');
        container.innerHTML = modules.map(m => `
            <div class="module-item">
                <h4>${m.code} - ${m.libelle || ''}</h4>
                <div class="module-stats">
                    <div class="module-stat">
                        <span class="stat-label">Total</span>
                        <span class="stat-value">${m.total}</span>
                    </div>
                    <div class="module-stat">
                        <span class="stat-label">Justifiées</span>
                        <span class="stat-value justifiees">${m.justifiees}</span>
                    </div>
                    <div class="module-stat">
                        <span class="stat-label">Non justifiées</span>
                        <span class="stat-value non-justifiees">${m.non_justifiees}</span>
                    </div>
                </div>
                <div class="progress-stack">
                    ${m.total > 0 ? `
                        <div class="progress-justifiees" style="width: ${(m.justifiees / m.total) * 100}%"></div>
                        <div class="progress-non-justifiees" style="width: ${(m.non_justifiees / m.total) * 100}%"></div>
                    ` : '<div style="width:100%; background:#e0e0e0;"></div>'}
                </div>
            </div>
        `).join('');
    }
});