import React, { useState, useEffect } from 'react';
import SELECTORS from '../data/selectors.json';

export default function SidebarSettings({ config, onConfigChange }) {
    const [update, setUpdate] = useState(null);
    const [checking, setChecking] = useState(false);

    useEffect(() => { runCheck(false); }, []);

    async function runCheck(force) {
        if (!window.updatesAPI) {
            setUpdate({ error: 'unavailable' });
            return;
        }
        setChecking(true);
        const minDelay = new Promise(r => setTimeout(r, 400));
        try {
            const [result] = await Promise.all([
                window.updatesAPI.check(force ? { force: true } : undefined),
                minDelay
            ]);
            setUpdate(result);
        } catch {
            setUpdate({ error: 'offline' });
        }
        setChecking(false);
    }

    function renderUpdateLink() {
        if (checking) {
            return <button className="meta-link" disabled>Checking…</button>;
        }
        if (update && update.error) {
            return <button className="meta-link error" onClick={() => runCheck(true)}>Retry</button>;
        }
        if (update && update.hasUpdate) {
            return (
                <button
                    className="meta-link"
                    onClick={() => window.windowAPI.openExternal(update.downloadUrl)}
                >
                    Update v{String(update.latest).replace(/^v/, '')}
                </button>
            );
        }
        if (update) {
            return (
                <button className="meta-link" onClick={() => runCheck(true)} title="Check again">
                    Up to date
                </button>
            );
        }
        return <button className="meta-link" onClick={() => runCheck(true)}>Check for updates</button>;
    }

    const versionText = update?.current ? `v${update.current}` : 'Claude Resolve';

    return (
        <div className="settings">
            <div className="sb-title"><span>Settings</span></div>

            <div className="set-row">
                <label>Model</label>
                <select
                    className="select"
                    value={SELECTORS.models.some(m => m.value === config.model) ? config.model : 'sonnet'}
                    onChange={e => onConfigChange({ model: e.target.value })}
                >
                    {SELECTORS.models.map(m => (
                        <option key={m.value} value={m.value}>{m.label} · {m.sub}</option>
                    ))}
                </select>
            </div>

            <div className="set-row">
                <label>Effort</label>
                <select
                    className="select"
                    value={SELECTORS.effort.some(e => e.value === config.effort) ? config.effort : 'auto'}
                    onChange={e => onConfigChange({ effort: e.target.value })}
                >
                    {SELECTORS.effort.map(e => (
                        <option key={e.value} value={e.value}>{e.label}</option>
                    ))}
                </select>
            </div>

            <div className="set-row">
                <label>FPS</label>
                <select
                    className="select"
                    value={config.fps}
                    onChange={e => onConfigChange({ fps: Number(e.target.value) })}
                >
                    <option value={24}>24</option>
                    <option value={25}>25</option>
                    <option value={30}>30</option>
                    <option value={60}>60</option>
                </select>
            </div>

            <div className="set-row">
                <label>Resolution</label>
                <select
                    className="select"
                    value={`${config.width}x${config.height}`}
                    onChange={e => {
                        const [w, h] = e.target.value.split('x').map(Number);
                        onConfigChange({ width: w, height: h });
                    }}
                >
                    <option value="1920x1080">1920 × 1080</option>
                    <option value="3840x2160">3840 × 2160</option>
                    <option value="1080x1920">1080 × 1920 (vertical)</option>
                </select>
            </div>

            <div className="meta-line">
                <span>{versionText}</span>
                {renderUpdateLink()}
            </div>
        </div>
    );
}
