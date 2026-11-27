/**
 * QuickServe — Single Unified Top Navigation Bar
 * Professional, accessible, responsive Bootstrap 5 navbar.
 * Zero emojis, clean English copywriting.
 */
function renderNavigation(activePage, user) {
  // If an old sidebar element exists, remove or clear it to ensure strictly 1 navigation bar
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarEl) {
    sidebarEl.innerHTML = '';
    sidebarEl.style.display = 'none';
  }

  const topbar = document.getElementById('navbar-container');
  if (!topbar) return;

  const isStaff = user && user.is_staff;
  const initial = (user ? (user.full_name || user.username || 'U') : 'U').charAt(0).toUpperCase();
  const displayName = user ? (user.full_name || user.username) : 'Guest';

  topbar.innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow-sm py-2">
      <div class="container-xl">
        <!-- Brand -->
        <a class="navbar-brand d-flex align-items-center" href="index.html">
          <i class="fa fa-utensils text-warning me-2 fs-5"></i>
          <span class="fw-bold tracking-tight text-white fs-4">QuickServe</span>
        </a>

        <!-- Mobile Toggle -->
        <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#qs-unified-nav" aria-controls="qs-unified-nav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navbar Content -->
        <div class="collapse navbar-collapse" id="qs-unified-nav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
            <li class="nav-item">
              <a class="nav-link ${activePage === 'dashboard' ? 'active' : ''}" href="index.html">
                <i class="fa fa-chart-line me-1 opacity-75"></i> Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link ${activePage === 'menu' ? 'active' : ''}" href="menu.html">
                <i class="fa fa-book-open me-1 opacity-75"></i> Menu
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link ${activePage === 'order-create' ? 'active' : ''}" href="order-create.html">
                <i class="fa fa-cart-plus me-1 opacity-75"></i> Place Order
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link ${activePage === 'orders' ? 'active' : ''}" href="orders.html">
                <i class="fa fa-receipt me-1 opacity-75"></i> Orders
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link ${activePage === 'delivery' ? 'active' : ''}" href="delivery.html">
                <i class="fa fa-motorcycle me-1 opacity-75"></i> Delivery Tracking
              </a>
            </li>

            ${isStaff ? `
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle ${['menu-manage', 'customers', 'reports'].includes(activePage) ? 'active' : ''}" href="#" id="staffDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fa fa-sliders-h me-1 opacity-75"></i> Management
                </a>
                <ul class="dropdown-menu dropdown-menu-dark shadow-sm border-0" aria-labelledby="staffDropdown">
                  <li><a class="dropdown-item ${activePage === 'menu-manage' ? 'active' : ''}" href="menu-manage.html"><i class="fa fa-edit me-2 text-warning"></i>Manage Menu</a></li>
                  <li><a class="dropdown-item ${activePage === 'customers' ? 'active' : ''}" href="customers.html"><i class="fa fa-users me-2 text-warning"></i>Customers</a></li>
                  <li><hr class="dropdown-divider border-secondary"></li>
                  <li><a class="dropdown-item ${activePage === 'reports' ? 'active' : ''}" href="reports.html"><i class="fa fa-chart-bar me-2 text-warning"></i>Sales Reports</a></li>
                </ul>
              </li>
            ` : ''}
          </ul>

          <!-- User Section -->
          <div class="d-flex align-items-center gap-2">
            ${user ? `
              <div class="dropdown">
                <a class="d-flex align-items-center text-decoration-none text-white dropdown-toggle" href="#" id="userMenuDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <div class="rounded-circle bg-warning text-dark d-flex align-items-center justify-content-center fw-bold me-2" style="width:34px; height:34px; font-size:0.85rem;">
                    ${initial}
                  </div>
                  <div class="d-none d-sm-block text-start me-1">
                    <div class="fw-semibold small leading-tight">${displayName}</div>
                    <span class="badge ${isStaff ? 'bg-warning text-dark' : 'bg-secondary'} px-2 py-0" style="font-size:0.65rem;">
                      ${isStaff ? 'Staff Admin' : 'Customer'}
                    </span>
                  </div>
                </a>
                <ul class="dropdown-menu dropdown-menu-end dropdown-menu-dark shadow-sm border-0" aria-labelledby="userMenuDropdown">
                  <li><a class="dropdown-item ${activePage === 'profile' ? 'active' : ''}" href="profile.html"><i class="fa fa-user-circle me-2 text-warning"></i>My Profile</a></li>
                  <li><a class="dropdown-item ${activePage === 'orders' ? 'active' : ''}" href="orders.html"><i class="fa fa-history me-2 text-warning"></i>Order History</a></li>
                  <li><hr class="dropdown-divider border-secondary"></li>
                  <li><button class="dropdown-item text-danger" id="nav-btn-logout"><i class="fa fa-sign-out-alt me-2"></i>Sign Out</button></li>
                </ul>
              </div>
            ` : `
              <a href="login.html" class="btn btn-sm btn-outline-light me-2">Sign In</a>
              <a href="signup.html" class="btn btn-sm btn-warning">Register</a>
            `}
          </div>
        </div>
      </div>
    </nav>
  `;

  const logoutBtn = document.getElementById('nav-btn-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      Auth.logout();
    });
  }
}

// Backward compatibility helper
function renderSidebar(activePage, user) {
  renderNavigation(activePage, user);
}
