/**
 * QuickServe — Application State, Indian Data Store & CRUD Helpers
 * No hardcoded customer names: customer accounts and names are entered by users.
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
   SEED DATA (Version 3: No emojis, no hardcoded customer names)
   ============================================================ */
function seedData() {
  if (QS.get('seed_version') === 3) return;

  // Clear any old customer sessions without valid dynamic ID
  const cur = QS.get('session');
  if (cur && !cur.is_staff && (!cur.id || cur.id < 1000)) {
    QS.remove('session');
  }

  // Authentic Indian Menu Items with HD food photography & categories
  const menuItems = [
    {
      id: 1,
      name: 'Butter Chicken',
      category: 'Main Course',
      is_veg: false,
      price: 350.00,
      description: 'Succulent chicken pieces simmered in rich satin tomato and butter gravy finished with fresh cream.',
      image_url: 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 2,
      name: 'Dal Makhani',
      category: 'Main Course',
      is_veg: true,
      price: 220.00,
      description: 'Slow-cooked whole black lentils simmered overnight with fresh churned white butter and mild spices.',
      image_url: 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 3,
      name: 'Paneer Tikka',
      category: 'Starters',
      is_veg: true,
      price: 280.00,
      description: 'Cubes of fresh malai paneer marinated in spiced hung curd, skewered with bell peppers and tandoor-roasted.',
      image_url: 'https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 4,
      name: 'Hyderabadi Chicken Biryani',
      category: 'Biryani & Rice',
      is_veg: false,
      price: 420.00,
      description: 'Kachi dum biryani made with long-grain basmati, marinated spiced chicken, fried onions, and pure saffron.',
      image_url: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 5,
      name: 'Masala Dosa',
      category: 'Starters',
      is_veg: true,
      price: 180.00,
      description: 'Crisp golden fermented rice crepe rolled with tempered mustard potato mash, coconut chutney, and piping hot sambar.',
      image_url: 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 6,
      name: 'Chole Bhature',
      category: 'Main Course',
      is_veg: true,
      price: 160.00,
      description: 'Piquant Amritsari chickpea masala served with two puffed golden bhaturas, pickled onions, and green chillies.',
      image_url: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 7,
      name: 'Gulab Jamun (2 pcs)',
      category: 'Desserts',
      is_veg: true,
      price: 120.00,
      description: 'Velvety milk-solid mawa dumplings fried to golden amber and steeped in warm rose-cardamom syrup.',
      image_url: 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 8,
      name: 'Mango Lassi',
      category: 'Beverages',
      is_veg: true,
      price: 90.00,
      description: 'Chilled Punjabi yogurt shake blended with sweet Ratnagiri Alphonso pulp and crushed pistachios.',
      image_url: 'https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 9,
      name: 'Palak Paneer',
      category: 'Main Course',
      is_veg: true,
      price: 260.00,
      description: 'Soft cottage cheese simmered in smooth garlicky spinach puree seasoned with roasted cumin and kasuri methi.',
      image_url: 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 10,
      name: 'Samosa Chaat',
      category: 'Starters',
      is_veg: true,
      price: 95.00,
      description: 'Crushed flaky potato samosas layered with warm chole, sweetened beaten curd, tamarind-saunth, and crispy sev.',
      image_url: 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 11,
      name: 'Tandoori Garlic Naan',
      category: 'Breads',
      is_veg: true,
      price: 60.00,
      description: 'Teardrop flatbread slapped on clay tandoor walls, brushed with clarified butter, garlic, and fresh coriander.',
      image_url: 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop',
      is_available: true
    },
    {
      id: 12,
      name: 'Shahi Kheer',
      category: 'Desserts',
      is_veg: true,
      price: 110.00,
      description: 'Slow-reduced fragrant basmati rice pudding infused with saffron, crushed green cardamom, and slivered almonds.',
      image_url: 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop',
      is_available: true
    }
  ];
  QS.set('menu', menuItems);

  // Pre-seeded staff user only. Customer accounts are created when users register.
  const users = [
    {
      id: 1,
      username: 'admin',
      full_name: 'Restaurant Manager',
      email: 'admin@quickserve.in',
      password: 'admin123',
      is_staff: true,
      phone: '+91 98765 00001',
      address: 'Restaurant HQ, Bandra Kurla Complex, Mumbai, MH - 400051'
    }
  ];
  QS.set('users', users);

  // Orders are created dynamically by users when placing orders
  QS.set('orders', []);
  QS.set('delivery', {});

  QS.set('next_user_id', 2);
  QS.set('next_order_id', 1);
  QS.set('seed_version', 3);
  QS.set('seeded', true);
}

