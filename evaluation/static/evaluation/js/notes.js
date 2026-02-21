document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JavaScript notes chargé');
    
    // ===============================
    // ÉLÉMENTS DU DOM
    // ===============================
    
    const filterEtudiant = document.getElementById('filterEtudiant');
    const filterModule = document.getElementById('filterModule');
    const tbody = document.querySelector('#tableNotes tbody');
    
    // Modal
    const modal = document.getElementById('modalAddNote');
    const btnAdd = document.getElementById('btnAddNote');
    const btnClose = document.querySelector('.close-modal');
    
    // Formulaire
    const formNote = document.getElementById('formNote');
    
    // Selects
    const etudiantSelect = document.getElementById('etudiant');
    const moduleSelect = document.getElementById('moduleSelect');
    const typeSelect = document.getElementById('type');
    
    // Stockage global des notes
    window.notesData = [];

    // ===============================
    // GESTION DU MODAL
    // ===============================
    
    if (btnAdd && modal) {
        btnAdd.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
            modal.classList.add('show');
            if (formNote) formNote.reset();
            document.getElementById('editingIndex').value = '';
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Ajouter une note';
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
    // CHARGEMENT DES DONNÉES
    // ===============================
    
    loadData();
    
    async function loadData() {
        try {
            await Promise.all([
                loadEtudiants(),
                loadModules(),
                loadNotes()
            ]);
        } catch (error) {
            console.error('Erreur chargement:', error);
        }
    }
    
    async function loadEtudiants() {
        try {
            const response = await fetch('/etudiants/api/data/');
            const data = await response.json();
            
            if (etudiantSelect) {
                etudiantSelect.innerHTML = '<option value="">Sélectionnez un étudiant...</option>';
                data.etudiants.forEach(e => {
                    const option = document.createElement('option');
                    option.value = e.matricule;
                    option.textContent = `${e.matricule} - ${e.nom} ${e.prenom}`;
                    etudiantSelect.appendChild(option);
                });
            }
            
            if (filterEtudiant) {
                filterEtudiant.innerHTML = '<option value="">Tous les étudiants</option>';
                data.etudiants.forEach(e => {
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
    
    async function loadModules() {
        try {
            const response = await fetch('/cours/api/data/');
            const data = await response.json();
            
            if (moduleSelect) {
                moduleSelect.innerHTML = '<option value="">Sélectionnez un module...</option>';
                data.modules.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m.id;
                    option.textContent = `${m.code} - ${m.libelle}`;
                    moduleSelect.appendChild(option);
                });
            }
            
            if (filterModule) {
                filterModule.innerHTML = '<option value="">Tous les modules</option>';
                data.modules.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m.id;
                    option.textContent = `${m.code} - ${m.libelle}`;
                    filterModule.appendChild(option);
                });
            }
            
            // Remplir aussi le type select avec les choix possibles
            if (typeSelect) {
                typeSelect.innerHTML = '<option value="">Sélectionnez un type...</option>';
                const types = ['DS', 'TP', 'EXAM'];
                types.forEach(t => {
                    const option = document.createElement('option');
                    option.value = t;
                    option.textContent = t;
                    typeSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Erreur chargement modules:', error);
        }
    }
    
    async function loadNotes() {
        try {
            const response = await fetch('/evaluation/api/notes/');
            const data = await response.json();
            renderTable(data.notes || []);
        } catch (error) {
            console.error('Erreur chargement notes:', error);
        }
    }
    
    function renderTable(notes) {
        if (!tbody) return;
        
        // Stocker les données globalement pour l'édition
        window.notesData = notes;
        
        if (!notes.length) {
            tbody.innerHTML = `<tr><td colspan="6" class="empty-state">
                <i class="fas fa-info-circle"></i><br>
                Aucune note enregistrée.
            </td></tr>`;
            return;
        }
        
        tbody.innerHTML = notes.map(n => {
            const noteClass = n.valeur >= 10 ? 'note-excellente' : 'note-insuffisante';
            
            return `
                <tr>
                    <td>${n.etudiant_matricule || ''} - ${n.etudiant_nom || ''} ${n.etudiant_prenom || ''}</td>
                    <td>${n.module_code || ''} - ${n.module_libelle || ''}</td>
                    <td>${n.type || ''}</td>
                    <td class="note-value ${noteClass}">${n.valeur || 0}/20</td>
                    <td>${formatDate(n.date)}</td>
                    <td>
                        <div class="actions-cell">
                            <button class="btn-action" onclick="editNote(${n.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-action delete-btn" onclick="deleteNote(${n.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }
    
    // ===============================
    // FILTRES
    // ===============================
    
    function applyFilters() {
        loadNotes();
    }
    
    if (filterEtudiant) filterEtudiant.addEventListener('change', applyFilters);
    if (filterModule) filterModule.addEventListener('change', applyFilters);
    
    // ===============================
    // ENVOI DU FORMULAIRE
    // ===============================
    
    if (formNote) {
        formNote.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const editingId = document.getElementById('editingIndex')?.value;
            const isEditing = editingId && editingId !== '';
            
            const formData = {
                etudiant: etudiantSelect.value,
                module: moduleSelect.value,
                type: typeSelect.value,
                valeur: document.getElementById('note').value,
                date: document.getElementById('date').value
            };
            
            // Validation
            if (!formData.etudiant || !formData.module || !formData.type || !formData.valeur || !formData.date) {
                alert('Veuillez remplir tous les champs');
                return;
            }
            
            try {
                let url = '/evaluation/api/ajouter-note/';
                let method = 'POST';
                
                if (isEditing) {
                    url = `/evaluation/api/modifier-note/${editingId}/`;
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
                
                const result = await response.json();
                
                if (response.ok) {
                    modal.style.display = 'none';
                    modal.classList.remove('show');
                    formNote.reset();
                    document.getElementById('editingIndex').value = '';
                    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Ajouter une note';
                    await loadNotes();
                    alert(isEditing ? 'Note modifiée avec succès !' : 'Note ajoutée avec succès !');
                } else {
                    alert(result.message || 'Erreur lors de l\'enregistrement');
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

function formatDate(dateStr) {
    if (!dateStr) return '—';
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        return date.toLocaleDateString('fr-FR');
    } catch (error) {
        console.error('Erreur formatage date:', error);
        return dateStr;
    }
}

function editNote(id) {
    // Récupérer la note dans les données stockées
    const note = window.notesData.find(n => n.id === id);
    
    if (!note) {
        console.error('Note non trouvée:', id);
        return;
    }
    
    console.log('Modification de la note:', note);
    
    // Remplir le formulaire du modal avec vérifications
    const etudiantSelect = document.getElementById('etudiant');
    const moduleSelect = document.getElementById('moduleSelect');
    const typeSelect = document.getElementById('type');
    const noteInput = document.getElementById('note');
    const dateInput = document.getElementById('date');
    const editingIndex = document.getElementById('editingIndex');
    const modalTitle = document.getElementById('modalTitle');
    const modal = document.getElementById('modalAddNote');
    
    // Vérifier que tous les éléments existent avant de les utiliser
    if (etudiantSelect && etudiantSelect.options) {
        for (let i = 0; i < etudiantSelect.options.length; i++) {
            if (etudiantSelect.options[i].value === note.etudiant_matricule) {
                etudiantSelect.selectedIndex = i;
                break;
            }
        }
    } else {
        console.error('etudiantSelect non trouvé');
    }
    
    if (moduleSelect && moduleSelect.options) {
        for (let i = 0; i < moduleSelect.options.length; i++) {
            if (moduleSelect.options[i].value == note.module_id) {
                moduleSelect.selectedIndex = i;
                break;
            }
        }
    } else {
        console.error('moduleSelect non trouvé');
    }
    
    if (typeSelect && typeSelect.options) {
        for (let i = 0; i < typeSelect.options.length; i++) {
            if (typeSelect.options[i].value === note.type) {
                typeSelect.selectedIndex = i;
                break;
            }
        }
    } else {
        console.error('typeSelect non trouvé');
    }
    
    if (noteInput) noteInput.value = note.valeur || '';
    if (dateInput) dateInput.value = note.date || '';
    if (editingIndex) editingIndex.value = id;
    
    // Changer le titre du modal
    if (modalTitle) {
        modalTitle.innerHTML = '<i class="fas fa-edit"></i> Modifier la note';
    }
    
    // Ouvrir le modal
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('show');
    } else {
        console.error('modal non trouvé');
    }
}

async function deleteNote(id) {
    if (!confirm('Supprimer cette note ?')) return;
    
    try {
        const response = await fetch(`/evaluation/api/supprimer-note/${id}/`, {
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