/* ============================================================
   ANIMATION SHOWCASE – animations.js
   Parallax scroll system + old showcase animation logic
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // --- GLOBAL REFS ---
    const viewport = document.getElementById('scrollViewport');
    const introOverlay = document.getElementById('introOverlay');
    const sectionLabel = document.getElementById('sectionLabel');
    const dots = document.querySelectorAll('.progress-dot');
    const panels = document.querySelectorAll('.anim-panel');
    const cards = document.querySelectorAll('.content-card');
    const sections = document.querySelectorAll('.content-section');
    const sectionLabels = ['01 — The Reaction', '02 — The Sequence', '03 — The Mechanism'];
    let currentSection = 0;
    let introHidden = false;

    // Hide intro on first scroll
    viewport.addEventListener('scroll', () => {
        if (!introHidden && viewport.scrollTop > 50) {
            introOverlay.classList.add('hidden');
            sectionLabel.classList.add('visible');
            introHidden = true;
        }
    }, { passive: true });

    // Section switching
    function updateSection(newSection) {
        if (newSection === currentSection) return;
        panels.forEach((p, i) => p.classList.toggle('active', i === newSection));
        dots.forEach((d, i) => d.classList.toggle('active', i === newSection));
        sectionLabel.textContent = sectionLabels[newSection];
        currentSection = newSection;
    }

    // Progress dot click navigation
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const s = parseInt(dot.dataset.section);
            sections[s]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });


    /* ============================================================
       BEAKER ANIMATION (from old showcase – full 14 bubbles + pop effects)
       ============================================================ */
    const beakerPanel = document.getElementById('beakerPanel');
    const sceneContainer = beakerPanel?.querySelector('.scene-container');
    const displacementX = beakerPanel?.querySelector('#displacementX');
    const displacementY = beakerPanel?.querySelector('#displacementY');
    const liquidScaler = beakerPanel?.querySelector('#liquid-scaler');
    const wobblePath = beakerPanel?.querySelector('#wobblePath');
    const customPathBubble1 = beakerPanel?.querySelector('#custom-path-bubble-1');
    const popEffectsContainer = beakerPanel?.querySelector('#pop-effects-container');
    const shockwavePool = beakerPanel?.querySelectorAll('#shockwave-pool circle');
    const particlePoolContainer = beakerPanel?.querySelector('#particle-pool');

    // Create particle pool elements (replaces document.write)
    if (particlePoolContainer) {
        for (let i = 0; i < 60; i++) {
            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            g.setAttribute('opacity', '0');
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('r', '3');
            circle.setAttribute('fill', '#f9d3d9');
            g.appendChild(circle);
            particlePoolContainer.appendChild(g);
        }
    }
    const particlePool = beakerPanel?.querySelectorAll('#particle-pool g');

    const wobblePathLength = wobblePath ? wobblePath.getTotalLength() : 150;
    const customPathLength = customPathBubble1 ? customPathBubble1.getTotalLength() : 700;
    const Y_OFFSET = -150;
    const HORIZONTAL_DRIFT = 80;
    const START_Y = { min: 700, max: 780 };
    const ANTICIPATION_MS = 50;
    const SATURATION_START = 0.1;
    let popTriggered = false;
    const lerp = (a, b, t) => a + (b - a) * t;

    // Bubble configs (14 bubbles from old showcase)
    const bubbleConfigs = [
        { elId: 'bubble-1', customPathId: 'custom-path-bubble-1', endScale: 1.37, start: 0.25, end: 1.0 },
        { elId: 'bubble-2', endPos: { x: 349.6, y: 10 + Y_OFFSET }, cp: { x: 330, y: 300 }, endScale: 1.10, start: 0.30, end: 1.0 },
        { elId: 'bubble-3', endPos: { x: 280, y: 50 + Y_OFFSET }, cp1: { x: 180, y: 500 }, cp2: { x: 380, y: 200 }, endScale: 1.00, start: 0.35, end: 1.0 },
        { elId: 'bubble-4', endPos: { x: 378.29, y: 347.6 + Y_OFFSET }, endScale: 1.16, start: 0.40, end: 1.0 },
        { elId: 'bubble-5', endPos: { x: 402.43, y: 477.15 + Y_OFFSET }, endScale: 0.95, start: 0.45, end: 1.0 },
        { elId: 'bubble-6', endPos: { x: 265.98, y: 532.7 + Y_OFFSET }, endScale: 0.89, start: 0.50, end: 1.0 },
        { elId: 'bubble-7', endPos: { x: 379.8, y: 571.53 + Y_OFFSET }, endScale: 0.72, start: 0.55, end: 1.0 },
        { elId: 'bubble-8', endPos: { x: 489.67, y: 663.93 + Y_OFFSET }, endScale: 0.64, start: 0.60, end: 1.0 },
        { elId: 'bubble-9', endPos: { x: 393.89, y: 732.59 + Y_OFFSET }, endScale: 0.64, start: 0.65, end: 1.0 },
        { elId: 'bubble-10', endPos: { x: 290.07, y: 785.19 + Y_OFFSET }, endScale: 0.49, start: 0.70, end: 1.0 },
        { elId: 'bubble-11', endPos: { x: 182.44, y: 872.3 + Y_OFFSET }, endScale: 0.49, start: 0.72, end: 1.0 },
        { elId: 'bubble-12', endPos: { x: 266.06, y: 922.35 + Y_OFFSET }, endScale: 0.29, start: 0.75, end: 1.0 },
        { elId: 'bubble-13', endPos: { x: 474.95, y: 909.27 + Y_OFFSET }, endScale: 0.29, start: 0.78, end: 1.0 },
        { elId: 'bubble-14', endPos: { x: 533.47, y: 849.04 + Y_OFFSET }, endScale: 0.44, start: 0.80, end: 1.0 },
    ].map(cfg => {
        const el = beakerPanel?.querySelector('#' + cfg.elId);
        const result = { ...cfg, el, startScale: 0.1, isPopping: false };
        if (cfg.customPathId) {
            const pathEl = beakerPanel?.querySelector('#' + cfg.customPathId);
            if (pathEl) { result.customPath = pathEl; result.customLen = pathEl.getTotalLength(); }
        } else if (cfg.endPos) {
            result.startPos = {
                x: cfg.endPos.x + (Math.random() - 0.5) * HORIZONTAL_DRIFT,
                y: START_Y.min + Math.random() * (START_Y.max - START_Y.min)
            };
        }
        return result;
    });

    const popBubbles = bubbleConfigs.filter(b => ['bubble-1', 'bubble-2', 'bubble-3'].includes(b.elId));

    function getBubblePos(cfg, t) {
        if (cfg.customPath) {
            const pt = cfg.customPath.getPointAtLength(t * cfg.customLen);
            return { x: pt.x, y: pt.y + Y_OFFSET };
        }
        if (!cfg.endPos || !cfg.startPos) return { x: 0, y: 0 };
        const p0 = cfg.startPos, p3 = cfg.endPos;
        if (cfg.cp1 && cfg.cp2) {
            return {
                x: (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * cfg.cp1.x + 3 * (1 - t) * t ** 2 * cfg.cp2.x + t ** 3 * p3.x,
                y: (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * cfg.cp1.y + 3 * (1 - t) * t ** 2 * cfg.cp2.y + t ** 3 * p3.y,
            };
        }
        if (cfg.cp) {
            return {
                x: (1 - t) ** 2 * p0.x + 2 * (1 - t) * t * cfg.cp.x + t ** 2 * p3.x,
                y: (1 - t) ** 2 * p0.y + 2 * (1 - t) * t * cfg.cp.y + t ** 2 * p3.y,
            };
        }
        const wp = wobblePath ? wobblePath.getPointAtLength(t * wobblePathLength) : { x: 0, y: 0 };
        return { x: lerp(p0.x, p3.x, t) + wp.x, y: lerp(p0.y, p3.y, t) };
    }

    // Pop effects (shockwave + particles)
    let shockIdx = 0, particleIdx = 0;
    function animateShockwave(x, y, initialR) {
        if (!shockwavePool || !popEffectsContainer) return;
        const sw = shockwavePool[shockIdx++ % shockwavePool.length];
        popEffectsContainer.appendChild(sw);
        const dur = 500, start = performance.now();
        (function frame(ts) {
            const p = Math.min((ts - start) / dur, 1);
            const ease = 1 - (1 - p) ** 2;
            sw.setAttribute('cx', x);
            sw.setAttribute('cy', y);
            sw.setAttribute('r', lerp(initialR, initialR + 120, ease));
            sw.style.opacity = lerp(0.7, 0, p);
            if (p < 1) requestAnimationFrame(frame);
        })(performance.now());
    }

    function animateParticles(x, y) {
        if (!particlePool || !popEffectsContainer) return;
        for (let i = 0; i < 20; i++) {
            const particle = particlePool[particleIdx++ % particlePool.length];
            popEffectsContainer.appendChild(particle);
            const angle = Math.random() * Math.PI * 2;
            const dist = lerp(20, 80, Math.random());
            const dur = lerp(400, 800, Math.random());
            const start = performance.now();
            (function frame(ts) {
                const p = Math.min((ts - start) / dur, 1);
                const ease = Math.sin(p * Math.PI / 2);
                particle.style.transform = `translate(${x + Math.cos(angle) * dist * ease}px, ${y + Math.sin(angle) * dist * ease}px)`;
                particle.style.opacity = 1 - p;
                if (p < 1) requestAnimationFrame(frame);
            })(performance.now());
        }
    }

    function animateAnticipation(el, matrix, onComplete) {
        const start = performance.now();
        const initScale = matrix.a, targetScale = initScale * 0.9;
        const px = matrix.e, py = matrix.f;
        (function frame(ts) {
            const p = Math.min((ts - start) / ANTICIPATION_MS, 1);
            el.style.transform = `translate(${px}px, ${py}px) scale(${lerp(initScale, targetScale, p)})`;
            if (p < 1) requestAnimationFrame(frame);
            else onComplete();
        })(performance.now());
    }

    function triggerPop(cfg) {
        const el = cfg.el;
        if (!el || cfg.isPopping) return;
        cfg.isPopping = true;
        const tf = window.getComputedStyle(el).transform;
        if (tf === 'none') return;
        const m = new DOMMatrix(tf);
        animateAnticipation(el, m, () => {
            const px = m.e, py = m.f, sc = m.a * 0.9;
            const dur = 300, start = performance.now();
            (function frame(ts) {
                const p = Math.min((ts - start) / dur, 1);
                el.style.transform = `translate(${px}px, ${py}px) scale(${lerp(sc, sc * 1.67, p)})`;
                el.style.opacity = 1 - p;
                if (p < 1) requestAnimationFrame(frame);
            })(performance.now());
            animateShockwave(px, py, 25 * m.a);
            animateParticles(px, py);
        });
    }

    function triggerFinale() {
        if (popTriggered) return;
        popTriggered = true;
        setTimeout(() => triggerPop(popBubbles[1]), 100);
        setTimeout(() => triggerPop(popBubbles[0]), 20);
        setTimeout(() => triggerPop(popBubbles[2]), 320);
    }

    function updateBeaker(progress) {
        if (!sceneContainer) return;
        const satP = Math.max(0, (progress - SATURATION_START) / (1 - SATURATION_START));
        sceneContainer.style.filter = `url(#underglow) saturate(${satP})`;
        if (liquidScaler) liquidScaler.setAttribute('transform', `scale(${lerp(0.9, 1, progress)})`);
        const amp = Math.sin(progress ** 3 * Math.PI);
        if (displacementX) displacementX.setAttribute('scale', Math.sin(progress * 4 * Math.PI) * 50 * amp);
        if (displacementY) displacementY.setAttribute('scale', Math.sin(progress * 3 * Math.PI) * 50 * amp);

        bubbleConfigs.forEach(cfg => {
            if (!cfg.el || cfg.isPopping) return;
            const seg = (progress - cfg.start) / (cfg.end - cfg.start);
            const t = Math.max(0, Math.min(1, seg));
            if (t > 0) {
                const pos = getBubblePos(cfg, t);
                const sc = lerp(cfg.startScale, cfg.endScale, t);
                cfg.el.style.transform = `translate(${pos.x}px, ${pos.y}px) scale(${sc})`;
                cfg.el.style.opacity = 1;
            } else {
                cfg.el.style.opacity = 0;
            }
        });

        if (progress >= 1.0 && !popTriggered) triggerFinale();
        else if (progress < 0.95 && popTriggered) {
            popTriggered = false;
            popBubbles.forEach(b => b.isPopping = false);
        }
    }


    /* ============================================================
       CONTROLLER ANIMATION (from old showcase – full interactive)
       ============================================================ */
    const controllerContainer = document.getElementById('controllerContainer');
    const dpadLocation = document.getElementById('dpad-location');
    const beams = document.getElementById('transmission-beams');
    const defaultGrommet = dpadLocation?.querySelector('.grommet-graphic-default');
    const activeGrommet = dpadLocation?.querySelector('.grommet-graphic-active');

    // Joystick drag state
    const joystickDragState = { 'l-joystick-assembly': false, 'r-joystick-assembly': false };

    function initJoystick(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const stick = container.querySelector('.joystick-stick');
        const base = container.querySelector('.joystick-base');
        const axis = container.querySelector('.joystick-axis');
        if (!stick || !base || !axis) return;
        let dragging = false;

        const startDrag = e => {
            joystickDragState[containerId] = true;
            dragging = true;
            stick.classList.remove('return-to-center');
            axis.classList.add('is-visible');
            document.addEventListener('mousemove', onDrag);
            document.addEventListener('touchmove', onDrag, { passive: false });
            document.addEventListener('mouseup', endDrag);
            document.addEventListener('touchend', endDrag);
            e.preventDefault();
            e.stopPropagation();
        };

        const onDrag = e => {
            if (!dragging) return;
            e.preventDefault();
            const touch = e.touches ? e.touches[0] : e;
            const rect = base.getBoundingClientRect();
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            const maxR = rect.width / 2;
            let dx = touch.clientX - cx, dy = touch.clientY - cy;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist > maxR) { dx = dx / dist * maxR; dy = dy / dist * maxR; }

            const rotX = 28 * (-dy / maxR), rotY = 28 * (dx / maxR);
            const tx = 8 * (dx / maxR), ty = 8 * (dy / maxR);
            stick.style.setProperty('--rotateX', rotX + 'deg');
            stick.style.setProperty('--rotateY', rotY + 'deg');
            stick.style.setProperty('--translateX', tx + 'px');
            stick.style.setProperty('--translateY', ty + 'px');

            const lx = 35 + rotY / 28 * 20, ly = 35 - rotX / 28 * 20;
            axis.style.setProperty('--axis-light-x', lx + '%');
            axis.style.setProperty('--axis-light-y', ly + '%');

            const sx = 4 + rotY / 28 * 4, sy = 4 - rotX / 28 * 4;
            base.style.setProperty('--grommet-shadow-x', sx + 'px');
            base.style.setProperty('--grommet-shadow-y', sy + 'px');
        };

        const endDrag = () => {
            joystickDragState[containerId] = false;
            if (!dragging) return;
            dragging = false;
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('touchmove', onDrag);
            document.removeEventListener('mouseup', endDrag);
            document.removeEventListener('touchend', endDrag);
            stick.classList.add('return-to-center');
            axis.classList.remove('is-visible');
            stick.style.setProperty('--rotateX', '0deg');
            stick.style.setProperty('--rotateY', '0deg');
            stick.style.setProperty('--translateX', '0px');
            stick.style.setProperty('--translateY', '0px');
            axis.style.setProperty('--axis-light-x', '35%');
            axis.style.setProperty('--axis-light-y', '35%');
            base.style.setProperty('--grommet-shadow-x', '4px');
            base.style.setProperty('--grommet-shadow-y', '4px');
        };

        stick.addEventListener('mousedown', startDrag);
        stick.addEventListener('touchstart', startDrag, { passive: false });
    }

    function setupBumper(triggerId, visualId) {
        const trigger = document.getElementById(triggerId);
        const visual = document.getElementById(visualId);
        if (!trigger || !visual) return;
        const press = e => { visual.classList.add('is-pressed'); e.preventDefault(); };
        const release = () => visual.classList.remove('is-pressed');
        trigger.addEventListener('mousedown', press);
        trigger.addEventListener('mouseup', release);
        trigger.addEventListener('mouseleave', release);
        trigger.addEventListener('touchstart', press, { passive: false });
        trigger.addEventListener('touchend', release);
    }

    function pressDpadGrommet() {
        if (activeGrommet) activeGrommet.style.display = 'block';
        if (defaultGrommet) defaultGrommet.style.display = 'none';
    }
    function releaseDpadGrommet() {
        if (activeGrommet) activeGrommet.style.display = 'none';
        if (defaultGrommet) defaultGrommet.style.display = 'block';
    }

    function setupDpadTriggers() {
        const triggers = dpadLocation?.querySelectorAll('.trigger');
        if (!triggers) return;
        triggers.forEach(trigger => {
            trigger.addEventListener('mousedown', pressDpadGrommet);
            trigger.addEventListener('mouseup', releaseDpadGrommet);
            trigger.addEventListener('mouseleave', releaseDpadGrommet);
            trigger.addEventListener('touchstart', e => { e.preventDefault(); pressDpadGrommet(); }, { passive: false });
            trigger.addEventListener('touchend', e => { e.preventDefault(); releaseDpadGrommet(); });
        });
    }

    // Controller elements lookup
    const ctrlEls = {
        'btn-start':  { press: document.querySelector('#btn-start-location'),  light: document.querySelector('#btn-start-location .start-select-button') },
        'btn-select': { press: document.querySelector('#btn-select-location'), light: document.querySelector('#btn-select-location .start-select-button') },
        'btn-a':      { press: document.querySelector('#btn-a-location .game-button'), light: document.querySelector('#btn-a-location span') },
        'btn-b':      { press: document.querySelector('#btn-b-location .game-button'), light: document.querySelector('#btn-b-location span') },
        'btn-x':      { press: document.querySelector('#btn-x-location .game-button'), light: document.querySelector('#btn-x-location span') },
        'btn-y':      { press: document.querySelector('#btn-y-location .game-button'), light: document.querySelector('#btn-y-location span') },
        'l-bumper':   { press: document.getElementById('l-bumper'), light: null },
        'r-bumper':   { press: document.getElementById('r-bumper'), light: null },
        'dpad':       dpadLocation,
        'l-stick':    { stick: document.getElementById('l-joystick-assembly')?.querySelector('.joystick-stick'), axis: document.getElementById('l-joystick-assembly')?.querySelector('.joystick-axis'), id: 'l-joystick-assembly' },
        'r-stick':    { stick: document.getElementById('r-joystick-assembly')?.querySelector('.joystick-stick'), axis: document.getElementById('r-joystick-assembly')?.querySelector('.joystick-axis'), id: 'r-joystick-assembly' },
    };

    // Animation timeline
    const ctrlTimeline = [
        { type: 'dpad', dir: 'up',    start: 0.05, end: 0.10 },
        { type: 'press', el: ctrlEls['btn-y'], start: 0.10, end: 0.15 },
        { type: 'dpad', dir: 'right', start: 0.15, end: 0.20 },
        { type: 'press', el: ctrlEls['btn-x'], start: 0.20, end: 0.25 },
        { type: 'dpad', dir: 'down',  start: 0.25, end: 0.30 },
        { type: 'press', el: ctrlEls['btn-b'], start: 0.30, end: 0.35 },
        { type: 'dpad', dir: 'left',  start: 0.35, end: 0.40 },
        { type: 'press', el: ctrlEls['btn-a'], start: 0.40, end: 0.45 },
        { type: 'joystick', el: ctrlEls['l-stick'], start: 0.45, end: 0.65 },
        { type: 'joystick', el: ctrlEls['r-stick'], start: 0.50, end: 0.70 },
        { type: 'press', el: ctrlEls['l-bumper'],   start: 0.70, end: 0.78 },
        { type: 'press', el: ctrlEls['r-bumper'],   start: 0.70, end: 0.78 },
        { type: 'press', el: ctrlEls['btn-select'], start: 0.74, end: 0.78 },
        { type: 'press', el: ctrlEls['btn-start'],  start: 0.79, end: 0.83 },
    ];

    let dpadPressedByAnim = false;
    let beamState = 'hidden';

    function updateController(progress) {
        if (!controllerContainer) return;
        controllerContainer.style.filter = `grayscale(${1 - progress})`;

        let anyDpadActive = false;
        ctrlTimeline.forEach(action => {
            const active = progress >= action.start && progress < action.end;
            if (action.type === 'press') {
                if (!action.el?.press) return;
                action.el.press.classList.toggle('is-pressed', active);
                if (action.el.light) action.el.light.classList.toggle('is-lit', active);
                const grommet = action.el.press.closest('.grommet-css, .start-select-assembly');
                if (grommet) grommet.classList.toggle('is-pressed', active);
            } else if (action.type === 'dpad') {
                ctrlEls['dpad']?.classList.toggle('is-pressed-' + action.dir, active);
                if (active) anyDpadActive = true;
            }
        });

        if (anyDpadActive && !dpadPressedByAnim) { pressDpadGrommet(); dpadPressedByAnim = true; }
        else if (!anyDpadActive && dpadPressedByAnim) { releaseDpadGrommet(); dpadPressedByAnim = false; }

        // Joystick rotation (scroll-driven, unless user is dragging)
        ['l-stick', 'r-stick'].forEach(stickId => {
            const s = ctrlEls[stickId];
            if (!s?.stick || joystickDragState[s.id]) return;
            const action = ctrlTimeline.find(a => a.type === 'joystick' && a.el?.id === s.id && progress >= a.start && progress < a.end);
            if (action) {
                s.axis?.classList.add('is-visible');
                const t = (progress - action.start) / (action.end - action.start);
                const angle = t * 2 * Math.PI;
                const x = Math.cos(angle), y = Math.sin(angle);
                s.stick.style.setProperty('--rotateX', (28 * y * -1) + 'deg');
                s.stick.style.setProperty('--rotateY', (28 * x) + 'deg');
                s.stick.style.setProperty('--translateX', (8 * x) + 'px');
                s.stick.style.setProperty('--translateY', (8 * y) + 'px');
            } else {
                s.axis?.classList.remove('is-visible');
                s.stick.style.setProperty('--rotateX', '0deg');
                s.stick.style.setProperty('--rotateY', '0deg');
                s.stick.style.setProperty('--translateX', '0px');
                s.stick.style.setProperty('--translateY', '0px');
            }
        });

        // Beams
        const shouldBeams = progress >= 0.70;
        if (shouldBeams && beamState !== 'visible' && beamState !== 'entering') {
            beamState = 'entering';
            beams?.classList.remove('animate-out-phase1', 'animate-out-phase2', 'animate-out-phase3');
            beams?.classList.add('animate-in');
            setTimeout(() => {
                if (beamState !== 'entering') return;
                beams?.classList.remove('animate-in');
                beams?.classList.add('animate-out-phase1');
                setTimeout(() => {
                    if (beamState !== 'entering') return;
                    beams?.classList.remove('animate-out-phase1');
                    beams?.classList.add('animate-out-phase2');
                    setTimeout(() => { if (beamState === 'entering') beamState = 'visible'; }, 700);
                }, 700);
            }, 700);
        } else if (!shouldBeams && beamState !== 'hidden') {
            beamState = 'hidden';
            beams?.classList.remove('animate-in', 'animate-out-phase1', 'animate-out-phase2');
        }
    }

    // Initialize interactive elements
    setTimeout(() => {
        initJoystick('l-joystick-assembly');
        initJoystick('r-joystick-assembly');
        setupBumper('l-bumper-trigger', 'l-bumper');
        setupBumper('r-bumper-trigger', 'r-bumper');
        setupDpadTriggers();
    }, 100);


    /* ============================================================
       WRENCH ANIMATION (from old showcase – cog rotation + celebration)
       ============================================================ */
    const wrenchContainer = document.getElementById('wrenchContainer');
    const cog = wrenchContainer?.querySelector('.cog');
    const celebration = wrenchContainer?.querySelector('.celebration-effects');
    let celebTriggered = false;

    function updateWrench(progress) {
        if (!wrenchContainer) return;
        wrenchContainer.style.filter = `grayscale(${100 - progress * 100}%) opacity(${0.7 + progress * 0.3})`;
        if (cog) cog.style.transform = `translate(-50%, -50%) rotate(${progress * 720}deg)`;
        if (celebration) {
            if (progress < 1) {
                celebration.classList.remove('fade-out');
                celebration.style.transform = `translate(-50%, -50%) scale(${0.5 + progress * 0.5})`;
                celebration.style.opacity = progress;
                celebTriggered = false;
            } else if (!celebTriggered) {
                celebration.classList.add('fade-out');
                celebTriggered = true;
            }
        }
    }


    /* ============================================================
       MAIN SCROLL HANDLER
       ============================================================ */
    function onScroll() {
        const scrollTop = viewport.scrollTop;
        const scrollHeight = viewport.scrollHeight - viewport.clientHeight;
        const globalProgress = scrollTop / scrollHeight;
        const sectionProgress = globalProgress * 3;
        const sectionIndex = Math.min(2, Math.floor(sectionProgress));
        const localProgress = Math.min(1, Math.max(0, sectionProgress - sectionIndex));

        updateSection(sectionIndex);

        if (sectionIndex === 0) updateBeaker(localProgress);
        else if (sectionIndex === 1) updateController(localProgress);
        else updateWrench(localProgress);

        // Content card visibility
        cards.forEach((card, i) => {
            const rect = sections[i]?.getBoundingClientRect();
            if (rect) {
                const vis = rect.top < window.innerHeight * 0.8 && rect.bottom > window.innerHeight * 0.2;
                card.classList.toggle('visible', vis);
            }
        });
    }

    viewport.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
});
