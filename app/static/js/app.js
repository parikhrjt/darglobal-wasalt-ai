/**
 * DarGlobal × Wasalt AI Advisor Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // Lucide Icons init
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // App State
  const state = {
    currency: localStorage.getItem('dg_currency') || 'SAR',
    lang: localStorage.getItem('dg_lang') || 'en',
    rates: {
      USD: 1.0,
      AED: 3.6725,
      SAR: 3.75,
      GBP: 0.80,
      EUR: 0.93
    },
    currencySymbols: {
      USD: '$',
      AED: 'AED ',
      SAR: 'SAR ',
      GBP: '£',
      EUR: '€'
    }
  };

  // DOM Elements
  const messagesContainer = document.getElementById('messagesContainer');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  const currencySelector = document.getElementById('currencySelector');
  const langToggleBtn = document.getElementById('langToggleBtn');
  const langLabel = document.getElementById('langLabel');
  const activeModelLabel = document.getElementById('activeModelLabel');
  
  // Modals & Drawers
  const propertyModal = document.getElementById('propertyModal');
  const propertyModalContent = document.getElementById('propertyModalContent');
  const closePropertyModalBtn = document.getElementById('closePropertyModalBtn');

  const bookingModal = document.getElementById('bookingModal');
  const closeBookingModalBtn = document.getElementById('closeBookingModalBtn');
  const bookingForm = document.getElementById('bookingForm');
  const bookingSuccessBox = document.getElementById('bookingSuccessBox');
  const bookingRefText = document.getElementById('bookingRefText');

  const settingsModal = document.getElementById('settingsModal');
  const settingsModalBtn = document.getElementById('settingsModalBtn');
  const openModelSettingsBtn = document.getElementById('openModelSettingsBtn');
  const closeSettingsModalBtn = document.getElementById('closeSettingsModalBtn');
  const saveSettingsBtn = document.getElementById('saveSettingsBtn');
  const modelSelect = document.getElementById('modelSelect');
  const apiKeyInput = document.getElementById('apiKeyInput');

  const catalogDrawer = document.getElementById('catalogDrawer');
  const openCatalogBtn = document.getElementById('openCatalogBtn');
  const closeCatalogBtn = document.getElementById('closeCatalogBtn');
  const catalogList = document.getElementById('catalogList');
  const catalogFilterBtns = document.querySelectorAll('.catalog-filter-btn');

  // Initialize values
  currencySelector.value = state.currency;
  const savedModel = localStorage.getItem('dg_model') || 'meta-llama/llama-3.3-70b-instruct:free';
  activeModelLabel.innerText = savedModel;
  modelSelect.value = savedModel;
  apiKeyInput.value = localStorage.getItem('dg_api_key') || '';

  // Currency Converter Utility
  function formatPrice(priceUsd) {
    if (!priceUsd) return 'Price on Request';
    const rate = state.rates[state.currency] || 1.0;
    const converted = Math.round(priceUsd * rate);
    const symbol = state.currencySymbols[state.currency] || '$';
    return `${symbol}${converted.toLocaleString()}`;
  }

  // Currency Change Handler
  currencySelector.addEventListener('change', (e) => {
    state.currency = e.target.value;
    localStorage.setItem('dg_currency', state.currency);
    document.querySelectorAll('[data-price-usd]').forEach(el => {
      const usd = parseFloat(el.getAttribute('data-price-usd'));
      el.innerText = formatPrice(usd);
    });
  });

  // Language Toggle Handler
  function applyLanguage(lang) {
    state.lang = lang;
    localStorage.setItem('dg_lang', lang);
    if (lang === 'ar') {
      document.documentElement.setAttribute('dir', 'rtl');
      langLabel.innerText = 'English';
      chatInput.placeholder = 'اسأل عن مشاريع دار الأركان العالمية، فلل الرياض في وصلت، أو احسب العائد الاستثماري...';
    } else {
      document.documentElement.removeAttribute('dir');
      langLabel.innerText = 'العربية';
      chatInput.placeholder = 'Ask about luxury developments, Riyadh villas, ROI models, or book a private viewing...';
    }
  }

  langToggleBtn.addEventListener('click', () => {
    applyLanguage(state.lang === 'en' ? 'ar' : 'en');
  });

  if (state.lang === 'ar') {
    applyLanguage('ar');
  }

  // Settings Modal Handlers
  function openSettings() { settingsModal.classList.remove('hidden'); }
  function closeSettings() { settingsModal.classList.add('hidden'); }
  settingsModalBtn.addEventListener('click', openSettings);
  openModelSettingsBtn.addEventListener('click', openSettings);
  closeSettingsModalBtn.addEventListener('click', closeSettings);

  saveSettingsBtn.addEventListener('click', () => {
    const chosenModel = modelSelect.value;
    const key = apiKeyInput.value.trim();
    localStorage.setItem('dg_model', chosenModel);
    localStorage.setItem('dg_api_key', key);
    activeModelLabel.innerText = chosenModel;
    closeSettings();
    alert('AI settings saved successfully.');
  });

  // Catalog Drawer Handlers
  openCatalogBtn.addEventListener('click', () => {
    catalogDrawer.classList.add('open');
    loadCatalog('all');
  });
  closeCatalogBtn.addEventListener('click', () => {
    catalogDrawer.classList.remove('open');
  });

  catalogFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      catalogFilterBtns.forEach(b => {
        b.classList.remove('bg-brand-gold', 'text-brand-charcoal');
        b.classList.add('bg-brand-charcoal', 'text-slate-300');
      });
      btn.classList.add('bg-brand-gold', 'text-brand-charcoal');
      btn.classList.remove('bg-brand-charcoal', 'text-slate-300');
      loadCatalog(btn.getAttribute('data-filter'));
    });
  });

  async function loadCatalog(filter = 'all') {
    catalogList.innerHTML = '<div class="text-xs text-brand-muted p-4 text-center">Loading properties...</div>';
    try {
      const data = await API.getProperties(filter);
      catalogList.innerHTML = '';
      if (!data.properties || data.properties.length === 0) {
        catalogList.innerHTML = '<div class="text-xs text-brand-muted p-4 text-center">No properties found.</div>';
        return;
      }
      data.properties.forEach(p => {
        const item = document.createElement('div');
        item.className = 'property-card p-3 rounded-xl border border-brand-surfaceBorder space-y-2 cursor-pointer';
        item.innerHTML = `
          <div class="h-32 rounded-lg bg-cover bg-center" style="background-image: url('${p.hero_image_url || 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=80'}')"></div>
          <div>
            <div class="flex items-center justify-between text-[10px] text-brand-gold font-semibold uppercase">
              <span>${p.source}</span>
              <span>${p.brand_partner || ''}</span>
            </div>
            <h4 class="font-serif font-bold text-sm text-white truncate">${p.name}</h4>
            <p class="text-xs text-brand-muted truncate">${p.neighborhood}, ${p.city}</p>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-brand-surfaceBorder">
              <span class="text-xs font-bold text-brand-gold" data-price-usd="${p.price_usd}">${formatPrice(p.price_usd)}</span>
              <span class="text-[10px] text-slate-400">${p.bedrooms_display}</span>
            </div>
          </div>
        `;
        item.addEventListener('click', () => {
          openPropertyModal(p.id);
        });
        catalogList.appendChild(item);
      });
    } catch (e) {
      catalogList.innerHTML = `<div class="text-xs text-red-400 p-4 text-center">Failed to load catalog: ${e.message}</div>`;
    }
  }

  // Quick prompt chips
  document.querySelectorAll('.prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const text = chip.innerText.replace(/^[^\w\s\u0600-\u06FF]+/, '').trim();
      chatInput.value = text;
      handleSendMessage(text);
    });
  });

  // Chat Form Submit
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;
    chatInput.value = '';
    handleSendMessage(message);
  });

  async function handleSendMessage(message) {
    appendUserMessage(message);
    setTyping(true);

    try {
      const data = await API.sendMessage(message);
      setTyping(false);
      appendAgentMessage(data);
    } catch (err) {
      setTyping(false);
      appendAgentErrorMessage(err.message || 'Error communicating with AI engine.');
    }
  }

  function setTyping(isTyping) {
    if (isTyping) {
      typingIndicator.classList.remove('hidden');
      typingIndicator.classList.add('flex');
      sendBtn.disabled = true;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } else {
      typingIndicator.classList.add('hidden');
      typingIndicator.classList.remove('flex');
      sendBtn.disabled = false;
    }
  }

  function appendUserMessage(text) {
    const bubble = document.createElement('div');
    bubble.className = 'flex justify-end';
    bubble.innerHTML = `
      <div class="user-bubble max-w-xl text-slate-100 px-4 py-3 rounded-2xl rounded-tr-none text-sm shadow-md">
        <p class="leading-relaxed">${escapeHtml(text)}</p>
      </div>
    `;
    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendAgentMessage(data) {
    const bubble = document.createElement('div');
    bubble.className = 'flex justify-start space-x-3';
    
    // Parse markdown
    const formattedHtml = marked.parse(data.response || '');

    // Tools badge
    let toolsHtml = '';
    if (data.tools_executed && data.tools_executed.length > 0) {
      const toolNames = data.tools_executed.map(t => `<span class="bg-brand-charcoal text-brand-gold px-1.5 py-0.5 rounded border border-brand-surfaceBorder font-mono">${t.tool}</span>`).join(' ');
      toolsHtml = `
        <div class="mb-3 text-[11px] text-brand-muted flex items-center space-x-1.5">
          <i data-lucide="zap" class="w-3.5 h-3.5 text-brand-gold"></i>
          <span>Executed Autonomous Tools: ${toolNames}</span>
        </div>
      `;
    }

    // Property Cards Section
    let cardsHtml = '';
    if (data.cards && data.cards.length > 0) {
      const cardItems = data.cards.map(p => `
        <div class="property-card rounded-xl p-3 flex flex-col justify-between border border-brand-surfaceBorder">
          <div class="relative h-32 rounded-lg bg-cover bg-center overflow-hidden mb-2" style="background-image: url('${p.hero_image_url || 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=80'}')">
            <span class="absolute top-2 left-2 bg-brand-charcoal/90 text-brand-gold text-[10px] font-bold px-2 py-0.5 rounded border border-brand-gold/30">
              ${p.source}
            </span>
            ${p.brand_partner && !p.brand_partner.includes('Marketplace') ? `
              <span class="absolute top-2 right-2 bg-brand-gold text-brand-charcoal text-[9px] font-extrabold px-1.5 py-0.5 rounded uppercase">
                ${p.brand_partner}
              </span>
            ` : ''}
          </div>
          <div>
            <h4 class="font-serif font-bold text-sm text-white truncate">${p.name}</h4>
            <p class="text-xs text-brand-muted truncate mb-2">${p.neighborhood}, ${p.city}</p>
            <div class="flex items-center justify-between text-xs py-1 border-t border-brand-surfaceBorder/60">
              <span class="text-brand-gold font-bold" data-price-usd="${p.price_usd}">${formatPrice(p.price_usd)}</span>
              <span class="text-slate-300 font-medium">${p.bedrooms_display || p.bedrooms}</span>
            </div>
            <div class="flex items-center justify-between text-[11px] text-brand-muted pt-1">
              <span>ROI: <strong class="text-emerald-400">${p.projected_roi_pct || 8.0}%</strong></span>
              <span>${p.golden_visa_eligible ? '✅ Golden Visa' : ''}</span>
            </div>
          </div>
          <div class="flex space-x-1.5 mt-3 pt-2 border-t border-brand-surfaceBorder">
            <button onclick="openPropertyModal('${p.id}')" class="flex-1 bg-brand-charcoal hover:bg-brand-surfaceBorder text-slate-200 text-[11px] py-1.5 rounded-lg border border-brand-surfaceBorder text-center font-medium transition-colors">
              Details
            </button>
            <button onclick="openBookingModal('${p.id}', '${escapeAttr(p.name)}')" class="flex-1 bg-brand-gold hover:bg-brand-goldLight text-brand-charcoal text-[11px] py-1.5 rounded-lg font-bold text-center transition-colors">
              Book Viewing
            </button>
          </div>
        </div>
      `).join('');

      cardsHtml = `
        <div class="mt-4 pt-3 border-t border-brand-surfaceBorder/80">
          <p class="text-xs font-serif font-bold text-brand-gold mb-3 flex items-center space-x-1.5">
            <i data-lucide="building" class="w-4 h-4"></i>
            <span>Featured Luxury Developments & Verified Listings:</span>
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            ${cardItems}
          </div>
        </div>
      `;
    }

    bubble.innerHTML = `
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-gold to-brand-goldDark flex items-center justify-center flex-shrink-0 shadow-md shadow-brand-gold/10 mt-1">
        <i data-lucide="gem" class="w-4 h-4 text-brand-charcoal"></i>
      </div>
      <div class="agent-bubble max-w-2xl text-slate-200 p-5 rounded-2xl rounded-tl-none shadow-xl border border-brand-surfaceBorder flex-1">
        ${toolsHtml}
        <div class="markdown-content text-sm text-slate-200 leading-relaxed">
          ${formattedHtml}
        </div>
        ${cardsHtml}
        <div class="mt-3 pt-2 border-t border-brand-surfaceBorder/40 flex items-center justify-between text-[10px] text-brand-muted">
          <span>${data.engine || 'DarGlobal AI'}</span>
          <span>REGA Compliant</span>
        </div>
      </div>
    `;

    messagesContainer.appendChild(bubble);
    if (window.lucide) window.lucide.createIcons();
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendAgentErrorMessage(errorText) {
    const bubble = document.createElement('div');
    bubble.className = 'flex justify-start space-x-3';
    bubble.innerHTML = `
      <div class="w-8 h-8 rounded-lg bg-red-500/20 text-red-400 border border-red-500/30 flex items-center justify-center flex-shrink-0 mt-1">
        <i data-lucide="alert-triangle" class="w-4 h-4"></i>
      </div>
      <div class="agent-bubble max-w-xl text-red-200 p-4 rounded-2xl rounded-tl-none shadow-xl border border-red-500/30 text-sm">
        <p class="font-bold mb-1">Execution Notice</p>
        <p class="text-xs text-red-300 leading-relaxed">${escapeHtml(errorText)}</p>
      </div>
    `;
    messagesContainer.appendChild(bubble);
    if (window.lucide) window.lucide.createIcons();
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Property Details Modal Inspection
  window.openPropertyModal = async function(propId) {
    propertyModal.classList.remove('hidden');
    propertyModalContent.innerHTML = '<div class="text-sm text-brand-muted text-center py-12">Loading full architectural dossier...</div>';

    try {
      const p = await API.getProperty(propId);
      const amenitiesHtml = (p.amenities || []).map(a => `
        <li class="flex items-center space-x-2 text-xs text-slate-300">
          <i data-lucide="check" class="w-3.5 h-3.5 text-brand-gold flex-shrink-0"></i>
          <span>${a}</span>
        </li>
      `).join('');

      propertyModalContent.innerHTML = `
        <div class="space-y-5">
          <div class="relative h-64 sm:h-80 rounded-xl bg-cover bg-center overflow-hidden" style="background-image: url('${p.hero_image_url}')">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
            <div class="absolute bottom-4 left-4 right-4 flex items-end justify-between">
              <div>
                <span class="bg-brand-gold text-brand-charcoal text-xs font-extrabold px-2 py-0.5 rounded uppercase">
                  ${p.brand_partner || p.source}
                </span>
                <h3 class="font-serif font-bold text-xl sm:text-2xl text-white mt-1">${p.name}</h3>
                <p class="text-xs text-slate-300 flex items-center space-x-1 mt-0.5">
                  <i data-lucide="map-pin" class="w-3.5 h-3.5 text-brand-gold"></i>
                  <span>${p.neighborhood}, ${p.city}, ${p.country}</span>
                </p>
              </div>
              <div class="text-right">
                <span class="text-xs text-brand-muted block">Starting Price</span>
                <span class="font-serif font-bold text-xl text-brand-gold" data-price-usd="${p.price_usd}">${formatPrice(p.price_usd)}</span>
              </div>
            </div>
          </div>

          <!-- Specs Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-brand-charcoal/70 p-4 rounded-xl border border-brand-surfaceBorder text-center">
            <div>
              <span class="text-[10px] text-brand-muted uppercase block">Bedrooms</span>
              <span class="font-bold text-sm text-white">${p.bedrooms_display}</span>
            </div>
            <div>
              <span class="text-[10px] text-brand-muted uppercase block">Bathrooms</span>
              <span class="font-bold text-sm text-white">${p.bathrooms_display}</span>
            </div>
            <div>
              <span class="text-[10px] text-brand-muted uppercase block">Living Area</span>
              <span class="font-bold text-sm text-white">${p.area_display}</span>
            </div>
            <div>
              <span class="text-[10px] text-brand-muted uppercase block">Projected ROI</span>
              <span class="font-bold text-sm text-emerald-400">${p.projected_roi_pct}% Net</span>
            </div>
          </div>

          <!-- Description -->
          <div>
            <h4 class="font-serif font-bold text-sm text-brand-gold mb-1">Architectural Overview</h4>
            <p class="text-xs text-slate-300 leading-relaxed">${p.description}</p>
          </div>

          <!-- Payment Plan & Status -->
          <div class="p-4 bg-brand-charcoal/50 rounded-xl border border-brand-surfaceBorder/80 space-y-2">
            <h4 class="font-serif font-bold text-sm text-brand-gold">Payment & Handover Milestones</h4>
            <div class="flex flex-wrap items-center justify-between text-xs text-slate-300 gap-2">
              <div><strong>Status:</strong> ${p.completion_status} (${p.completion_date})</div>
              <div><strong>Terms:</strong> ${p.payment_plan}</div>
              <div><strong>Golden Visa:</strong> ${p.golden_visa_eligible ? '✅ Fully Eligible' : 'N/A'}</div>
            </div>
          </div>

          <!-- Amenities -->
          <div>
            <h4 class="font-serif font-bold text-sm text-brand-gold mb-2">Signature Amenities</h4>
            <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              ${amenitiesHtml}
            </ul>
          </div>

          <!-- Modal Action Footer -->
          <div class="flex items-center space-x-3 pt-4 border-t border-brand-surfaceBorder">
            <a href="${p.url}" target="_blank" class="flex-1 bg-brand-charcoal hover:bg-brand-surfaceBorder border border-brand-surfaceBorder text-slate-200 text-xs py-2.5 rounded-xl font-bold text-center transition-colors">
              View Official Portal
            </a>
            <button onclick="openBookingModal('${p.id}', '${escapeAttr(p.name)}')" class="flex-1 bg-gradient-to-r from-brand-gold to-brand-goldDark text-brand-charcoal text-xs py-2.5 rounded-xl font-bold text-center hover:brightness-110 transition-all">
              Schedule VIP Private Viewing
            </button>
          </div>
        </div>
      `;
      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      propertyModalContent.innerHTML = `<div class="text-xs text-red-400 p-6 text-center">Failed to load property: ${e.message}</div>`;
    }
  };

  closePropertyModalBtn.addEventListener('click', () => {
    propertyModal.classList.add('hidden');
  });

  // Booking Modal Logic
  window.openBookingModal = function(propId, propName) {
    propertyModal.classList.add('hidden');
    document.getElementById('bookingPropId').value = propId || '';
    document.getElementById('bookingPropName').value = propName || '';
    bookingForm.classList.remove('hidden');
    bookingSuccessBox.classList.add('hidden');
    bookingModal.classList.remove('hidden');
  };

  closeBookingModalBtn.addEventListener('click', () => {
    bookingModal.classList.add('hidden');
  });

  bookingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      client_name: document.getElementById('bookingName').value,
      email: document.getElementById('bookingEmail').value,
      phone: document.getElementById('bookingPhone').value,
      property_id: document.getElementById('bookingPropId').value,
      property_name: document.getElementById('bookingPropName').value,
      notes: document.getElementById('bookingNotes').value
    };

    try {
      const res = await API.bookConsultation(payload);
      bookingForm.classList.add('hidden');
      bookingSuccessBox.classList.remove('hidden');
      bookingRefText.innerText = `Confirmation Reference: ${res.booking.booking_reference}. Our Senior Portfolio Director will reach out within 24 hours.`;
      if (window.lucide) window.lucide.createIcons();
    } catch (err) {
      alert('Booking failed: ' + err.message);
    }
  });

  // Utilities
  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeAttr(str) {
    if (!str) return '';
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
  }
});
