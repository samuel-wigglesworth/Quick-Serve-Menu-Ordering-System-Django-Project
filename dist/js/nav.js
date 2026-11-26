/**
 * Quick Serve – Shared Sidebar Renderer
 * Call renderSidebar(activePage, user) after DOMContentLoaded.
 */
function renderSidebar(activePage, user) {
  const el = document.getElementById('sidebar');
  if (!el) return;

  const navItem = (page, href, label, icon) => `
    <li><a href="${href}" data-page="${page}" class="${page === activePage ? 'active' : ''}">
      ${icon}<span>${label}</span>
    </a></li>`;

  const menuSVG   = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
  const dashSVG   = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`;
  const orderSVG  = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`;
  const truckSVG  = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>`;
  const userSVG   = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
  const editSVG   = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`;
  const reportSVG = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`;
  const peopleSVG = `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`;

  let html = `
    <div class="sidebar-section">
      <div class="sidebar-label">Main</div>
      <ul class="sidebar-nav">
        ${navItem('dashboard',     'index.html',        'Dashboard',      dashSVG)}
        ${navItem('menu',          'menu.html',         'Menu',           menuSVG)}
        ${navItem('order-create',  'order-create.html', 'Place Order',    orderSVG)}
        ${navItem('orders',        'orders.html',       'Order History',  orderSVG)}
        ${navItem('delivery',      'delivery.html',     'Delivery Tracking', truckSVG)}
      </ul>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-label">Account</div>
      <ul class="sidebar-nav">
        ${navItem('profile', 'profile.html', 'My Profile', userSVG)}
      </ul>
    </div>`;

  if (user && user.is_staff) {
    html += `
    <div class="sidebar-section">
      <div class="sidebar-label">Staff</div>
      <ul class="sidebar-nav">
        ${navItem('menu-manage', 'menu-manage.html', 'Manage Menu',  editSVG)}
        ${navItem('customers',   'customers.html',   'Customers',    peopleSVG)}
        ${navItem('reports',     'reports.html',     'Reports',      reportSVG)}
      </ul>
    </div>`;
  }

  el.innerHTML = html;
}
