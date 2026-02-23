document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ Dashboard Administratif chargé');

    let dashboardData = {
        etudiants: { total: 0, list: [] },
        modules: { total: 0, list: [] },
        absences: { total: 0, list: [] },
        alertes: { immediates: 0, etudiants_risque: [], modules_echec: [], retards_saisie: 0 }
    };

    updateDateTime();
    loadDashboardData();
    setInterval(loadDashboardData, 300000);

    setupModalEvents();
    setupClickableCards();

    function setupModalEvents() {
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', closeAllModals);
        });

        window.addEventListener('click', function(event) {
            if (event.target.classList.contains('modal')) {
                closeAllModals();
            }
        });
    }

    function setupClickableCards() {
        document.getElementById('etudiantsCard')?.addEventListener('click', () => loadEtudiantsData());
        document.getElementById('modulesCard')?.addEventListener('click', () => loadModulesData());
        document.getElementById('absencesCard')?.addEventListener('click', () => loadAbsencesData());
        document.getElementById('alertesCard')?.addEventListener('click', () => showSummary('alertes'));
    }

    function closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => modal.style.display = 'none');
    }

    function openModal(type) {
        const modal = document.getElementById(`${type}Modal`);
        const container = document.getElementById(`${type}DetailsContainer`);
        if (!modal || !container) return;

        let content = '';
        switch(type) {
            case 'etudiants': content = buildEtudiantsDetailsHTML(); break;
            case 'modules': content = buildModulesDetailsHTML(); break;
            case 'absences': content = buildAbsencesDetailsHTML(); break;
            case 'alertes': content = buildAlertesDetailsHTML(); break;
        }

        container.innerHTML = content;
        modal.style.display = 'block';
    }

    function updateDateTime() {
        const dateElement = document.getElementById('currentDateTime');
        if (!dateElement) return;
        dateElement.textContent = new Date().toLocaleDateString('fr-FR', {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
        });
    }

    async function loadDashboardData() {
        showLoading(true);
        try {
            const response = await fetch('/dashboard/api/stats/');
            const data = await response.json();
            console.log("📊 Données API reçues:", data);

            if (data.kpi) {
                setText('totalEtudiants', data.kpi.etudiants?.total || 0);
                setText('totalModules', data.kpi.modules?.total || 0);
                setText('totalAbsences', data.kpi.absences?.total || 0);
                setText('totalAlertes', data.kpi.alertes?.total || 0);
            }
            
            if (data.alertes) dashboardData.alertes = data.alertes;
            
        } catch (error) {
            console.error('❌ Erreur chargement dashboard:', error);
            showErrorMessage("Impossible de charger les données");
        } finally {
            showLoading(false);
        }
    }

    function setText(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    async function loadEtudiantsData() {
        showLoading(true);
        try {
            const response = await fetch('/etudiants/api/data/');
            const data = await response.json();
            
            if (Array.isArray(data)) {
                dashboardData.etudiants = { total: data.length, list: data };
            } else if (data.etudiants) {
                dashboardData.etudiants = { total: data.etudiants.length, list: data.etudiants };
            } else {
                dashboardData.etudiants = { total: 0, list: [] };
            }
            
            console.log("✅ Étudiants chargés:", dashboardData.etudiants);
            showSummary('etudiants');
        } catch (error) {
            console.error('Erreur chargement étudiants:', error);
            showErrorMessage("Erreur chargement des étudiants");
        } finally {
            showLoading(false);
        }
    }

    async function loadModulesData() {
        showLoading(true);
        try {
            const response = await fetch('/cours/api/data/');
            const data = await response.json();
            
            if (Array.isArray(data)) {
                dashboardData.modules = { total: data.length, list: data };
            } else if (data.modules) {
                dashboardData.modules = { total: data.modules.length, list: data.modules };
            } else {
                dashboardData.modules = { total: 0, list: [] };
            }
            
            console.log("✅ Modules chargés:", dashboardData.modules);
            showSummary('modules');
        } catch (error) {
            console.error('Erreur chargement modules:', error);
            showErrorMessage("Erreur chargement des modules");
        } finally {
            showLoading(false);
        }
    }

    async function loadAbsencesData() {
        showLoading(true);
        try {
            const response = await fetch('/evaluation/api/absences/');
            const data = await response.json();
            
            if (Array.isArray(data)) {
                dashboardData.absences = { total: data.length, list: data };
            } else if (data.absences) {
                dashboardData.absences = { total: data.absences.length, list: data.absences };
            } else {
                dashboardData.absences = { total: 0, list: [] };
            }
            
            console.log("✅ Absences chargées:", dashboardData.absences);
            showSummary('absences');
        } catch (error) {
            console.error('Erreur chargement absences:', error);
            showErrorMessage("Erreur chargement des absences");
        } finally {
            showLoading(false);
        }
    }

    function showSummary(type) {
        const container = document.getElementById('summaryContainer');
        if (!container) return;

        let summaryHTML = '';
        let color = getColorForType(type);
        let icon = getIconForType(type);
        let total = dashboardData[type]?.total || 0;

        switch(type) {
            case 'etudiants':
                summaryHTML = buildEtudiantsSummary();
                break;
            case 'modules':
                summaryHTML = buildModulesSummary();
                break;
            case 'absences':
                summaryHTML = buildAbsencesSummary();
                break;
            case 'alertes':
                summaryHTML = buildAlertesSummary();
                total = dashboardData.alertes?.immediates || 0;
                break;
        }

        container.innerHTML = `
            <div class="summary-card">
                <div class="summary-header">
                    <div class="summary-title">
                        <i class="fas ${icon} ${color}"></i>
                        <h3>Résumé des ${type}</h3>
                        <span class="summary-badge ${color}">${total}</span>
                    </div>
                    <button class="summary-close" onclick="closeSummary()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="summary-preview">
                    ${summaryHTML}
                </div>
                <div class="summary-footer">
                    <button class="btn-view-details ${color}" onclick="openModal('${type}')">
                        Voir les détails complets <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
            </div>
        `;
    }

    function closeSummary() {
        const container = document.getElementById('summaryContainer');
        if (container) {
            container.innerHTML = '';
        }
    }

    function getIconForType(type) {
        const icons = { etudiants: 'fa-users', modules: 'fa-book', absences: 'fa-calendar-times', alertes: 'fa-exclamation-triangle' };
        return icons[type] || 'fa-info-circle';
    }

    function getColorForType(type) {
        const colors = { etudiants: 'blue', modules: 'green', absences: 'orange', alertes: 'red' };
        return colors[type] || '';
    }

    function buildEtudiantsSummary() {
        const data = dashboardData.etudiants;
        if (!data.list || data.list.length === 0) {
            return `<div class="preview-item"><span class="preview-label">Total</span><span class="preview-value">${data.total}</span></div>`;
        }

        const parClasse = {};
        data.list.forEach(e => {
            const classe = e.classe || e.promotion || e.niveau || 'N/A';
            parClasse[classe] = (parClasse[classe] || 0) + 1;
        });

        return Object.entries(parClasse).map(([classe, count]) => `
            <div class="preview-item">
                <span class="preview-label">${classe}</span>
                <span class="preview-value">${count}</span>
            </div>
        `).join('');
    }

    function buildModulesSummary() {
        const data = dashboardData.modules;
        if (!data.list || data.list.length === 0) {
            return `<div class="preview-item"><span class="preview-label">Total</span><span class="preview-value">${data.total}</span></div>`;
        }

        return `<div class="preview-item"><span class="preview-label">Modules</span><span class="preview-value">${data.list.length}</span></div>`;
    }

    function buildAbsencesSummary() {
        const data = dashboardData.absences;
        if (!data.list || data.list.length === 0) {
            return `<div class="preview-item"><span class="preview-label">Total</span><span class="preview-value">${data.total}</span></div>`;
        }

        const justifiees = data.list.filter(a => a.justifie || a.est_justifie).length;
        const nonJustifiees = data.list.length - justifiees;

        return `
            <div class="preview-item"><span class="preview-label">Justifiées</span><span class="preview-value">${justifiees}</span></div>
            <div class="preview-item"><span class="preview-label">Non justifiées</span><span class="preview-value">${nonJustifiees}</span></div>
        `;
    }

    function buildAlertesSummary() {
        const data = dashboardData.alertes;
        return `
            <div class="preview-item"><span class="preview-label">Immédiates</span><span class="preview-value">${data.immediates || 0}</span></div>
            <div class="preview-item"><span class="preview-label">À risque</span><span class="preview-value">${data.etudiants_risque?.length || 0}</span></div>
            <div class="preview-item"><span class="preview-label">Échec</span><span class="preview-value">${data.modules_echec?.length || 0}</span></div>
            <div class="preview-item"><span class="preview-label">Retards</span><span class="preview-value">${data.retards_saisie || 0}</span></div>
        `;
    }

    function buildEtudiantsDetailsHTML() {
        const data = dashboardData.etudiants;
        if (!data.list || data.list.length === 0) {
            return '<div class="no-data">Aucun étudiant trouvé</div>';
        }

        let html = '<div class="list-container">';
        data.list.forEach(e => {
            const matricule = e.matricule || e.id || '';
            const nom = e.nom || '';
            const prenom = e.prenom || '';
            const classe = e.classe || e.promotion || e.niveau || 'N/A';
            const moyenne = e.moyenne || e.moyenne_generale || 'N/A';
            
            html += `
                <div class="list-item">
                    <div class="item-info">
                        <strong>${matricule}</strong>
                        <span>${prenom} ${nom} - ${classe}</span>
                    </div>
                    <span class="item-badge blue">${moyenne}/20</span>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }

    function buildModulesDetailsHTML() {
        const data = dashboardData.modules;
        if (!data.list || data.list.length === 0) {
            return '<div class="no-data">Aucun module trouvé</div>';
        }

        let html = '<div class="list-container">';
        data.list.forEach(m => {
            const code = m.code || m.id || '';
            const nom = m.nom || m.libelle || '';
            const credits = m.credits || m.nb_credits || 0;
            
            html += `
                <div class="list-item">
                    <div class="item-info">
                        <strong>${code}</strong>
                        <span>${nom}</span>
                    </div>
                    <span class="item-badge green">${credits} crédits</span>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }

    function buildAbsencesDetailsHTML() {
        const data = dashboardData.absences;
        if (!data.list || data.list.length === 0) {
            return '<div class="no-data">Aucune absence trouvée</div>';
        }

        let html = '<div class="list-container">';
        data.list.forEach(a => {
            const etudiant = a.etudiant || a.etudiant_nom || `${a.prenom || ''} ${a.nom || ''}`.trim() || 'N/A';
            const module = a.module || a.module_nom || a.cours || 'N/A';
            const date = a.date || a.date_absence || 'N/A';
            const justifie = a.justifie || a.est_justifie || false;
            
            html += `
                <div class="list-item">
                    <div class="item-info">
                        <strong>${etudiant}</strong>
                        <span>${module} - ${date}</span>
                    </div>
                    <span class="item-badge ${justifie ? 'green' : 'orange'}">
                        ${justifie ? 'Justifiée' : 'Non justifiée'}
                    </span>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }

    function buildAlertesDetailsHTML() {
        const data = dashboardData.alertes;
        let html = '';

        html += `<div class="detail-section">
            <h3><i class="fas fa-exclamation-circle red"></i> Alertes immédiates</h3>
            <div class="stat-card"><span class="stat-value red">${data.immediates || 0}</span></div>
        </div>`;

        if (data.etudiants_risque?.length > 0) {
            html += '<div class="detail-section"><h3><i class="fas fa-users red"></i> Étudiants à risque</h3><div class="list-container">';
            data.etudiants_risque.forEach(e => {
                html += `
                    <div class="list-item">
                        <div class="item-info">
                            <strong>${e.matricule || ''}</strong>
                            <span>${e.raison || ''}</span>
                        </div>
                        ${e.taux_absence ? `<span class="item-badge red">${e.taux_absence}%</span>` : ''}
                    </div>
                `;
            });
            html += '</div></div>';
        }

        if (data.modules_echec?.length > 0) {
            html += '<div class="detail-section"><h3><i class="fas fa-book red"></i> Modules en échec</h3><div class="tags-container">';
            data.modules_echec.forEach(m => {
                html += `<span class="module-tag">${m}</span>`;
            });
            html += '</div></div>';
        }

        html += `<div class="detail-section">
            <h3><i class="fas fa-clock red"></i> Retards de saisie</h3>
            <div class="stat-card"><span class="stat-value red">${data.retards_saisie || 0}</span></div>
        </div>`;

        return html;
    }

    // Rendre les fonctions accessibles globalement
    window.openModal = openModal;
    window.closeSummary = closeSummary;

    function showLoading(show) {
        let loader = document.getElementById('loading-indicator');
        if (!loader && show) {
            loader = document.createElement('div');
            loader.id = 'loading-indicator';
            loader.innerHTML = '<div class="spinner"></div><span>Chargement...</span>';
            document.body.appendChild(loader);
        }
        if (loader) loader.style.display = show ? 'flex' : 'none';
    }

    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i><span>${message}</span><button onclick="this.parentElement.remove()">×</button>`;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
});