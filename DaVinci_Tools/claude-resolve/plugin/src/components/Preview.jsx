import React, { useRef, useState, useEffect, useMemo, memo } from 'react';

// Module-level singleton: fetched once per session, shared across all Preview
// instances. The bundle is ~1.2 MB (UMDs + base64 fonts), no point re-fetching.
let cachedBundle = null;
let pendingBundle = null;
function loadBundle() {
    if (cachedBundle) return Promise.resolve(cachedBundle);
    if (!pendingBundle) {
        pendingBundle = window.previewAPI.getRealtimeBundle()
            .then(b => { cachedBundle = b; return b; })
            .catch(() => { pendingBundle = null; return { umd: '', fonts: '' }; });
    }
    return pendingBundle;
}

function injectIntoHead(html, content) {
    if (html.includes('<head>')) return html.replace('<head>', '<head>' + content);
    if (html.includes('<html>')) return html.replace('<html>', '<html><head>' + content + '</head>');
    return '<head>' + content + '</head>' + html;
}

function injectBeforeBodyClose(html, content) {
    if (html.includes('</body>')) return html.replace('</body>', content + '</body>');
    if (html.includes('</html>')) return html.replace('</html>', content + '</html>');
    return html + content;
}

const FRAME_PLAY_SCRIPT = `<script>
document.addEventListener('DOMContentLoaded',function(){
if(typeof window.getAnimationDuration!=='function'||typeof window.renderFrame!=='function')return;
var fps=25,dur=window.getAnimationDuration(),total=Math.ceil(dur*fps);
var running=true,startTime=null,lastFrame=-1;
function tick(ts){
if(!running){startTime=null;requestAnimationFrame(tick);return}
if(!startTime)startTime=ts;
var elapsed=ts-startTime;
var f=Math.floor(elapsed/(1000/fps))%total;
if(f!==lastFrame){window.renderFrame(f,fps);lastFrame=f}
requestAnimationFrame(tick)}
window.addEventListener('message',function(e){if(e.data==='play')running=true;else if(e.data==='pause')running=false});
requestAnimationFrame(tick);
});
<\/script>`;

// Realtime mode helper: postMessage duration back to parent so it can schedule
// the next iframe re-mount and create a perpetual loop.
const REALTIME_DURATION_HELPER = `<script>
window.addEventListener('load', function() {
  try {
    var dur = typeof window.getAnimationDuration === 'function' ? window.getAnimationDuration() : 0;
    if (dur > 0) window.parent.postMessage({ __cr: 'duration', seconds: dur }, '*');
  } catch (_) {}
});
<\/script>`;

const REPLAY_BUFFER_MS = 500;

// Preview scales to fit (contain) within the card width and this max height,
// so vertical/square clips show whole — never cropped. Pure UX cap; tune freely.
const MAX_PREVIEW_H = 420;

