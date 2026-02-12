const API_BASE = "/cours/api";

document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('tbodyModules');
    const searchInput = document.getElementById('searchModule');
    const filterSemestre = document.getElementById('filterSemestre');
    const form = document.getElementById('formModule');
    const modal = document.getElementById('modalModule');
    const btnOpen = document.getElementById('btnAddModule');
    const btnClose = document.querySelector('.close-modal');

    loadModules();

    async function loadModules() {
        try {
            const res = await fetch(`${API_BASE}/data/`);
            const result = await res.json();
            
            tbody.innerHTML = ""; // Supprime le loader

            if (!result.modules || result.modules.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; padding:30px;">Aucun module trouvé.</td></tr>';
                return;
            }

            result.modules.forEach(m => {
                const tr = document.createElement('tr');
                const color = m.taux >= 50 ? "#28a745" : "#dc3545";

                tr.innerHTML = `
                    <td><span class="code-tag">${m.code}</span></td>
                    <td><strong>${m.libelle}</strong></td>
                    <td>${m.coefficient}</td>
                    <td><span class="badge-semestre">S${m.semestre}</span></td>
                    <td><small>${m.professeurs || 'Non assigné'}</small></td>
                    <td>${m.moyenne} / 20</td>
                    <td>
                        <div style="display:flex; align-items:center; gap:10px; min-width:120px;">
                            <div class="progress-bar-mini"><div class="progress-fill" style="width:${m.taux}%; background:${color};"></div></div>
                            <span style="color:${color}; font-weight:bold;">${m.taux}%</span>
                        </div>
                    </td>
                    <td><button class="btn-icon" style="color:#ff4757" onclick="deleteModule(${m.id})"><i class="fas fa-trash"></i></button></td>
                `;
                tbody.appendChild(tr);
            });
        } catch (error) {
            console.error("Erreur:", error);
            tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:red;">Erreur de chargement des données.</td></tr>';
        }
    }

    // Filtrage
    function applyFilters() {
        const term = searchInput.value.toLowerCase();
        const sem = filterSemestre.value;
        tbody.querySelectorAll('tr').forEach(row => {
            if (row.cells.length < 4) return;
            const matchSearch = row.cells[0].innerText.toLowerCase().includes(term) || row.cells[1].innerText.toLowerCase().includes(term);
            const matchSem = sem === "" || row.cells[3].innerText === `S${sem}`;
            row.style.display = (matchSearch && matchSem) ? "" : "none";
        });
    }

    searchInput?.addEventListener('input', applyFilters);
    filterSemestre?.addEventListener('change', applyFilters);

    // Formulaire
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            code: document.getElementById('m_code').value,
            libelle: document.getElementById('m_libelle').value,
            coefficient: document.getElementById('m_coef').value,
            semestre: document.getElementById('m_semestre').value
        };
        const res = await fetch(`${API_BASE}/ajouter/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            body: JSON.stringify(data)
        });
        if (res.ok) { modal.style.display = 'none'; form.reset(); loadModules(); }
    });

    btnOpen.onclick = () => modal.style.display = 'block';
    btnClose.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => { if(e.target == modal) modal.style.display = 'none'; };
});

async function deleteModule(id) {
    if (confirm("Supprimer ce module ?")) {
        const res = await fetch(`/cours/api/supprimer/${id}/`, { method: 'DELETE', headers: {'X-CSRFToken': getCookie('csrftoken')} });
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
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break;
            }
        }
    }
    return cookieValue;
}