/**
 * Quick Serve – Application State & Utilities
 * localStorage-backed data store. All pages share this module.
 */

/* ============================================================
   STORAGE HELPERS
   ============================================================ */
const QS = {
  get(key) {
    try { return JSON.parse(localStorage.getItem('qs_' + key) || 'null'); } catch { return null; }
  },
  set(key, val) {
    localStorage.setItem('qs_' + key, JSON.stringify(val));
  },
  remove(key) {
    localStorage.removeItem('qs_' + key);
  }
};

/* ============================================================
   SEED DEFAULT DATA  (runs only once)
   ============================================================ */
function seedData() {
  if (QS.get('seeded')) return;

  // Users: [{id, username, email, password, is_staff, phone, address}]
  QS.set('users', [
    { id: 1, username: 'admin', email: 'admin@quickserve.com', password: 'admin123', is_staff: true,  phone: '555-0100', address: '1 Main St' },
    { id: 2, username: 'john',  email: 'john@example.com',     password: 'pass123',  is_staff: false, phone: '555-0201', address: '42 Oak Ave' },
    { id: 3, username: 'sarah', email: 'sarah@example.com',    password: 'pass123',  is_staff: false, phone: '555-0302', address: '7 Pine Rd' },
  ]);

  // Menu Items: [{id, name, description, price, is_available}]
  QS.set('menu', [
    { id: 1, name: 'Classic Burger',    description: 'Beef patty, lettuce, tomato, pickles, house sauce on a brioche bun.',      price: 9.99,  is_available: true },
    { id: 2, name: 'Grilled Chicken',   description: 'Marinated chicken breast with garlic herb butter and seasonal vegetables.', price: 12.50, is_available: true },
    { id: 3, name: 'Caesar Salad',      description: 'Romaine lettuce, parmesan, croutons and house Caesar dressing.',            price: 8.00,  is_available: true },
    { id: 4, name: 'Margherita Pizza',  description: 'San Marzano tomato, fresh mozzarella, basil on a thin crust.',              price: 14.00, is_available: true },
    { id: 5, name: 'Fish and Chips',    description: 'Beer-battered cod served with thick-cut chips and tartar sauce.',           price: 11.75, is_available: true },
    { id: 6, name: 'Veggie Wrap',       description: 'Seasonal roasted vegetables, hummus, feta in a whole-wheat tortilla.',      price: 8.50,  is_available: true },
    { id: 7, name: 'Pasta Carbonara',   description: 'Spaghetti with pancetta, eggs, pecorino and black pepper.',                 price: 13.00, is_available: false },
    { id: 8, name: 'Chocolate Lava Cake', description: 'Warm chocolate cake with a molten centre, served with vanilla ice cream.', price: 6.50, is_available: true },
  ]);

  // Orders: [{id, customer_id, status, created_at, items:[{menu_item_id, quantity}]}]
  const now = Date.now();
  QS.set('orders', [
    { id: 1, customer_id: 2, status: 'delivered',  created_at: new Date(now - 86400000*2).toISOString(),
      items: [{ menu_item_id: 1, quantity: 2 }, { menu_item_id: 8, quantity: 1 }] },
    { id: 2, customer_id: 3, status: 'preparing',  created_at: new Date(now - 3600000).toISOString(),
      items: [{ menu_item_id: 4, quantity: 1 }] },
    { id: 3, customer_id: 2, status: 'pending',    created_at: new Date(now - 1800000).toISOString(),
      items: [{ menu_item_id: 2, quantity: 1 }, { menu_item_id: 3, quantity: 1 }] },
    { id: 4, customer_id: 3, status: 'dispatched', created_at: new Date(now - 7200000).toISOString(),
      items: [{ menu_item_id: 5, quantity: 1 }, { menu_item_id: 6, quantity: 2 }] },
  ]);

  // Delivery: {order_id: {rider_name, current_location, eta, updated_at}}
  QS.set('delivery', {
    1: { rider_name: 'Marcus T.', current_location: 'Delivered', eta: 'Arrived',           updated_at: new Date(now - 86400000).toISOString() },
    4: { rider_name: 'Linda K.',  current_location: '3rd & Main St', eta: '10 minutes',    updated_at: new Date(now - 1200000).toISOString() },
  });

  QS.set('next_user_id',  4);
  QS.set('next_order_id', 5);
  QS.set('seeded', true);
}

/* ============================================================
   AUTH HELPERS
   ============================================================ */
const Auth = {
  login(username, password) {
    const users = QS.get('users') || [];
    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
      QS.set('session', { id: user.id, username: user.username, is_staff: user.is_staff });
      return true;
    }
    return false;
  },
  logout() {
    QS.remove('session');
    window.location.href = 'login.html';
  },
  current() {
    return QS.get('session');
  },
  require(staffOnly = false) {
    const user = this.current();
    if (!user) { window.location.href = 'login.html'; return null; }
    if (staffOnly && !user.is_staff) { window.location.href = 'index.html'; return null; }
    return user;
  },
  isStaff() {
    const u = this.current();
    return u && u.is_staff;
  }
};

