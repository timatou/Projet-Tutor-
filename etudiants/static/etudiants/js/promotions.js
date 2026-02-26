const API_BASE = "/etudiants/api";

document.addEventListener('DOMContentLoaded', function () {
    loadPromotions();

    // On remplace le onclick en dur par des event listeners plus propres
    const formPromo = document.getElementById('formPromo');
    const formGroupe = document.getElementById('formGroupe');

    if (formPromo) {
        formPromo.addEventListener('submit', function(e) {
            e.preventDefault();
            savePromo();
        });
    }

    if (formGroupe) {
        formGroupe.addEventListener('submit', function(e) {
            e.preventDefault();
            saveGroupe();
        });
    }
});

async function loadPromotions() {
    const res = await fetch(`${API_BASE}/promotions/`);
    const promos = await res.json();
    
    const promoTableBody = document.querySelector('#tablePromotions tbody');
    const selectPromo = document.getElementById('selectPromoForGroupe');
    
    promoTableBody.innerHTML = "";
    selectPromo.innerHTML = '<option value="">-- Sélectionner une promo --</option>';

    promos.forEach(p => {
        // Ajouter au tableau
        promoTableBody.innerHTML += `
            <tr>
                <td><strong>${p.nom}</strong></td>
                <td>${p.annee || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deletePromo(${p.id})"><i class="fas fa-trash"></i></button>
                </td>
            </tr>`;
        
        // Ajouter au select du formulaire Groupe
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = p.nom;
        selectPromo.appendChild(option);
    });
}

async function savePromo() {
    // Vérifie bien que tes IDs dans le HTML sont promoNom et promoAnnee
    const data = {
        nom: document.getElementById('promoNom').value,
        annee: document.getElementById('promoAnnee').value,
        promotion_id: document.getElementById('selectPromoForGroupe').value
    };

    try {
        const res = await fetch(`${API_BASE}/promotions/ajouter/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': getCookie('csrftoken') 
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {
            document.getElementById('formPromo').reset();
            loadPromotions(); // Recharge le tableau (l'année devrait apparaître maintenant)
        } else {
            // Affiche le message d'erreur envoyé par Django (ex: "existe déjà")
            alert("Erreur : " + result.message);
        }
    } catch (error) {
        alert("Erreur de connexion au serveur");
    }
}

async function saveGroupe() {
    const data = {
        nom: document.getElementById('groupeNom').value,
        promotion_id: document.getElementById('selectPromoForGroupe').value
    };

    const res = await fetch(`${API_BASE}/groupes/ajouter/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Groupe ajouté !");
        document.getElementById('formGroupe').reset();
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