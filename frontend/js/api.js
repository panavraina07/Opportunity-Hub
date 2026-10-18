/* ============================================================
   OPPORTUNITYHUB FRONTEND API & INTERACTIONS (api.js)
   ============================================================ */

const API_BASE_URL = 'https://opportunity-hub-beige.vercel.app/api';

// Toast Notification Helper
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.innerText = message;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3500);
}

// -------------------------------------------------------------
// 1. FETCH AND RENDER OPPORTUNITIES (with Search Support)
// -------------------------------------------------------------
async function loadOpportunities(searchQuery = '') {
  try {
    const url = searchQuery 
      ? `${API_BASE_URL}/opportunities?q=${encodeURIComponent(searchQuery)}`
      : `${API_BASE_URL}/opportunities`;

    const res = await fetch(url);
    const result = await res.json();
    if (!result.success) return;

    const categories = ['scholarships', 'internships', 'hackathons', 'workshops', 'competitions', 'government'];

    categories.forEach(cat => {
      const singularCat = cat.endsWith('s') ? cat.slice(0, -1) : cat;
      const sectionGrid = document.querySelector(`#${cat} .card-grid`);

      if (sectionGrid) {
        const items = result.data.filter(item => item.category.toLowerCase() === singularCat);

        if (items.length > 0) {
          sectionGrid.innerHTML = items.map(item => `
            <article class="card reveal in-view" data-cat="${item.category}">
              <span class="tag"><i class="fas fa-tag"></i>${item.tag}</span>
              <h3>${item.title}</h3>
              <div class="org"><i class="fas fa-building"></i>${item.organization}</div>
              <div class="details">
                ${item.eligibility ? `<p><i class="fas fa-user-graduate"></i><span><strong>For:</strong> ${item.eligibility}</span></p>` : ''}
                ${item.amount ? `<p><i class="fas fa-trophy"></i><span><strong>Amount/Perk:</strong> ${item.amount}</span></p>` : ''}
                ${item.deadline ? `<p><i class="fas fa-calendar"></i><span><strong>Deadline:</strong> ${item.deadline}</span></p>` : ''}
                ${item.details ? `<p><i class="fas fa-info-circle"></i><span>${item.details}</span></p>` : ''}
              </div>
              
              <!-- FEATURE 6: APPLY & SHARE BUTTONS -->
              <div class="card-actions">
                <a href="${item.apply_url}" target="_blank" rel="noopener" class="btn">
                  Apply now <i class="fas fa-arrow-right"></i>
                </a>
                <button class="btn-share" onclick="shareOpportunity('${item.title}', '${item.apply_url}')" title="Share via WhatsApp or Copy">
                  <i class="fas fa-share-alt"></i>
                </button>
              </div>
            </article>
          `).join('');
        } else {
          sectionGrid.innerHTML = `<p style="color:var(--text-dim); grid-column:1/-1; padding:20px 0;">No matching opportunities found in this category.</p>`;
        }
      }
    });

  } catch (err) {
    console.warn('Backend server offline.', err);
  }
}

// -------------------------------------------------------------
// 2. FEATURE 6: SHARE OPPORTUNITY (WhatsApp + Clipboard)
// -------------------------------------------------------------
function shareOpportunity(title, url) {
  const shareText = `Check out this opportunity: *${title}*\nApply here: ${url}\nFound on OpportunityHub 🚀`;
  
  if (navigator.share) {
    navigator.share({ title, text: shareText, url }).catch(() => {});
  } else {
    navigator.clipboard.writeText(`${title} - ${url}`);
    showToast(' Link copied to clipboard!');
  }
}

// -------------------------------------------------------------
// 3. FEATURE 2: REAL-TIME SEARCH BAR LISTENER
// -------------------------------------------------------------
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');

if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearSearchBtn.style.display = query ? 'block' : 'none';
    loadOpportunities(query);
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearSearchBtn.style.display = 'none';
    loadOpportunities('');
  });
}

// -------------------------------------------------------------
// 4. FEATURE 1: ADD OPPORTUNITY MODAL & FORM HANDLER
// -------------------------------------------------------------
const addModal = document.getElementById('addOpportunityModal');
const openAddBtn = document.getElementById('openAddModalBtn');
const closeAddBtn = document.getElementById('closeAddModalBtn');
const addForm = document.getElementById('addOpportunityForm');

if (openAddBtn) openAddBtn.addEventListener('click', () => addModal.classList.add('active'));
if (closeAddBtn) closeAddBtn.addEventListener('click', () => addModal.classList.remove('active'));

if (addForm) {
  addForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
      category: document.getElementById('oppCategory').value,
      tag: document.getElementById('oppTag').value,
      title: document.getElementById('oppTitle').value,
      organization: document.getElementById('oppOrg').value,
      eligibility: document.getElementById('oppEligibility').value,
      amount: document.getElementById('oppAmount').value,
      deadline: document.getElementById('oppDeadline').value,
      apply_url: document.getElementById('oppUrl').value,
      details: document.getElementById('oppDetails').value
    };

    try {
      const res = await fetch(`${API_BASE_URL}/opportunities`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.success) {
        showToast('🎉 Opportunity published successfully!');
        addModal.classList.remove('active');
        addForm.reset();
        loadOpportunities(); // Instantly re-render cards
      } else {
        alert(data.message);
      }
    } catch (err) {
      alert('Failed to connect to backend server.');
    }
  });
}

// -------------------------------------------------------------
// 5. FEATURE 4: NOTIFICATION PREFERENCES MODAL & FORM
// -------------------------------------------------------------
const alertsModal = document.getElementById('alertsModal');
const openAlertsBtn = document.getElementById('openAlertsModalBtn');
const closeAlertsBtn = document.getElementById('closeAlertsModalBtn');
const alertsForm = document.getElementById('alertsForm');

if (openAlertsBtn) openAlertsBtn.addEventListener('click', () => alertsModal.classList.add('active'));
if (closeAlertsBtn) closeAlertsBtn.addEventListener('click', () => alertsModal.classList.remove('active'));

if (alertsForm) {
  alertsForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const selectedFields = Array.from(document.querySelectorAll('input[name="field"]:checked'))
      .map(cb => cb.value)
      .join(', ');

    const payload = {
      email: document.getElementById('alertEmail').value,
      fields: selectedFields,
      notification_type: document.getElementById('alertType').value
    };

    try {
      const res = await fetch(`${API_BASE_URL}/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.success) {
        showToast('🔔 Notification preferences saved!');
        alertsModal.classList.remove('active');
        alertsForm.reset();
      } else {
        alert(data.message);
      }
    } catch (err) {
      alert('Failed to connect to backend.');
    }
  });
}

// Close modals when clicking outside the card
window.addEventListener('click', (e) => {
  if (e.target === addModal) addModal.classList.remove('active');
  if (e.target === alertsModal) alertsModal.classList.remove('active');
});

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
  loadOpportunities();
});
