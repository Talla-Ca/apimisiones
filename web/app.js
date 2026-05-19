// RPG Daily Quests - Core Application Logic (app.js)

// --- STATE MANAGEMENT ---
const state = {
  activeTab: 'tab-misiones',
  misiones: [],
  historial: [],
  estadisticas: {
    misiones_pendientes: 0,
    misiones_completadas: 0,
    xp_total_ganada: 0
  },
  currentLevel: 1,
  apiSettings: {
    source: 'prod', // 'prod', 'local', 'custom', 'mock'
    customUrl: 'http://localhost:8000',
    activeUrl: 'https://apirpguni.onrender.com'
  },
  isOfflineMode: false,
  isLoading: false,
  connectionStatus: 'connecting' // 'connecting', 'connected', 'error', 'mock'
};

// Constant gameplay variables matching Dart config
const GAME_CONFIG = {
  XP_PER_LEVEL: 500,
  MAX_MISIONES: 10,
  API_TIMEOUT: 8000 // 8 seconds
};

// --- MOCK / OFFLINE DATABASE INITIALIZER ---
function getMockDB() {
  let mockDB = localStorage.getItem('rpg_mock_db');
  if (!mockDB) {
    const initialDB = {
      misiones: [
        { id: 1, descripcion: "📚 Completar tarea de algoritmos", xp: 100, estado: "pendiente", fecha_creacion: new Date().toISOString() },
        { id: 2, descripcion: "🏃 Hacer ejercicio por 30 minutos", xp: 150, estado: "pendiente", fecha_creacion: new Date().toISOString() },
        { id: 3, descripcion: "☕ Leer un artículo de programación", xp: 50, estado: "pendiente", fecha_creacion: new Date().toISOString() }
      ],
      historial: [
        { id: 101, mision_id: 99, descripcion: "⚔️ Estudiar para el examen de base de datos", xp: 200, fecha_completada: new Date(Date.now() - 86400000).toLocaleString() }
      ]
    };
    localStorage.setItem('rpg_mock_db', JSON.stringify(initialDB));
    return initialDB;
  }
  return JSON.parse(mockDB);
}

function saveMockDB(db) {
  localStorage.setItem('rpg_mock_db', JSON.stringify(db));
}

// --- 8-BIT AUDIO SYNTHESIZER ---
const soundEffects = {
  ctx: null,

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  },

  playTone(freq, type, duration, delay = 0) {
    try {
      this.init();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      
      osc.type = type;
      osc.frequency.value = freq;
      
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime + delay);
      // Linear ramp decay
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + delay + duration);
      
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      
      osc.start(this.ctx.currentTime + delay);
      osc.stop(this.ctx.currentTime + delay + duration);
    } catch (e) {
      console.warn("Audio Context blocked or unsupported:", e);
    }
  },

  playQuestComplete() {
    // Quick rising retro major arpeggio
    this.playTone(261.63, 'triangle', 0.1, 0);     // C4
    this.playTone(329.63, 'triangle', 0.1, 0.08);  // E4
    this.playTone(392.00, 'triangle', 0.1, 0.16);  // G4
    this.playTone(523.25, 'sine', 0.25, 0.24);    // C5
  },

  playLevelUp() {
    // Triumphant 8-bit RPG fanfarre
    const t = 'square';
    this.playTone(349.23, t, 0.15, 0);     // F4
    this.playTone(392.00, t, 0.15, 0.15);  // G4
    this.playTone(440.00, t, 0.15, 0.3);   // A4
    this.playTone(523.25, t, 0.12, 0.45);  // C5
    this.playTone(493.88, t, 0.12, 0.57);  // B4
    this.playTone(523.25, t, 0.12, 0.69);  // C5
    this.playTone(587.33, t, 0.12, 0.81);  // D5
    this.playTone(659.25, t, 0.5, 0.93);   // E5 (Triumph)
  },

  playAction() {
    this.playTone(600, 'sine', 0.05); // Quick click
  },

  playDelete() {
    this.playTone(150, 'sawtooth', 0.2); // Soft rumble
  },

  playError() {
    this.playTone(130, 'sawtooth', 0.12, 0);
    this.playTone(130, 'sawtooth', 0.12, 0.08);
  }
};

