const API_BASE = "/etudiants/api"; 

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const filterPromo = document.getElementById('filterPromo');
    const tbody = document.querySelector('#tableEtudiants tbody');
    const form = document.getElementById('formEtudiant');
    const modal = document.getElementById('modalAddEtudiant');
    const btnOpen = document.getElementById('btnAddEtudiant');
    const btnClose = document.querySelector('.close-modal');
    
    // Nouveaux éléments pour la gestion dynamique des groupes
    const formPromoSelect = document.getElementById('promotion');
    const formGroupeSelect = document.getElementById('groupe');

    let tousLesGroupes = []; // Stockage local des groupes pour filtrage rapide

    // Initialisation
    loadInitialData();
    loadEtudiants();

    // ==========================================
    // 1. CHARGEMENT INITIAL (Promos + Groupes)
    // ==========================================
    async function loadInitialData() {
        try {
            // Charger les Promotions
            const resP = await fetch(`${API_BASE}/promotions/`);
            const promos = await resP.json();
            promos.forEach(p => {
                const option = `<option value="${p.nom}">${p.nom}</option>`;
                filterPromo.innerHTML += option; // Pour la recherche
                formPromoSelect.innerHTML += option; // Pour le formulaire
            });

            // Charger tous les Groupes
            const resG = await fetch(`${API_BASE}/groupes/`);
            tousLesGroupes = await resG.json();
        } catch (err) { 
            console.error("Erreur chargement listes:", err); 
        }
    }

    // Logique de filtrage dynamique des groupes dans le formulaire
    formPromoSelect.addEventListener('change', function() {
        const promoSelectionnee = this.value;
        
        // On réinitialise le menu des groupes
        formGroupeSelect.innerHTML = '<option value="">-- Choisir un groupe --</option>';
        
        if (promoSelectionnee) {
            // On filtre les groupes qui appartiennent à la promo choisie
            const groupesFiltrés = tousLesGroupes.filter(g => g.promotion__nom === promoSelectionnee);
            
            groupesFiltrés.forEach(g => {
                formGroupeSelect.innerHTML += `<option value="${g.nom}">${g.nom}</option>`;
            });
        }
    });

    // ==========================================
    // 2. RECHERCHE ET FILTRES
    // ==========================================
    function applyFilters() {
        const term = searchInput.value.toLowerCase();
        const promo = filterPromo.value.toLowerCase();

        tbody.querySelectorAll('tr').forEach(row => {
            const nom = row.children[1].textContent.toLowerCase();
            const prenom = row.children[2].textContent.toLowerCase();
            const promotion = row.children[3].textContent.toLowerCase();

            const match = (term === '' || nom.includes(term) || prenom.includes(term)) &&
                        (promo === '' || promotion === promo);

            row.style.display = match ? '' : 'none';
        });
    }

    searchInput.addEventListener('input', applyFilters);
    filterPromo.addEventListener('change', applyFilters);

    // ==========================================
    // 3. CHARGEMENT DU TABLEAU
    // ==========================================
    async function loadEtudiants() {
        try {
            const res = await fetch(`${API_BASE}/data/`);
            const result = await res.json();
            tbody.innerHTML = "";
            result.etudiants.forEach(e => addRow(e));
        } catch (error) { console.error("Erreur chargement:", error); }
    }

    function addRow(e) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${e.matricule}</td>
            <td>${e.nom}</td>
            <td>${e.prenom}</td>
            <td>${e.promotion}</td>
            <td>${e.groupe || 'N/A'}</td>
            <td>${e.email}</td>
            <td>
                <button class="btn-icon delete" onclick="deleteEtudiant('${e.matricule}')">🗑</button>
            </td>
        `;
        tbody.appendChild(tr);
    }

    // ==========================================
    // 4. AJOUTER UN ÉTUDIANT
    // ==========================================
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const etudiantData = {
            matricule: document.getElementById('matricule').value,
            nom: document.getElementById('nom').value,
            prenom: document.getElementById('prenom').value,
            promotion: formPromoSelect.value,
            groupe: formGroupeSelect.value, // Maintenant récupéré depuis le select dynamique
            email: document.getElementById('email').value
        };

        try {
            const response = await fetch(`${API_BASE}/ajouter/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(etudiantData)
            });

            if (response.ok) {
                modal.style.display = 'none';
                form.reset();
                // On remet aussi le select groupe à l'état initial
                formGroupeSelect.innerHTML = '<option value="">-- Choisir un groupe --</option>';
                loadEtudiants(); 
            } else {
                const errorData = await response.json();
                alert("Erreur : " + (errorData.message || "Impossible d'ajouter l'étudiant."));
            }
        } catch (error) {
            console.error("Erreur lors de l'envoi:", error);
        }
    });

    // Gestion de la modale
    btnOpen.onclick = () => modal.style.display = 'block';
    btnClose.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => { if(e.target == modal) modal.style.display = 'none'; };
});

// Fonctions globales (Suppression et Cookie)
async function deleteEtudiant(matricule) {
    if (confirm("Supprimer cet étudiant ?")) {
        try {
            const res = await fetch(`/etudiants/api/supprimer/${matricule}/`, {
                
                
                method: 'DELETE',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            if (res.ok) location.reload();
        } catch (err) { console.error("Erreur suppression:", err); }
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