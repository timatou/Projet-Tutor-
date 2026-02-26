document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JavaScript chargé');
    
    // ===============================
    // ÉLÉMENTS DU DOM
    // ===============================
    
    // Filtres
    const filterEtudiant = document.getElementById('filterEtudiant');
    const filterModule = document.getElementById('filterModule');
    const dateDebut = document.getElementById('dateDebut');
    const dateFin = document.getElementById('dateFin');
    
    // Tableau
    const tbody = document.querySelector('#tableAbsences tbody');
    
    // Modal
    const modal = document.getElementById('modalAddAbsence');
    const btnAdd = document.getElementById('btnAddAbsence');
    const btnClose = document.querySelector('.close-modal');
    
    // Formulaire
    const formAbsence = document.getElementById('formAbsence');
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.getElementById('justificatif');
    
    // SELECTS (étudiants et modules)
    const etudiantSelect = document.getElementById('etudiantSelect');
    const moduleSelect = document.getElementById('moduleSelect');
    
    // Résumé
    const summaryValues = document.querySelectorAll('.summary-value');
    
    // Stockage global des absences
    window.absencesData = [];

    // ===============================
    // GESTION DU MODAL
    // ===============================
    
    if (btnAdd && modal) {
        btnAdd.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
            modal.classList.add('show');
            if (formAbsence) formAbsence.reset();
            document.getElementById('editingIndex').value = '';
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Signaler une absence';
        });
    }
    
    if (btnClose && modal) {
        btnClose.addEventListener('click', function() {
            modal.style.display = 'none';
            modal.classList.remove('show');
        });
    }
    
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    });

    // ===============================
    // GESTION DE L'UPLOAD
    // ===============================
    
    if (fileUpload && fileInput) {
        fileUpload.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', function() {
            if (this.files?.[0]) {
                const file = this.files[0];
                fileUpload.innerHTML = `
                    <i class="fas fa-file-pdf" style="color: #0f2d5c;"></i>
                    <span style="color: #0f2d5c; font-weight: 500;">${file.name}</span>
                    <small style="color: #1e7b48;">${(file.size / 1024).toFixed(2)} KB</small>
                `;
            }
        });
    }

    // ===============================
    // CHARGEMENT DES DONNÉES
    // ===============================
    
    loadInitialData();
    
    async function loadInitialData() {
        try {
            await loadEtudiants();
            await loadModules();
            await loadAbsences();
        } catch (error) {
            console.error('Erreur chargement initial:', error);
        }
    }
    
    // CHARGEMENT DES ÉTUDIANTS (dans un SELECT)
    async function loadEtudiants() {
        try {
            console.log('Chargement des étudiants...');
            const response = await fetch('/etudiants/api/data');
            console.log('Status étudiants:', response.status);
            
            if (!response.ok) {
                console.error('Erreur HTTP:', response.status);
                return;
            }
            
            const data = await response.json();
            console.log('Données étudiants reçues:', data);
            
            const etudiants = data.etudiants || [];
            
            // Remplir le SELECT étudiant
            if (etudiantSelect) {
                etudiantSelect.innerHTML = '<option value="">Sélectionnez un étudiant...</option>';
                etudiants.forEach(e => {
                    const option = document.createElement('option');
                    option.value = e.matricule;
                    option.textContent = `${e.matricule} - ${e.nom} ${e.prenom}`;
                    etudiantSelect.appendChild(option);
                });
                console.log(`✅ ${etudiants.length} étudiants chargés`);
            }
            
            // Remplir le filtre étudiant
            if (filterEtudiant) {
                filterEtudiant.innerHTML = '<option value="">Tous les étudiants</option>';
                etudiants.forEach(e => {
                    const option = document.createElement('option');
                    option.value = e.matricule;
                    option.textContent = `${e.matricule} - ${e.nom} ${e.prenom}`;
                    filterEtudiant.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Erreur chargement étudiants:', error);
        }
    }
    
    // CHARGEMENT DES MODULES
    async function loadModules() {
        try {
            console.log('Chargement des modules...');
            const response = await fetch('/cours/api/data/');
            console.log('Status modules:', response.status);
            
            if (!response.ok) {
                console.error('Erreur HTTP:', response.status);
                return;
            }
            
            const data = await response.json();
            console.log('Données modules reçues:', data);
            
            const modules = data.modules || [];
            
            // Remplir le select module du formulaire
            if (moduleSelect) {
                moduleSelect.innerHTML = '<option value="">Sélectionnez un module...</option>';
                modules.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m.id;
                    option.textContent = `${m.code} - ${m.libelle}`;
                    moduleSelect.appendChild(option);
                });
                console.log(`✅ ${modules.length} modules chargés`);
            }
            
            // Remplir le filtre module
            if (filterModule) {
                filterModule.innerHTML = '<option value="">Tous les modules</option>';
                modules.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m.id;
                    option.textContent = `${m.code} - ${m.libelle}`;
                    filterModule.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Erreur chargement modules:', error);
        }
    }
    
    // CHARGEMENT DES ABSENCES
    async function loadAbsences() {
        try {
            let url = '/evaluation/api/absences/';
            const params = new URLSearchParams();
            
            if (filterEtudiant?.value) params.append('etudiant', filterEtudiant.value);
            if (filterModule?.value) params.append('module', filterModule.value);
            if (dateDebut?.value) params.append('date_debut', dateDebut.value);
            if (dateFin?.value) params.append('date_fin', dateFin.value);
            
            if (params.toString()) url += '?' + params.toString();
            
            const response = await fetch(url);
            const data = await response.json();
            
            renderTable(data.absences || []);
            updateSummary(data.stats || {});
        } catch (error) {
            console.error('Erreur chargement absences:', error);
            showError();
        }
    }
    
    function renderTable(absences) {
        if (!tbody) return;
        
        // Stocker les données globalement
        window.absencesData = absences;
        
        if (!absences.length) {
            tbody.innerHTML = `<tr><td colspan="6" class="empty-state">
                <i class="fas fa-info-circle"></i><br>
                Aucune absence enregistrée.
            </td></tr>`;
            return;
        }
        
        tbody.innerHTML = absences.map(abs => {
            const badgeClass = abs.justifiee ? 'justifie' : 'non-justifie';
            const badgeTexte = abs.justifiee ? 'Justifié' : 'Non justifié';
            
            return `
                <tr>
                    <td>${abs.etudiant_matricule} - ${abs.etudiant_nom} ${abs.etudiant_prenom || ''}</td>
                    <td>${abs.module_code} - ${abs.module_libelle}</td>
                    <td>${formatDate(abs.date)}</td>
                    <td>${abs.duree} h</td>
                    <td><span class="justification-badge ${badgeClass}">${badgeTexte}</span></td>
                    <td>
                        <div class="actions-cell">
                            ${!abs.justifiee ? 
                                `<button class="btn-action justify-btn" onclick="justifierAbsence(${abs.id})">
                                    <i class="fas fa-check"></i>
                                </button>` : ''
                            }
                            <button class="btn-action" onclick="editAbsence(${abs.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-action delete-btn" onclick="deleteAbsence(${abs.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }
    
    function updateSummary(stats) {
    console.log('📊 Mise à jour des stats:', stats);
    
    document.getElementById('totalAbsences').textContent = stats.total || 0;
    document.getElementById('absencesJustifiees').textContent = stats.justifiees || 0;
    document.getElementById('absencesNonJustifiees').textContent = stats.non_justifiees || 0;
    document.getElementById('etudiantsConcernes').textContent = stats.etudiants_concernes || 0;
}
    function formatDate(dateStr) {
        if (!dateStr) return '—';
        return new Date(dateStr).toLocaleDateString('fr-FR');
    }
    
    function showError() {
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="6" class="empty-state">
                <i class="fas fa-exclamation-triangle"></i><br>
                Erreur de chargement
            </td></tr>`;
        }
    }

    // ===============================
    // FILTRES
    // ===============================
    
    function applyFilters() {
        loadAbsences();
    }
    
    if (filterEtudiant) filterEtudiant.addEventListener('change', applyFilters);
    if (filterModule) filterModule.addEventListener('change', applyFilters);
    if (dateDebut) dateDebut.addEventListener('change', applyFilters);
    if (dateFin) dateFin.addEventListener('change', applyFilters);

    // ===============================
    // ENVOI DU FORMULAIRE
    // ===============================
    
    if (formAbsence) {
        formAbsence.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!etudiantSelect.value) {
                alert('Veuillez sélectionner un étudiant');
                return;
            }
            
            if (!moduleSelect.value) {
                alert('Veuillez sélectionner un module');
                return;
            }
            
            const editingId = document.getElementById('editingIndex')?.value;
            const isEditing = editingId && editingId !== '';
            
            const formData = {
                etudiant: etudiantSelect.value,
                module: moduleSelect.value,
                date: document.getElementById('date').value,
                duree: document.getElementById('duree').value,
                motif: document.getElementById('motif').value
            };
            
            console.log('Données envoyées:', formData);
            console.log('Mode:', isEditing ? 'Édition' : 'Création');
            
            try {
                let url = '/evaluation/api/ajouter-absence/';
                let method = 'POST';
                
                if (isEditing) {
                    url = `/evaluation/api/modifier-absence/${editingId}/`;
                    method = 'PUT';
                }
                
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    modal.style.display = 'none';
                    modal.classList.remove('show');
                    formAbsence.reset();
                    document.getElementById('editingIndex').value = '';
                    
                    // Recharger les absences
                    await loadAbsences();
                    
                    // Restaurer le titre du modal
                    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Signaler une absence';
                    
                    alert(isEditing ? 'Absence modifiée avec succès !' : 'Absence enregistrée avec succès !');
                } else {
                    const error = await response.json();
                    alert(error.message || 'Erreur lors de l\'enregistrement');
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('Erreur de connexion au serveur');
            }
        });
    }
});