// --- CONFETTI PARTICLE SYSTEM ---
function spawnConfetti(x, y, isBig = false) {
  const container = document.body;
  const count = isBig ? 120 : 40;
  const colors = ['#00d4ff', '#00ffff', '#D4AF37', '#00ff00', '#ff6b6b', '#ff00ff', '#ffffff'];
  
  for (let i = 0; i < count; i++) {
    const p = document.createElement('div');
    p.className = 'confetti';
    
    // Choose random colors
    p.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    
    // Initial sizes
    const size = Math.random() * 8 + 4;
    p.style.width = `${size}px`;
    p.style.height = `${size}px`;
    
    // Set viewport coordinates starting point
    p.style.left = `${x || window.innerWidth / 2}px`;
    p.style.top = `${y || window.innerHeight / 2}px`;
    
    container.appendChild(p);

    // Random angles and speeds
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * (isBig ? 12 : 6) + 2;
    const velX = Math.cos(angle) * speed;
    let velY = Math.sin(angle) * speed - (isBig ? 8 : 4); // upwards initial boost
    
    let currentX = x || window.innerWidth / 2;
    let currentY = y || window.innerHeight / 2;
    let opacity = 1;
    let rotation = Math.random() * 360;
    const rotSpeed = (Math.random() - 0.5) * 10;
    
    const startTime = Date.now();
    const duration = isBig ? 2200 : 1200;

    function update() {
      const elapsed = Date.now() - startTime;
      if (elapsed >= duration) {
        p.remove();
        return;
      }
      
      velY += 0.22; // Gravity simulation
      currentX += velX;
      currentY += velY;
      rotation += rotSpeed;
      
      // Calculate opacity fade out
      opacity = 1 - (elapsed / duration);
      
      p.style.transform = `translate3d(${currentX - (x || window.innerWidth / 2)}px, ${currentY - (y || window.innerHeight / 2)}px, 0) rotate(${rotation}deg)`;
      p.style.opacity = opacity;
      
      requestAnimationFrame(update);
    }
    
    requestAnimationFrame(update);
  }
}

// --- NOTIFICATION SYSTEM (TOASTS) ---
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let icon = 'info';
  if (type === 'success') icon = 'check_circle';
  if (type === 'error') icon = 'error';
  
  toast.innerHTML = `
    <span class="material-icons">${icon}</span>
    <span>${message}</span>
  `;
  
  container.appendChild(toast);
  
  // Animate Entrance
  setTimeout(() => toast.classList.add('show'), 50);
  
  // Auto Remove
  setTimeout(() => {
    toast.classList.remove('show');
    toast.addEventListener('transitionend', () => toast.remove());
  }, 4000);
}

// --- API CLIENT WITH MOCK FALLBACK ---
async function apiRequest(endpoint, method = 'GET', body = null) {
  state.isLoading = true;
  document.getElementById('btn-submit-mision').disabled = true;

  // 1. MOCK MODE LOGIC
  if (state.apiSettings.source === 'mock') {
    state.connectionStatus = 'mock';
    return handleMockRequest(endpoint, method, body);
  }

  // Set connecting status on start of request
  if (state.connectionStatus !== 'connected' && state.connectionStatus !== 'connecting') {
    state.connectionStatus = 'connecting';
    updateConnectionIndicator();
  }

  // 2. NETWORK API LOGIC
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), GAME_CONFIG.API_TIMEOUT);
  const url = `${state.apiSettings.activeUrl}${endpoint}`;
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    },
    signal: controller.signal
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, options);
    clearTimeout(timeoutId);
    state.isLoading = false;
    document.getElementById('btn-submit-mision').disabled = false;

    if (!response.ok) {
      let errorMsg = 'Error en la API';
      try {
        const errJson = await response.json();
        errorMsg = errJson.detail || errJson.error || errorMsg;
      } catch(e) {}
      throw new Error(errorMsg);
    }

    // Update connection status on successful request
    state.connectionStatus = 'connected';
    state.isOfflineMode = false;
    updateConnectionIndicator();

    if (response.status === 204) return null;
    const data = await response.json();
    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    state.isLoading = false;
    document.getElementById('btn-submit-mision').disabled = false;

    // Auto failover/Offline helper
    console.error("API Fetch Error:", error);
    
    if (error.name === 'AbortError') {
      showToast("⏱️ Tiempo de espera agotado. Servidor inactivo o demorado.", "error");
    } else {
      showToast(`🔌 Servidor fuera de línea. Cambiando temporalmente a modo demostración offline.`, "error");
    }

    // Force mock mode state
    state.isOfflineMode = true;
    state.connectionStatus = 'error';
    updateConnectionIndicator();
    return handleMockRequest(endpoint, method, body);
  }
}

