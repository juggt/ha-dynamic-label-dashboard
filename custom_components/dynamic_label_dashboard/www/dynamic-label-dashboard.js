class DynamicLabelDashboardPanel extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this._init) {
      this._init = true;
      this.attachShadow({ mode: 'open' });
      this.load();
    }
  }

  async load() {
    this.renderLoading();
    try {
      const data = await this._hass.callWS({ type: 'dynamic_label_dashboard/dashboard_snapshot' });
      this.renderData(data);
    } catch (err) {
      this.renderError(err);
    }
  }

  renderLoading() {
    this.shadowRoot.innerHTML = this.baseHtml(`<div class="card"><h1>Dynamic Label Dashboard</h1><p>Lade Daten...</p></div>`);
  }

  renderError(err) {
    this.shadowRoot.innerHTML = this.baseHtml(`<div class="card"><h1>Dynamic Label Dashboard</h1><p>Fehler: ${this.escape(err?.message || String(err))}</p></div>`);
  }

  baseHtml(content) {
    return `
      <style>
        :host { display:block; padding:16px; color: var(--primary-text-color); }
        .layout { display:grid; grid-template-columns: 320px 1fr; gap:16px; }
        .card { background: var(--card-background-color); border-radius: 16px; padding: 16px; box-shadow: var(--ha-card-box-shadow, none); }
        h1,h2,h3 { margin: 0 0 12px; }
        .muted { opacity: .75; font-size: 13px; }
        .label-list, .room-list, .item-list { display:flex; flex-direction:column; gap:10px; }
        .label-chip { display:inline-flex; align-items:center; gap:8px; border:1px solid var(--divider-color); border-radius:999px; padding:6px 10px; margin:4px 6px 0 0; font-size:12px; }
        .room { border:1px solid var(--divider-color); border-radius:12px; padding:12px; }
        .room-header { display:flex; justify-content:space-between; gap:12px; align-items:center; margin-bottom:10px; }
        .items { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:10px; }
        .item { border:1px solid var(--divider-color); border-radius:10px; padding:10px; }
        .pill { display:inline-block; padding:2px 8px; border-radius:999px; background: rgba(127,127,127,.15); font-size:12px; margin:2px 6px 0 0; }
        @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } }
      </style>
      ${content}
    `;
  }

  escape(v) {
    return String(v)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  renderData(data) {
    const labelsHtml = (data.labels || []).map(label => {
      const flags = [label.selected_summary ? 'Summary' : '', label.selected_detail ? 'Detail' : ''].filter(Boolean).join(' · ');
      return `<div><span class="label-chip">${this.escape(label.name)}${flags ? ` <span class="muted">${this.escape(flags)}</span>` : ''}</span></div>`;
    }).join('');

    const roomsHtml = (data.rooms || []).map(room => {
      const itemsHtml = (room.items || []).map(item => `
        <div class="item">
          <strong>${this.escape(item.name)}</strong><br>
          <span class="muted">${this.escape(item.id)}</span><br>
          <span>Status: ${this.escape(item.state ?? 'unknown')}</span><br>
          <span class="pill">Match: ${this.escape(item.match_source)}</span>
          ${(item.summary_match || []).map(x => `<span class="pill">S: ${this.escape(x)}</span>`).join('')}
          ${(item.detail_match || []).map(x => `<span class="pill">D: ${this.escape(x)}</span>`).join('')}
        </div>
      `).join('');

      return `
        <div class="room">
          <div class="room-header">
            <div>
              <h3>${this.escape(room.name)}</h3>
              <div class="muted">${this.escape(room.floor_name || 'Ohne Etage')}</div>
            </div>
            <div class="muted">${room.items.length} Treffer</div>
          </div>
          <div class="items">${itemsHtml}</div>
        </div>
      `;
    }).join('');

    const noRoomHtml = (data.no_room || []).map(item => `<div class="item"><strong>${this.escape(item.name)}</strong><br><span class="muted">${this.escape(item.id)}</span></div>`).join('');

    this.shadowRoot.innerHTML = this.baseHtml(`
      <div class="layout">
        <div class="card">
          <h1>Dynamic Label Dashboard</h1>
          <div class="muted">Erster echter Snapshot aus Home Assistant</div>
          <br>
          <div><strong>Version:</strong> ${this.escape(data.version || 'unknown')}</div>
          <div><strong>Labels:</strong> ${this.escape(data.counts?.labels ?? 0)}</div>
          <div><strong>Räume mit Treffern:</strong> ${this.escape(data.counts?.rooms_with_matches ?? 0)}</div>
          <div><strong>Ohne Raum:</strong> ${this.escape(data.counts?.items_without_room ?? 0)}</div>
          <br>
          <h2>Vorhandene Labels</h2>
          <div class="label-list">${labelsHtml || '<div class="muted">Keine Labels gefunden</div>'}</div>
        </div>
        <div class="card">
          <h2>Räume</h2>
          <div class="room-list">${roomsHtml || '<div class="muted">Noch keine Treffer. Aktuell werden nur ausgewählte Labels berücksichtigt.</div>'}</div>
          ${(data.no_room || []).length ? `<br><h2>Ohne Raum</h2><div class="items">${noRoomHtml}</div>` : ''}
        </div>
      </div>
    `);
  }
}

customElements.define('dynamic-label-dashboard-panel', DynamicLabelDashboardPanel);