/* ============================================================
   AUTH HELPERS
   ============================================================ */
const Auth = {
  login(username, password) {
    const users = QS.get('users') || [];
    const user = users.find(u => u.username.toLowerCase() === username.toLowerCase() && u.password === password);
    if (user) {
      QS.set('session', {
        id: user.id,
        username: user.username,
        full_name: user.full_name || user.username,
        is_staff: Boolean(user.is_staff)
      });
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
   DATA HELPERS (FULL CRUD FOR ALL MODULES)
   ============================================================ */
const Data = {
  // ── MENU (CRUD) ──────────────────────────────────────────
  getMenuItems() {
    return QS.get('menu') || [];
  },
  getAvailableItems() {
    return this.getMenuItems().filter(i => i.is_available);
  },
  getMenuItem(id) {
    return this.getMenuItems().find(i => i.id === Number(id));
  },
  saveMenuItem(item) {
    const items = this.getMenuItems();
    const idx = items.findIndex(i => i.id === item.id);
    if (idx >= 0) items[idx] = item; else items.push(item);
    QS.set('menu', items);
  },
  addMenuItem(data) {
    const items = this.getMenuItems();
    const id = Math.max(0, ...items.map(i => i.id)) + 1;
    const item = {
      id,
      name: data.name || 'New Dish',
      category: data.category || 'Main Course',
      is_veg: Boolean(data.is_veg),
      price: Number(data.price) || 0,
      description: data.description || '',
      image_url: data.image_url || 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop',
      is_available: data.is_available !== false
    };
    items.push(item);
    QS.set('menu', items);
    return item;
  },
  deleteMenuItem(id) {
    const items = this.getMenuItems().filter(i => i.id !== Number(id));
    QS.set('menu', items);
  },

  // ── ORDERS & BOOKING (CRUD) ──────────────────────────────
  getOrders() {
    return QS.get('orders') || [];
  },
  getOrder(id) {
    return this.getOrders().find(o => o.id === Number(id));
  },
  getOrdersForUser(uid) {
    return this.getOrders().filter(o => o.customer_id === Number(uid));
  },
  saveOrder(order) {
    const orders = this.getOrders();
    const idx = orders.findIndex(o => o.id === order.id);
    if (idx >= 0) orders[idx] = order; else orders.push(order);
    QS.set('orders', orders);
  },
  createOrder(customer_id, items, extra = {}) {
    const orders = this.getOrders();
    const id = Math.max(0, ...orders.map(o => o.id)) + 1;
    const order = {
      id,
      customer_id: Number(customer_id),
      status: 'pending',
      created_at: new Date().toISOString(),
      items: items, // [{menu_item_id, quantity}]
      notes: extra.notes || '',
      delivery_address: extra.delivery_address || ''
    };
    orders.push(order);
    QS.set('orders', orders);

    // Auto-create initial delivery tracking record
    this.saveDelivery(id, {
      rider_name: 'Assigning Rider',
      rider_phone: '—',
      current_location: 'Order Placed with Kitchen',
      eta: '30-45 mins'
    });

    return order;
  },
  updateOrderStatus(id, status) {
    const order = this.getOrder(id);
    if (order) {
      order.status = status;
      this.saveOrder(order);

      // Keep delivery status in sync
      const delivery = this.getDelivery(id) || {};
      if (status === 'delivered') {
        delivery.current_location = 'Delivered to customer';
        delivery.eta = 'Delivered';
        this.saveDelivery(id, delivery);
      } else if (status === 'dispatched') {
        delivery.current_location = 'Out for delivery on bike';
        delivery.eta = '15 mins';
        this.saveDelivery(id, delivery);
      }
    }
  },
  deleteOrder(id) {
    const orders = this.getOrders().filter(o => o.id !== Number(id));
    QS.set('orders', orders);
    this.deleteDelivery(id);
  },
  getOrderSubtotal(order) {
    const menu = this.getMenuItems();
    return (order.items || []).reduce((sum, li) => {
      const item = menu.find(m => m.id === li.menu_item_id);
      return sum + (item ? item.price * li.quantity : 0);
    }, 0);
  },
  getOrderTax(order) {
    // 5% GST
    return Math.round(this.getOrderSubtotal(order) * 0.05 * 100) / 100;
  },
  getOrderTotal(order) {
    return this.getOrderSubtotal(order) + this.getOrderTax(order);
  },

  // ── DELIVERY TRACKING (CRUD) ─────────────────────────────
  getDeliveries() {
    return QS.get('delivery') || {};
  },
  getDelivery(order_id) {
    return this.getDeliveries()[order_id] || null;
  },
  saveDelivery(order_id, data) {
    const deliveries = this.getDeliveries();
    deliveries[order_id] = {
      ...data,
      updated_at: new Date().toISOString()
    };
    QS.set('delivery', deliveries);
  },
  deleteDelivery(order_id) {
    const deliveries = this.getDeliveries();
    delete deliveries[order_id];
    QS.set('delivery', deliveries);
  },

  // ── CUSTOMERS & USERS (CRUD) ─────────────────────────────
  getUsers() {
    return QS.get('users') || [];
  },
  getUser(id) {
    return this.getUsers().find(u => u.id === Number(id));
  },
  saveUser(user) {
    const users = this.getUsers();
    const idx = users.findIndex(u => u.id === user.id);
    if (idx >= 0) users[idx] = user;
    QS.set('users', users);
  },
  addUser(data) {
    const users = this.getUsers();
    const id = Math.max(0, ...users.map(u => u.id)) + 1;
    const user = {
      id,
      username: data.username,
      full_name: data.full_name || data.username,
      email: data.email || '',
      password: data.password,
      is_staff: Boolean(data.is_staff),
      phone: data.phone || '+91 ',
      address: data.address || ''
    };
    users.push(user);
    QS.set('users', users);
    return user;
  },
  deleteUser(id) {
    const users = this.getUsers().filter(u => u.id !== Number(id));
    QS.set('users', users);
  }
};

/* ============================================================
   UI & FORMATTING UTILITIES
   ============================================================ */
const UI = {
  formatCurrency(val) {
    const num = Number(val) || 0;
    return '₹' + num.toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  },

  formatDate(isoStr) {
    if (!isoStr) return '—';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    }) + ', ' + d.toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  },

  statusBadge(status) {
    const map = {
      pending:    { icon: 'fa-clock',          label: 'Pending',    cls: 'badge-pending' },
      preparing:  { icon: 'fa-fire-burner',    label: 'Preparing',  cls: 'badge-preparing' },
      ready:      { icon: 'fa-check',          label: 'Ready',      cls: 'badge-ready' },
      dispatched: { icon: 'fa-motorcycle',     label: 'Dispatched', cls: 'badge-dispatched' },
      delivered:  { icon: 'fa-check-double',   label: 'Delivered',  cls: 'badge-delivered' },
      cancelled:  { icon: 'fa-ban',            label: 'Cancelled',  cls: 'badge-cancelled' }
    };
    const s = map[status] || { icon: 'fa-circle', label: status, cls: 'badge-pending' };
    return `<span class="status-badge ${s.cls}"><i class="fa ${s.icon}"></i> ${s.label}</span>`;
  },

  vegBadge(isVeg) {
    return `<span class="${isVeg ? 'veg-badge' : 'non-veg-badge'}" title="${isVeg ? 'Pure Veg' : 'Non-Veg'}"></span>`;
  },

  showAlert(msg, type = 'success', container = null) {
    const target = container || document.getElementById('alert-area') || document.querySelector('main');
    if (!target) return;
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show shadow-sm mb-3`;
    alert.role = 'alert';
    alert.innerHTML = `
      <i class="fa ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    target.prepend(alert);
    setTimeout(() => {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch {
        alert.remove();
      }
    }, 4500);
  }
};

/* ============================================================
   INITIALIZATION
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  seedData();
});
