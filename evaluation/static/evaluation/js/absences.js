document.addEventListener('DOMContentLoaded', function() {
    const filterEtudiant = document.getElementById('filterEtudiant');
    const filterModule = document.getElementById('filterModule');
    const tbody = document.querySelector('#tableAbsences tbody');
    const formAbsence = document.getElementById('formAbsence');
    const modal = document.getElementById('modalAddNote'); 
    const btnAdd = document.getElementById('btnAddNote');
    const btnClose = document.querySelector('.close-modal');

    // --- 1. Modale ---
    if (btnAdd && modal) btnAdd.onclick = () => modal.style.display = 'block';
    if (btnClose && modal) btnClose.onclick = () => modal.style.display = 'none';

    // --- 2. Système de Filtrage ---
    function applyFilters() {
        const valEtudiant = filterEtudiant.value.toLowerCase().trim();
        const valModule = filterModule.value.toLowerCase().trim();
        const rows = tbody.querySelectorAll('tr');

        rows.forEach(row => {
            const textEtudiant = row.querySelector('.col-etudiant')?.textContent.toLowerCase() || "";
            const textModule = row.querySelector('.col-module')?.textContent.toLowerCase() || "";
            const matchEtud = valEtudiant === "" || textEtudiant.includes(valEtudiant);
            const matchMod = valModule === "" || textModule.includes(valModule);
            row.style.display = (matchEtud && matchMod) ? "" : "none";
        });
    }

    if (filterEtudiant) filterEtudiant.addEventListener('change', applyFilters);
    if (filterModule) filterModule.addEventListener('change', applyFilters);

    // --- 3. Chargement des données ---
    loadData();

    async function loadData() {
        try {
            const [resAbs, resEtud, resMod] = await Promise.all([
                fetch('/evaluation/api/absences/'),
                fetch('/etudiants/api/data/'),
                fetch('/cours/api/data/')
            ]);

            const dataAbs = await resAbs.json();
            const dataEtud = await resEtud.json();
            const dataMod = await resMod.json();

            // Remplissage des filtres de recherche
            fillSelect(filterEtudiant, dataEtud.etudiants, 'matricule', 'matricule');
            fillSelect(filterModule, dataMod.modules, 'libelle', 'libelle');

            // --- CORRECTION DATALIST (DÉTECTION AUTO) ---
             const datalist = document.getElementById('listEtudiants');
            datalist.innerHTML = ''; 
            dataEtud.etudiants.forEach(e => {
                datalist.innerHTML += `<option value="${e.matricule.trim()}">${e.nom} ${e.prenom}</option>`;
            });

            // Remplissage du Select Modules dans le formulaire
            const selectModForm = document.getElementById('moduleSelect');
            if (selectModForm && dataMod.modules) {
                selectModForm.innerHTML = '<option value="">-- Choisir --</option>';
                dataMod.modules.forEach(m => {
                    const opt = document.createElement('option');
                    opt.value = m.id;
                    opt.textContent = m.libelle || m.name;
                    selectModForm.appendChild(opt);
                });
            }

            renderTable(dataAbs.absences);

        } catch (err) {
            console.error("Erreur:", err);
        }
    }

    function fillSelect(element, items, valueProp, textProp) {
        if (!element || !items) return;
        element.innerHTML = '<option value="">Tous</option>';
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = String(item[valueProp] || item.id).trim(); 
            opt.textContent = item[textProp] || item.nom || item.libelle;
            element.appendChild(opt);
        });
    }

    function renderTable(absences) {
        if (!tbody) return;
        tbody.innerHTML = '';
        absences.forEach(abs => {
            const tr = document.createElement('tr');
            const dateAff = abs.date_absence ? abs.date_absence.split('-').reverse().join('/') : '—';
            const badgeClass = abs.justifiee ? 'badge-success' : 'badge-danger';
            
            tr.innerHTML = `
                <td class="col-etudiant">${abs.etudiant}</td>
                <td class="col-module">${abs.module}</td>
                <td>${dateAff}</td>
                <td><strong>${abs.duree}h</strong></td>
                <td><span class="badge ${badgeClass}">${abs.justifiee ? 'Justifiée' : 'Non justifiée'}</span></td>
                <td>
                    <button class="btn-icon" onclick="deleteAbsence(${abs.id})">
                        <i class="fas fa-trash" style="color:#ff4757"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    // --- 4. Envoi du Formulaire ---
    if (formAbsence) {
        formAbsence.onsubmit = async (e) => {
            e.preventDefault();
            const payload = {
                etudiant: document.getElementById('etudiantInput').value, 
                module: document.getElementById('moduleSelect').value,
                date: document.getElementById('date').value,
                duree: document.getElementById('duree').value,
                justifiee: document.getElementById('justifiee').checked, 
                motif: document.getElementById('motif').value
            };
            console.log("Données envoyées :", payload);

            const res = await fetch('/evaluation/api/ajouter-absence/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                modal.style.display = 'none';
                formAbsence.reset();
                loadData();
            }
        };
    }
});

// Fonctions globales
async function deleteAbsence(id) {
    if (confirm("Supprimer ?")) {
        const res = await fetch(`/evaluation/api/supprimer-absence/${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        if (res.ok) location.reload();
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