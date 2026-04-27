function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.querySelector('#tableNotes tbody');
    const modal = document.getElementById('modalAddNote');
    const btnAdd = document.getElementById('btnAddNote');
    const btnClose = document.querySelector('.close-modal');
    const btnCancel = document.getElementById('btnCancel');
    const formNote = document.getElementById('formNote');
    const etudiantInput = document.getElementById('etudiant');
    const epreuveSelect = document.getElementById('epreuveSelect');
    const noteInput = document.getElementById('note');
    const editingIndex = document.getElementById('editingIndex');

    window.notesData = [];

    function openModal() {
        modal.classList.add('show');
    }

    function closeModal() {
        modal.classList.remove('show');
        if (formNote) formNote.reset();
        if (editingIndex) editingIndex.value = '';
    }

    if (btnAdd) {
        btnAdd.addEventListener('click', function() {
            formNote.reset();
            editingIndex.value = '';
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Ajouter une note';
            openModal();
        });
    }

    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnCancel) btnCancel.addEventListener('click', closeModal);

    window.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });

    loadEpreuvesDirect();
    loadEtudiants();
    loadNotes();

    async function loadEpreuvesDirect() {
        try {
            if (!epreuveSelect) return;
            epreuveSelect.innerHTML = '<option value="" disabled selected>Chargement...</option>';

            const response = await fetch('/evaluation/api/epreuves/');
            if (!response.ok) throw new Error(`Erreur HTTP ${response.status}`);
            const data = await response.json();

            epreuveSelect.innerHTML = '<option value="" disabled selected>Sélectionnez une épreuve...</option>';

            if (data.epreuves && data.epreuves.length > 0) {
                data.epreuves.forEach(epreuve => {
                    const option = document.createElement('option');
                    option.value = epreuve.id;
                    let texte = '';
                    if (epreuve.module_code) texte += epreuve.module_code;
                    if (epreuve.type) texte += (texte ? ' - ' : '') + epreuve.type;
                    if (epreuve.date) {
                        try {
                            const d = new Date(epreuve.date);
                            texte += ` (${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()})`;
                        } catch {
                            texte += ` (${epreuve.date})`;
                        }
                    }
                    option.textContent = texte || `Épreuve #${epreuve.id}`;
                    epreuveSelect.appendChild(option);
                });
            } else {
                epreuveSelect.innerHTML = '<option value="" disabled>Aucune épreuve disponible</option>';
            }
        } catch (error) {
            console.error("Erreur chargement épreuves:", error);
            if (epreuveSelect) {
                epreuveSelect.innerHTML = '<option value="">Erreur de chargement</option>';
            }
        }
    }

    async function loadEtudiants() {
        try {
            const response = await fetch('/etudiants/api/data/');
            const data = await response.json();
            const datalist = document.getElementById('listEtudiants');
            if (datalist && data.etudiants) {
                datalist.innerHTML = '';
                data.etudiants.forEach(e => {
                    const option = document.createElement('option');
                    option.value = e.matricule;
                    option.textContent = `${e.matricule} - ${e.nom} ${e.prenom}`;
                    datalist.appendChild(option);
                });
            }
        } catch (error) {
            console.error("Erreur chargement étudiants:", error);
        }
    }

    async function loadNotes() {
        try {
            const response = await fetch('/evaluation/api/notes/');
            const data = await response.json();
            window.notesData = data.notes || [];
            renderTable(window.notesData);
        } catch (error) {
            console.error("Erreur chargement notes:", error);
        }
    }

    function renderTable(notes) {
        if (!tbody) return;
        if (!notes || notes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Aucune note enregistrée.</td></tr>';
            return;
        }
        tbody.innerHTML = notes.map(n => `
            <tr>
                <td>${n.etudiant_matricule || ''} - ${n.etudiant_nom || ''} ${n.etudiant_prenom || ''}</td>
                <td>${n.module_code || ''}</td>
                <td>${n.type || ''}</td>
                <td>${n.valeur || 0}/20</td>
                <td>${n.date_epreuve || ''}</td>
                <td>
                    <button class="btn-action" onclick="editNote(${n.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-action delete-btn" onclick="deleteNote(${n.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    if (formNote) {
        formNote.addEventListener('submit', async function(e) {
            e.preventDefault();

            if (!etudiantInput.value.trim()) {
                alert('Veuillez saisir un matricule étudiant');
                return;
            }
            if (!epreuveSelect.value) {
                alert('Veuillez sélectionner une épreuve');
                return;
            }
            if (!noteInput.value) {
                alert('Veuillez saisir une note');
                return;
            }

            const payload = {
                etudiant: etudiantInput.value.trim(),
                epreuve: parseInt(epreuveSelect.value),
                valeur: parseFloat(noteInput.value)
            };

            try {
                const response = await fetch('/evaluation/api/notes/ajouter/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    closeModal();
                    await loadNotes();
                    alert('Note ajoutée !');
                } else {
                    const result = await response.json();
                    alert(result.message || 'Erreur');
                }
            } catch (error) {
                alert('Erreur de connexion');
            }
        });
    }
});

async function deleteNote(id) {
    if (!confirm('Supprimer cette note ?')) return;
    try {
        await fetch(`/evaluation/api/notes/supprimer/${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        location.reload();
    } catch (error) {
        alert('Erreur');
    }
}

function editNote(id) {
    const note = window.notesData.find(n => n.id === id);
    if (!note) return;
    document.getElementById('etudiant').value = note.etudiant_matricule || '';
    document.getElementById('note').value = note.valeur || '';
    document.getElementById('editingIndex').value = id;
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Modifier la note';
    document.getElementById('modalAddNote').classList.add('show');
}
