/**
 * Student Academic Performance Prediction and Improvement Support System
 * Core Frontend Utilities and Interaction Handlers
 */

// Toast notification helper
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const bgClass = type === 'success' ? 'bg-success text-white' :
                  type === 'error' || type === 'danger' ? 'bg-danger text-white' :
                  type === 'warning' ? 'bg-warning text-dark' : 'bg-primary text-white';

  const icon = type === 'success' ? 'fa-check-circle' :
               type === 'error' || type === 'danger' ? 'fa-exclamation-circle' :
               type === 'warning' ? 'fa-triangle-exclamation' : 'fa-info-circle';

  const toastId = 'toast-' + Date.now();
  const html = `
    <div id="${toastId}" class="toast align-items-center ${bgClass} border-0 shadow-lg mb-2" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body d-flex align-items-center gap-2">
          <i class="fa-solid ${icon} fs-5"></i>
          <div>${message}</div>
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;
  container.insertAdjacentHTML('beforeend', html);
  const el = document.getElementById(toastId);
  const toast = new bootstrap.Toast(el, { delay: 4000 });
  toast.show();
  el.addEventListener('hidden.bs.toast', () => el.remove());
}

// Category Badge Helper
function getCategoryBadge(category) {
  switch (category) {
    case 'Excellent':
      return `<span class="badge-category badge-excellent"><i class="fa-solid fa-star me-1"></i>Excellent</span>`;
    case 'Very Good':
      return `<span class="badge-category badge-very-good"><i class="fa-solid fa-thumbs-up me-1"></i>Very Good</span>`;
    case 'Good':
      return `<span class="badge-category badge-good"><i class="fa-solid fa-circle-check me-1"></i>Good</span>`;
    case 'Average':
      return `<span class="badge-category badge-average"><i class="fa-solid fa-circle-exclamation me-1"></i>Average</span>`;
    case 'Needs Improvement':
      return `<span class="badge-category badge-needs-improvement"><i class="fa-solid fa-triangle-exclamation me-1"></i>Needs Improvement</span>`;
    default:
      return `<span class="badge bg-secondary">Pending</span>`;
  }
}

// Attendance Progress Bar Helper
function getAttendanceProgressBar(pct) {
  const p = parseFloat(pct) || 0;
  let color = 'bg-danger';
  if (p >= 85) color = 'bg-success';
  else if (p >= 75) color = 'bg-primary';
  else if (p >= 65) color = 'bg-warning';

  return `
    <div class="d-flex align-items-center gap-2">
      <div class="custom-progress flex-grow-1" style="height: 8px;">
        <div class="progress-bar ${color}" role="progressbar" style="width: ${Math.min(100, Math.max(0, p))}%" aria-valuenow="${p}" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
      <span class="fw-bold fs-7">${p.toFixed(1)}%</span>
    </div>
  `;
}

// Mobile sidebar toggle
document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebarToggle');
  const backdrop = document.getElementById('sidebarBackdrop');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('show');
      if (backdrop) backdrop.classList.toggle('show');
    });
  }

  if (backdrop && sidebar) {
    backdrop.addEventListener('click', () => {
      sidebar.classList.remove('show');
      backdrop.classList.remove('show');
    });
  }
});