/* ============================================================
   DATA HELPERS
   ============================================================ */
const Data = {
  // Menu
  getMenuItems()           { return QS.get('menu') || []; },
  getAvailableItems()      { return this.getMenuItems().filter(i => i.is_available); },
  getMenuItem(id)          { return this.getMenuItems().find(i => i.id === Number(id)); },
  saveMenuItem(item) {
    const items = this.getMenuItems();
    const idx = items.findIndex(i => i.id === item.id);
    if (idx >= 0) items[idx] = item; else items.push(item);
    QS.set('menu', items);
  },
  addMenuItem(data) {
    const items = this.getMenuItems();
    const id = Math.max(0, ...items.map(i => i.id)) + 1;
    const item = { id, ...data };
    items.push(item);
    QS.set('menu', items);
    return item;
  },
  deleteMenuItem(id) {
    QS.set('menu', this.getMenuItems().filter(i => i.id !== Number(id)));
  },

  // Orders
  getOrders()              { return QS.get('orders') || []; },
  getOrder(id)             { return this.getOrders().find(o => o.id === Number(id)); },
  getOrdersForUser(uid)    { return this.getOrders().filter(o => o.customer_id === Number(uid)); },
  saveOrder(order) {
    const orders = this.getOrders();
    const idx = orders.findIndex(o => o.id === order.id);
    if (idx >= 0) orders[idx] = order; else orders.push(order);
    QS.set('orders', orders);
  },
  createOrder(customer_id, items) {
    const orders = this.getOrders();
    const id = Math.max(0, ...orders.map(o => o.id)) + 1;
    const order = { id, customer_id: Number(customer_id), status: 'pending', created_at: new Date().toISOString(), items };
    orders.push(order);
    QS.set('orders', orders);
    return order;
  },
  updateOrderStatus(id, status) {
    const order = this.getOrder(id);
    if (order) { order.status = status; this.saveOrder(order); }
  },
  getOrderTotal(order) {
    const menu = this.getMenuItems();
    return order.items.reduce((sum, li) => {
      const item = menu.find(m => m.id === li.menu_item_id);
      return sum + (item ? item.price * li.quantity : 0);
    }, 0);
  },

  // Delivery
  getDeliveries()          { return QS.get('delivery') || {}; },
  getDelivery(order_id)    { return this.getDeliveries()[order_id] || null; },
  saveDelivery(order_id, data) {
    const deliveries = this.getDeliveries();
    deliveries[order_id] = { ...data, updated_at: new Date().toISOString() };
    QS.set('delivery', deliveries);
  },

  // Users / Customers
  getUsers()               { return QS.get('users') || []; },
  getUser(id)              { return this.getUsers().find(u => u.id === Number(id)); },
  saveUser(user) {
    const users = this.getUsers();
    const idx = users.findIndex(u => u.id === user.id);
    if (idx >= 0) users[idx] = user;
    QS.set('users', users);
  },
  addUser(data) {
    const users = this.getUsers();
    const id = Math.max(0, ...users.map(u => u.id)) + 1;
    const user = { id, ...data };
    users.push(user);
    QS.set('users', users);
    return user;
  }
};

/* ============================================================
   UI UTILITIES
   ============================================================ */
const UI = {
  statusBadge(status) {
    return `<span class="badge badge-${status}">${status}</span>`;
  },
  formatDate(isoStr) {
    if (!isoStr) return '—';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) +
           ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  },
  formatCurrency(val) {
    return '$' + Number(val).toFixed(2);
  },
  showAlert(msg, type = 'success', container = null) {
    const el = document.createElement('div');
    el.className = `alert alert-${type}`;
    el.textContent = msg;
    const target = container || document.querySelector('.main-content');
    if (target) {
      target.prepend(el);
      setTimeout(() => el.remove(), 4000);
    }
  },
  renderTopbar(user) {
    const tb = document.getElementById('topbar-user');
    if (tb) tb.textContent = user ? user.username : '';
    const logoutBtn = document.getElementById('topbar-logout');
    if (logoutBtn) logoutBtn.addEventListener('click', () => Auth.logout());
  },
  setActiveNav(page) {
    document.querySelectorAll('.sidebar-nav a').forEach(a => {
      a.classList.toggle('active', a.dataset.page === page);
    });
  },
  openModal(id)  { document.getElementById(id)?.classList.add('open'); },
  closeModal(id) { document.getElementById(id)?.classList.remove('open'); },
};

/* ============================================================
   BOOTSTRAP
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  seedData();

  // Wire up modal close buttons
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.closeModal || btn.closest('.modal-overlay')?.id;
      if (id) UI.closeModal(id);
      else btn.closest('.modal-overlay')?.classList.remove('open');
    });
  });

  // Close modal on overlay click
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.classList.remove('open');
    });
  });
});
