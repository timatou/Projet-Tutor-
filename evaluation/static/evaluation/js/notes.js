document.addEventListener('DOMContentLoaded', function() {
    // --- Sélections ---
    const filterEtudiant = document.getElementById('filterEtudiant');
    const filterModule = document.getElementById('filterModule');
    const tbody = document.querySelector('#tableNotes tbody');
    const formNote = document.getElementById('formNote');
    const modal = document.getElementById('modalAddNote');
    
    // --- Liste des types (doit correspondre à ton backend) ---
    const typesDisponibles = [
        { val: 'EXAM', label: 'Examen' },
        { val: 'DS', label: 'Devoir Surveillé' },
        { val: 'TP', label: 'Travaux Pratiques' },
        { val: 'PROJET', label: 'Projet' }
    ];

    // Initialisation
    loadData();

    // 1. Charger toutes les données
    async function loadData() {
        try {
            const [resNotes, resEtud, resMod] = await Promise.all([
                fetch('/evaluation/api/notes/'),
                fetch('/etudiants/api/data/'),
                fetch('/cours/api/data/')
            ]);

            const dataNotes = await resNotes.json();
            const dataEtud = await resEtud.json();
            const dataMod = await resMod.json();

            fillSelect(filterEtudiant, dataEtud.etudiants, 'matricule', 'matricule');
            fillSelect(filterModule, dataMod.modules, 'libelle', 'libelle');

            // Remplir la Datalist Étudiants
            const datalist = document.getElementById('listEtudiants');
            datalist.innerHTML = ''; 
            dataEtud.etudiants.forEach(e => {
                datalist.innerHTML += `<option value="${e.matricule.trim()}">${e.nom} ${e.prenom}</option>`;
            });

            // Remplir le Select des Modules
            const selectModForm = document.getElementById('moduleSelect');
            selectModForm.innerHTML = '<option value="">Sélectionnez un module...</option>';
            dataMod.modules.forEach(m => {
                selectModForm.innerHTML += `<option value="${m.id}">${m.libelle}</option>`;
            });

            // --- AJOUT : Remplir le Select des Types dans le formulaire ---
            const selectTypeForm = document.getElementById('type'); // Assure-toi que l'id est 'type' dans ton HTML
            if (selectTypeForm) {
                selectTypeForm.innerHTML = '';
                typesDisponibles.forEach(t => {
                    selectTypeForm.innerHTML += `<option value="${t.val}">${t.label}</option>`;
                });
            }

            renderTable(dataNotes.notes);

        } catch (err) {
            console.error("Erreur de chargement:", err);
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:red;">Erreur de connexion au serveur.</td></tr>';
        }
    }

    function fillSelect(element, items, valueProp, textProp) {
        element.innerHTML = '<option value="">Tous</option>';
        if (!items) return;
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = String(item[valueProp]).trim(); 
            opt.textContent = item[textProp];
            element.appendChild(opt);
        });
    }

    // 2. Rendu du tableau (Mise à jour pour afficher le TYPE et la DATE)
    function renderTable(notes) {
        tbody.innerHTML = '';
        if (!notes || notes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Aucune note enregistrée.</td></tr>';
            return;
        }

        notes.forEach(n => {
            const tr = document.createElement('tr');
            // Formater la date si elle est au format YYYY-MM-DD
            const dateAffichage = n.date ? n.date.split('-').reverse().join('/') : '—';

            tr.innerHTML = `
                <td class="col-etudiant">${n.etudiant.trim()}</td>
                <td class="col-module">${n.module.trim()}</td>
                <td><span class="badge">${n.type || 'Note'}</span></td>
                <td><strong>${n.valeur}</strong></td>
                <td>${dateAffichage}</td>
                <td>
                    <button class="btn-icon" onclick="deleteNote(${n.id})" style="border:none; background:none; cursor:pointer;">
                        <i class="fas fa-trash delete-icon" style="color:#ff4757"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    function applyFilters() {
        const selectedEtudiant = filterEtudiant.value.toLowerCase().trim();
        const selectedModule = filterModule.value.toLowerCase().trim();
        const rows = tbody.querySelectorAll('tr');

        rows.forEach(row => {
            const cellEtudiant = row.querySelector('.col-etudiant');
            const cellModule = row.querySelector('.col-module');
            if (!cellEtudiant || !cellModule) return;

            const textEtudiant = cellEtudiant.textContent.toLowerCase().trim();
            const textModule = cellModule.textContent.toLowerCase().trim();

            const matchEtud = selectedEtudiant === "" || textEtudiant === selectedEtudiant;
            const matchMod = selectedModule === "" || textModule.includes(selectedModule);

            row.style.display = (matchEtud && matchMod) ? "" : "none";
        });
    }

    filterEtudiant.addEventListener('change', applyFilters);
    filterModule.addEventListener('change', applyFilters);

    // --- Gestion Modale & Formulaire ---
    const btnAdd = document.getElementById('btnAddNote');
    if (btnAdd) btnAdd.onclick = () => modal.style.display = 'block';
    
    const btnClose = document.querySelector('.close-modal');
    if (btnClose) btnClose.onclick = () => modal.style.display = 'none';
    
    formNote.onsubmit = async (e) => {
        e.preventDefault();
        // --- AJOUT : Récupération de la valeur du type ---
        const payload = {
            etudiant: document.getElementById('etudiant').value,
            module: document.getElementById('moduleSelect').value,
            type: document.getElementById('type').value, // On récupère EXAM, DS, etc.
            valeur: document.getElementById('note').value,
            date: document.getElementById('date').value
        };

        try {
            const res = await fetch('/evaluation/api/ajouter-note/', {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': getCookie('csrftoken'), 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
    modal.style.display = 'none';
    formNote.reset();
    loadData(); 
} else {
    const errorData = await res.json();
    alert("❌ Erreur : " + (errorData.error || "Problème inconnu"));
    console.error("Détail de l'erreur:", errorData);
}
        } catch (err) {
            alert("Erreur réseau.");
        }
    };
});

// 4. FONCTION DE SUPPRESSION
async function deleteNote(id) {
    if (!confirm("Voulez-vous vraiment supprimer cette note ?")) return;
    try {
        const res = await fetch(`/evaluation/api/supprimer-note/${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        if (res.ok) {
            document.location.reload(); 
        } else {
            alert("Erreur lors de la suppression.");
        }
    } catch (err) {
        console.error(err);
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