// --- OFFLINE / MOCK ENDPOINT INTERPRETER ---
function handleMockRequest(endpoint, method, body) {
  return new Promise((resolve, reject) => {
    // Simulate natural delay
    setTimeout(() => {
      const db = getMockDB();

      // HEALTH CHECK
      if (endpoint === '/' && method === 'GET') {
        resolve({ titulo: "RPG Daily Quests API (Mock)", version: "1.0", status: "online" });
      }
      
      // ESTADISTICAS
      else if (endpoint === '/estadisticas' && method === 'GET') {
        const pendientes = db.misiones.filter(m => m.estado === 'pendiente').length;
        const completadas = db.historial.length;
        const xp_total = db.historial.reduce((sum, h) => sum + h.xp, 0);
        resolve({
          misiones_pendientes: pendientes,
          misiones_completadas: completadas,
          xp_total_ganada: xp_total
        });
      }
      
      // HISTORIAL COMPLETADAS
      else if (endpoint === '/misiones/completadas' && method === 'GET') {
        resolve(db.historial);
      }
      
      // VER MISIONES PENDIENTES
      else if (endpoint === '/misiones' && method === 'GET') {
        resolve(db.misiones);
      }
      
      // CREAR MISION AUTO
      else if (endpoint === '/misiones/auto' && method === 'POST') {
        const pendientes = db.misiones.filter(m => m.estado === 'pendiente');
        if (pendientes.length >= GAME_CONFIG.MAX_MISIONES) {
          reject(new Error("Máximo 10 misiones activas simultáneamente"));
          return;
        }

        const maxId = db.misiones.reduce((max, m) => m.id > max ? m.id : max, 0);
        const nueva = {
          id: maxId + 1,
          descripcion: body.descripcion,
          xp: body.xp,
          estado: 'pendiente',
          fecha_creacion: new Date().toISOString()
        };
        db.misiones.push(nueva);
        saveMockDB(db);
        resolve({ mensaje: "Misión creada automáticamente", id: nueva.id, mision: nueva });
      }
      
      // COMPLETAR MISION
      else if (endpoint.startsWith('/misiones/') && endpoint.endsWith('/completar') && method === 'PUT') {
        const id = parseInt(endpoint.split('/')[2]);
        const index = db.misiones.findIndex(m => m.id === id);
        
        if (index === -1) {
          reject(new Error("Misión no encontrada"));
          return;
        }
        
        const mision = db.misiones[index];
        if (mision.estado === 'completada') {
          reject(new Error("La misión ya fue completada"));
          return;
        }
        
        // Remove from active list
        db.misiones.splice(index, 1);
        
        // Add to history
        const nuevoHistorial = {
          id: db.historial.length + 100,
          mision_id: mision.id,
          descripcion: mision.descripcion,
          xp: mision.xp,
          fecha_completada: new Date().toLocaleString()
        };
        db.historial.unshift(nuevoHistorial);
        saveMockDB(db);
        
        resolve({ mensaje: "Misión completada", xp_ganada: mision.xp });
      }
      
      // ELIMINAR MISION
      else if (endpoint.startsWith('/misiones/') && method === 'DELETE') {
        const id = parseInt(endpoint.split('/')[2]);
        const index = db.misiones.findIndex(m => m.id === id);
        
        if (index === -1) {
          reject(new Error("Misión no encontrada"));
          return;
        }
        
        db.misiones.splice(index, 1);
        saveMockDB(db);
        resolve({ mensaje: "Misión eliminada" });
      }
      
      else {
        reject(new Error("404 Endpoint no implementado en Mock"));
      }
    }, 400);
  });
}

// --- CONTROLLER LOGIC & DOM UPDATES ---

function updateConnectionIndicator() {
  const badge = document.getElementById('btn-api-config');
  const text = document.getElementById('connection-text');
  if (!badge || !text) return;
  
  badge.className = 'api-connection';
  
  // Align explicit mock setting status
  if (state.apiSettings.source === 'mock') {
    state.connectionStatus = 'mock';
  }
  
  switch (state.connectionStatus) {
    case 'connecting':
      badge.classList.add('connecting');
      text.textContent = 'Conectando...';
      break;
    case 'connected':
      badge.classList.add('connected');
      if (state.apiSettings.source === 'prod') {
        text.textContent = 'Prod (Conectado)';
      } else if (state.apiSettings.source === 'local') {
        text.textContent = 'API Local (Conectado)';
      } else if (state.apiSettings.source === 'custom') {
        text.textContent = 'API Personalizada';
      } else {
        text.textContent = 'Conectado';
      }
      break;
    case 'error':
      badge.classList.add('error-mode');
      text.textContent = 'Sin Conexión';
      break;
    case 'mock':
    default:
      badge.classList.add('mock-mode');
      text.textContent = state.isOfflineMode ? 'Offline (Demo)' : 'Modo Offline';
      break;
  }
}

