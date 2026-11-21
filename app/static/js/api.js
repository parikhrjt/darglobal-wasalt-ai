/**
 * DarGlobal & Wasalt API Client
 */

const API = {
  sessionId: localStorage.getItem('dg_session_id') || ('sess_' + Math.random().toString(36).substring(2, 10)),

  init() {
    localStorage.setItem('dg_session_id', this.sessionId);
  },

  async sendMessage(message) {
    const model = localStorage.getItem('dg_model') || 'meta-llama/llama-3.3-70b-instruct:free';
    const apiKey = localStorage.getItem('dg_api_key') || '';

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        session_id: this.sessionId,
        model,
        api_key: apiKey
      })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to process request');
    }
    return res.json();
  },

  async getProperties(source = null) {
    let url = '/api/properties?limit=50';
    if (source && source !== 'all') {
      url += `&source=${encodeURIComponent(source)}`;
    }
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch properties');
    return res.json();
  },

  async getProperty(id) {
    const res = await fetch(`/api/properties/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error('Property not found');
    return res.json();
  },

  async bookConsultation(payload) {
    const res = await fetch('/api/consultation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Booking failed');
    return res.json();
  },

  async getModels() {
    const res = await fetch('/api/models');
    if (!res.ok) throw new Error('Failed to fetch models');
    return res.json();
  }
};

API.init();