const HTMLPreview = memo(function HTMLPreview({ parsed, width, height }) {
    const iframeRef = useRef(null);
    const containerRef = useRef(null);
    const [box, setBox] = useState({ w: 0, h: 0, scale: 1 });
    const [isPlaying, setIsPlaying] = useState(true);
    const [bundle, setBundle] = useState(cachedBundle);
    const [replayKey, setReplayKey] = useState(0);
    const [loopDuration, setLoopDuration] = useState(null);
    const [isVisible, setIsVisible] = useState(true);
    const wasOffscreenRef = useRef(false);

    useEffect(() => {
        if (!bundle) loadBundle().then(setBundle);
    }, [bundle]);

    useEffect(() => {
        // Bump on new HTML and on bundle availability so the iframe is
        // re-mounted with the proper srcdoc once the UMDs/fonts arrive.
        if (bundle) setReplayKey(k => k + 1);
    }, [parsed.html, bundle]);

    // Fit-to-contain: the box takes the clip's aspect ratio (from config
    // width/height), bounded by the card width and MAX_PREVIEW_H. The iframe
    // renders at the clip's real viewport and scales to fill the box — the whole
    // frame is always visible, never cropped; leftover space letterboxes.
    useEffect(() => {
        function updateBox() {
            const availW = containerRef.current && containerRef.current.clientWidth;
            if (!availW) return;
            const ar = width / height;
            let w = availW;
            let h = w / ar;
            if (h > MAX_PREVIEW_H) { h = MAX_PREVIEW_H; w = h * ar; }
            setBox({ w, h, scale: w / width });
        }
        updateBox();
        const obs = new ResizeObserver(updateBox);
        if (containerRef.current) obs.observe(containerRef.current);
        return () => obs.disconnect();
    }, [width, height]);

    // IntersectionObserver: pause loop when iframe scrolls offscreen.
    useEffect(() => {
        if (!containerRef.current) return;
        const obs = new IntersectionObserver(
            ([entry]) => setIsVisible(entry.isIntersecting),
            { threshold: 0.1 }
        );
        obs.observe(containerRef.current);
        return () => obs.disconnect();
    }, []);

    // Listen for the duration handshake from the realtime iframe.
    useEffect(() => {
        if (parsed.mode !== 'realtime') return;
        function onMessage(e) {
            if (e.data && e.data.__cr === 'duration' && typeof e.data.seconds === 'number') {
                setLoopDuration(e.data.seconds);
            }
        }
        window.addEventListener('message', onMessage);
        return () => window.removeEventListener('message', onMessage);
    }, [parsed.mode]);

    // When iframe re-enters the viewport after being offscreen, restart the
    // animation so the user always sees it from frame 0 — not the static
    // end-state that's been sitting there.
    useEffect(() => {
        if (parsed.mode !== 'realtime') return;
        if (isVisible && wasOffscreenRef.current) {
            setReplayKey(k => k + 1);
            wasOffscreenRef.current = false;
        } else if (!isVisible) {
            wasOffscreenRef.current = true;
        }
    }, [isVisible, parsed.mode]);

    // The actual loop: schedule a key bump after duration + buffer.
    // Guarded on visibility — offscreen iframes don't burn CPU.
    useEffect(() => {
        if (parsed.mode !== 'realtime' || !loopDuration || !isVisible) return;
        const id = setTimeout(
            () => setReplayKey(k => k + 1),
            loopDuration * 1000 + REPLAY_BUFFER_MS
        );
        return () => clearTimeout(id);
    }, [parsed.mode, loopDuration, replayKey, isVisible]);

    const srcdoc = useMemo(() => {
        if (!bundle) return '<!DOCTYPE html><html><body style="margin:0;background:#000"></body></html>';

        let html = parsed.html;
        const headInjections = [];
        headInjections.push(bundle.fonts);
        if (parsed.mode === 'realtime') {
            headInjections.push(`<script>${bundle.umd}</script>`);
            headInjections.push(REALTIME_DURATION_HELPER);
        }
        html = injectIntoHead(html, headInjections.join(''));

        if (parsed.mode !== 'realtime') {
            html = injectBeforeBodyClose(html, FRAME_PLAY_SCRIPT);
        }
        return html;
    }, [parsed, bundle]);

    function togglePlay() {
        const next = !isPlaying;
        setIsPlaying(next);
        iframeRef.current?.contentWindow?.postMessage(next ? 'play' : 'pause', '*');
    }

    return (
        <div
            ref={containerRef}
            className="card-preview"
            style={{ height: box.h ? `${box.h}px` : undefined }}
        >
            <div className="card-preview-box" style={{ width: `${box.w}px`, height: `${box.h}px` }}>
                <iframe
                    key={replayKey}
                    ref={iframeRef}
                    className="card-preview-frame"
                    width={width}
                    height={height}
                    sandbox="allow-scripts"
                    srcDoc={srcdoc}
                    style={{ transform: `scale(${box.scale})` }}
                />
                {parsed.mode !== 'realtime' && (
                    <button
                        className={'card-play' + (isPlaying ? '' : ' play-glyph')}
                        onClick={togglePlay}
                    >
                        {isPlaying ? '⏸' : '▶'}
                    </button>
                )}
            </div>
        </div>
    );
});

export default function Preview({ parsed, width, height }) {
    return <HTMLPreview parsed={parsed} width={width || 1920} height={height || 1080} />;
}