// RENDER STATUS BAR AND STATISTICS
function renderStats() {
  const stats = state.estadisticas;
  
  // Calculate Level Logic exact as Flutter
  const xpTotal = stats.xp_total_ganada || 0;
  const level = Math.floor(xpTotal / GAME_CONFIG.XP_PER_LEVEL) + 1;
  const xpInLevel = xpTotal % GAME_CONFIG.XP_PER_LEVEL;
  const progressPct = (xpInLevel / GAME_CONFIG.XP_PER_LEVEL * 100);
  
  // Check for Level Up!
  if (level > state.currentLevel) {
    setTimeout(() => {
      soundEffects.playLevelUp();
      spawnConfetti(window.innerWidth / 2, window.innerHeight / 2 - 100, true);
      showToast(`🏆 ¡SUBISTE DE NIVEL! Ahora eres Nivel ${level} 🏆`, 'success');
    }, 600);
  }
  state.currentLevel = level;

  // Header Updates
  document.getElementById('char-level').textContent = `⭐ Nivel ${level}`;
  document.getElementById('char-xp-label').textContent = `XP: ${xpInLevel} / ${GAME_CONFIG.XP_PER_LEVEL} (Total: ${xpTotal})`;
  document.getElementById('char-xp-bar').style.width = `${progressPct}%`;
  
  // Stats Tab Cards
  document.getElementById('stat-pending').textContent = state.misiones.filter(m => m.estado === 'pendiente').length;
  document.getElementById('stat-completed').textContent = stats.misiones_completadas;
  document.getElementById('stat-xp').textContent = xpTotal;

  // Stats Tab Progress
  document.getElementById('stats-progress-label').textContent = `Progreso en Nivel ${level}`;
  document.getElementById('stats-xp-bar').style.width = `${progressPct}%`;
  document.getElementById('stats-xp-progress-pct').textContent = `${progressPct.toFixed(1)}%`;
  document.getElementById('stats-xp-progress-val').textContent = `${xpInLevel} / ${GAME_CONFIG.XP_PER_LEVEL}`;

  // History List
  const historyContainer = document.getElementById('history-list');
  if (state.historial.length === 0) {
    historyContainer.innerHTML = `
      <div class="no-quests" style="padding: 1.5rem 1rem; font-size: 0.95rem;">
        Sin misiones completadas aún
      </div>
    `;
  } else {
    historyContainer.innerHTML = state.historial.map(item => `
      <div class="history-item">
        <div class="history-desc">✅ ${escapeHTML(item.descripcion)}</div>
        <div class="history-meta">
          <span class="history-xp">⭐ ${item.xp} XP</span>
          <span>${item.fecha_completada || 'Fecha desconocida'}</span>
        </div>
      </div>
    `).join('');
  }
}

// RENDER ACTIVE QUEST CARDS
function renderQuests() {
  const container = document.getElementById('quest-list');
  const countBadge = document.getElementById('misiones-count');
  
  const pendientes = state.misiones.filter(m => m.estado === 'pendiente');
  countBadge.textContent = `${pendientes.length}/${GAME_CONFIG.MAX_MISIONES}`;
  
  if (pendientes.length === 0) {
    container.innerHTML = `
      <div class="no-quests">
        🚫 No hay misiones activas<br>¡Crea una nueva!
      </div>
    `;
    return;
  }
  
  container.innerHTML = pendientes.map(m => `
    <div class="quest-card" id="quest-card-${m.id}">
      <div class="quest-header">
        <div class="quest-description">[ID: ${m.id}] ${escapeHTML(m.descripcion)}</div>
      </div>
      <div class="quest-meta">
        <span class="quest-xp">
          <span class="material-icons" style="font-size: 18px; color: var(--text-secondary);">star</span>
          ${m.xp} XP
        </span>
        <span class="status-badge ${m.estado}">${m.estado === 'pendiente' ? 'pendiente' : 'completada'}</span>
      </div>
      <div class="quest-actions">
        <button class="btn btn-success btn-completar" data-id="${m.id}" data-xp="${m.xp}">
          <span class="material-icons">check</span> Completar
        </button>
        <button class="btn btn-danger btn-eliminar" data-id="${m.id}">
          <span class="material-icons">delete</span> Eliminar
        </button>
      </div>
    </div>
  `).join('');

  // Add event listeners dynamically
  container.querySelectorAll('.btn-completar').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = parseInt(btn.dataset.id);
      const xp = parseInt(btn.dataset.xp);
      // Confetti starts centered on button click
      const rect = btn.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      
      triggerConfirm(
        "Completar Misión",
        "¿Estás seguro de que completaste esta misión?",
        () => handleCompleteQuest(id, x, y)
      );
    });
  });

  container.querySelectorAll('.btn-eliminar').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = parseInt(btn.dataset.id);
      triggerConfirm(
        "Eliminar Misión",
        "¿Estás seguro de que quieres eliminar esta misión? Esta acción no se puede deshacer.",
        () => handleDeleteQuest(id),
        true // Danger color context
      );
    });
  });
}