// ===============================
// FONCTIONS GLOBALES
// ===============================

async function justifierAbsence(id) {
    if (!confirm('Marquer cette absence comme justifiée ?')) return;
    
    try {
        const response = await fetch(`/evaluation/api/justifier-absence/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Absence justifiée avec succès !');
            // Recharger la liste sans recharger toute la page
            location.reload();
        } else {
            alert('❌ ' + (data.message || 'Erreur lors de la justification'));
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur de connexion au serveur');
    }
}

async function deleteAbsence(id) {
    if (!confirm('Supprimer cette absence ?')) return;
    
    try {
        const response = await fetch(`/evaluation/api/supprimer-absence/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Erreur lors de la suppression');
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function editAbsence(id) {
    // Récupérer l'absence dans les données stockées
    const absence = window.absencesData.find(a => a.id === id);
    
    if (!absence) {
        console.error('Absence non trouvée:', id);
        return;
    }
    
    console.log('Modification de l\'absence:', absence);
    
    // Remplir le formulaire du modal
    const etudiantSelect = document.getElementById('etudiantSelect');
    const moduleSelect = document.getElementById('moduleSelect');
    const dateInput = document.getElementById('date');
    const dureeInput = document.getElementById('duree');
    const motifTextarea = document.getElementById('motif');
    const editingIndex = document.getElementById('editingIndex');
    
    if (etudiantSelect) etudiantSelect.value = absence.etudiant_matricule;
    if (moduleSelect) moduleSelect.value = absence.module_id;
    if (dateInput) dateInput.value = absence.date;
    if (dureeInput) dureeInput.value = absence.duree;
    if (motifTextarea) motifTextarea.value = absence.motif || '';
    if (editingIndex) editingIndex.value = id;
    
    // Changer le titre du modal
    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
        modalTitle.innerHTML = '<i class="fas fa-edit"></i> Modifier l\'absence';
    }
    
    // Ouvrir le modal
    const modal = document.getElementById('modalAddAbsence');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('show');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}