class DynamicLabelDashboardPanel extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this._loaded) {
      this._loaded = true;
      this.attachShadow({ mode: 'open' });
      this.load();
    }
  }

  async load() {
    this.render('Loading debug snapshot...');
    try {
      const data = await this._hass.callWS({ type: 'dynamic_label_dashboard/debug_snapshot' });
      this.renderData(data);
    } catch (err) {
      this.render(`Error loading debug snapshot: ${err?.message || err}`);
    }
  }

  render(text) {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display:block; padding:16px; color: var(--primary-text-color); }
        .card { background: var(--card-background-color); border-radius: 12px; padding: 16px; box-shadow: var(--ha-card-box-shadow, none); }
        pre { white-space: pre-wrap; word-break: break-word; font-size: 12px; }
        h1,h2 { margin: 0 0 12px; }
      </style>
      <div class="card">
        <h1>Dynamic Label Dashboard</h1>
        <pre>${text}</pre>
      </div>
    `;
  }

  renderData(data) {
    const summary = {
      counts: data.counts,
      labels: data.labels.slice(0, 20),
      floors: data.floors,
      areas: data.areas.slice(0, 50),
      devices: data.devices.slice(0, 25),
      entities: data.entities.slice(0, 40),
    };
    this.render(JSON.stringify(summary, null, 2));
  }
}

customElements.define('dynamic-label-dashboard-panel', DynamicLabelDashboardPanel);