// --- ACTION HANDLERS ---

async function fetchAllData() {
  try {
    const [misiones, stats, historial] = await Promise.all([
      apiRequest('/misiones'),
      apiRequest('/estadisticas'),
      apiRequest('/misiones/completadas')
    ]);
    
    state.misiones = misiones || [];
    state.estadisticas = stats || { misiones_pendientes: 0, misiones_completadas: 0, xp_total_ganada: 0 };
    state.historial = historial || [];
    
    renderQuests();
    renderStats();
  } catch (e) {
    showToast("Error al sincronizar datos de la API.", "error");
  }
}

async function handleCreateQuest(descripcion, xp) {
  try {
    soundEffects.playAction();
    const result = await apiRequest('/misiones/auto', 'POST', { descripcion, xp });
    
    if (result) {
      showToast("✅ Misión creada exitosamente", "success");
      
      // Clean form inputs
      document.getElementById('input-descripcion').value = '';
      document.getElementById('input-xp').value = 100;
      document.getElementById('xp-current-display').textContent = '100 XP';
      
      // Load and show active tab
      await fetchAllData();
      
      // Tab redirect on small screens
      if (window.innerWidth < 1024) {
        switchTab('tab-misiones');
      }
    }
  } catch (error) {
    soundEffects.playError();
    showToast(`Error: ${error.message}`, "error");
  }
}

async function handleCompleteQuest(id, clickX, clickY) {
  try {
    const result = await apiRequest(`/misiones/${id}/completar`, 'PUT');
    if (result) {
      soundEffects.playQuestComplete();
      spawnConfetti(clickX, clickY, false);
      showToast("✅ Misión completada con éxito", "success");
      await fetchAllData();
    }
  } catch (error) {
    soundEffects.playError();
    showToast(`Error: ${error.message}`, "error");
  }
}

async function handleDeleteQuest(id) {
  try {
    soundEffects.playDelete();
    const result = await apiRequest(`/misiones/${id}`, 'DELETE');
    showToast("🗑️ Misión eliminada correctamente", "success");
    await fetchAllData();
  } catch (error) {
    soundEffects.playError();
    showToast(`Error: ${error.message}`, "error");
  }
}

// --- NAVIGATION & INTERACTION CONTROLLER ---

function switchTab(targetTabId) {
  state.activeTab = targetTabId;
  
  // Handle tab section display on small screen
  document.querySelectorAll('.tab-content').forEach(section => {
    if (section.id === targetTabId) {
      section.classList.add('active');
    } else {
      section.classList.remove('active');
    }
  });

  // Handle bottom navigation item state
  document.querySelectorAll('.nav-item').forEach(btn => {
    if (btn.dataset.tab === targetTabId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}

// --- CONFIRMATION CUSTOM DIALOG MODAL ---
let confirmCallback = null;
function triggerConfirm(title, bodyText, onAccept, isDanger = false) {
  soundEffects.playAction();
  const overlay = document.getElementById('modal-confirm');
  const titleEl = document.getElementById('confirm-title');
  const bodyEl = document.getElementById('confirm-body');
  const acceptBtn = document.getElementById('btn-confirm-accept');

  titleEl.innerHTML = `<span class="material-icons">${isDanger ? 'warning' : 'help_outline'}</span> ${title}`;
  bodyEl.textContent = bodyText;
  
  if (isDanger) {
    acceptBtn.className = 'btn btn-danger';
  } else {
    acceptBtn.className = 'btn btn-success';
  }

  overlay.classList.add('open');
  confirmCallback = onAccept;
}

function closeConfirm() {
  document.getElementById('modal-confirm').classList.remove('open');
  confirmCallback = null;
}

// --- API CONNECTIONS MODAL ---
function loadApiSettings() {
  const savedSource = localStorage.getItem('rpg_api_source') || 'prod';
  const savedCustom = localStorage.getItem('rpg_api_custom') || 'http://localhost:8000';
  
  state.apiSettings.source = savedSource;
  state.apiSettings.customUrl = savedCustom;
  state.isOfflineMode = (savedSource === 'mock');
  state.connectionStatus = (savedSource === 'mock') ? 'mock' : 'connecting';

  // Select matching radio
  const radio = document.querySelector(`input[name="api-source"][value="${savedSource}"]`);
  if (radio) radio.checked = true;
  document.getElementById('api-custom-url').value = savedCustom;

  updateActiveUrl();
}

function updateActiveUrl() {
  const source = state.apiSettings.source;
  if (source === 'prod') {
    state.apiSettings.activeUrl = 'https://apirpguni.onrender.com';
  } else if (source === 'local') {
    state.apiSettings.activeUrl = 'http://localhost:8000';
  } else if (source === 'custom') {
    state.apiSettings.activeUrl = state.apiSettings.customUrl;
  } else {
    state.apiSettings.activeUrl = ''; // Mock mode
  }
}

function saveApiSettings() {
  const selectedSource = document.querySelector('input[name="api-source"]:checked').value;
  const customVal = document.getElementById('api-custom-url').value.trim();
  
  localStorage.setItem('rpg_api_source', selectedSource);
  if (customVal) {
    localStorage.setItem('rpg_api_custom', customVal);
    state.apiSettings.customUrl = customVal;
  }
  
  state.apiSettings.source = selectedSource;
  state.isOfflineMode = (selectedSource === 'mock');
  state.connectionStatus = (selectedSource === 'mock') ? 'mock' : 'connecting';
  
  updateActiveUrl();
  updateConnectionIndicator();
  document.getElementById('modal-api-config').classList.remove('open');
  
  showToast(`Conectado en Modo: ${selectedSource.toUpperCase()}`, "success");
  
  // Reload data
  fetchAllData();
}

// --- HELPERS ---
function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

// --- INITIALIZE APPLICATION ---
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initial State Settings
  loadApiSettings();
  updateConnectionIndicator();
  
  // 2. Setup Navigation Tab switches
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      soundEffects.playAction();
      switchTab(btn.dataset.tab);
    });
  });

  // 3. Slider dynamic changes
  const xpSlider = document.getElementById('input-xp');
  const xpDisplay = document.getElementById('xp-current-display');
  xpSlider.addEventListener('input', () => {
    xpDisplay.textContent = `${xpSlider.value} XP`;
  });

  // 4. Create Mission form submission
  document.getElementById('form-crear-mision').addEventListener('submit', (e) => {
    e.preventDefault();
    const descripcion = document.getElementById('input-descripcion').value.trim();
    const xp = parseInt(xpSlider.value);
    
    if (descripcion) {
      handleCreateQuest(descripcion, xp);
    }
  });

  // 5. Setup Action Modal Handlers
  document.getElementById('btn-confirm-cancel').addEventListener('click', () => {
    soundEffects.playAction();
    closeConfirm();
  });
  
  document.getElementById('btn-confirm-accept').addEventListener('click', () => {
    if (confirmCallback) confirmCallback();
    closeConfirm();
  });

  // 6. Setup API modal configuration
  document.getElementById('btn-api-config').addEventListener('click', () => {
    soundEffects.playAction();
    document.getElementById('modal-api-config').classList.add('open');
  });

  document.getElementById('btn-api-close').addEventListener('click', () => {
    soundEffects.playAction();
    document.getElementById('modal-api-config').classList.remove('open');
  });

  document.getElementById('btn-api-save').addEventListener('click', () => {
    soundEffects.playAction();
    saveApiSettings();
  });

  // Enable synth activation on first clicks
  window.addEventListener('click', () => soundEffects.init(), { once: true });
  window.addEventListener('touchstart', () => soundEffects.init(), { once: true });

  // 7. Load Data on bootstrap
  fetchAllData();
});
