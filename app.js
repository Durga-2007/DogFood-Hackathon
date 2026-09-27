/* ==========================================================================
   DOGFOOD — page logic
   --------------------------------------------------------------------------
   The dc-runtime (support.js) evaluates the inline <script data-dc-script>
   block in index.html with `DCLogic` and `React` injected as locals, and it
   reads that block as *text* — so it cannot carry a `src`. This file therefore
   exports a factory on `window`, and the inline block is a one-liner that
   calls it:

       const Component = window.DCApp(DCLogic, React);

   Load order: index.html loads support.js and then this file synchronously in
   <head>. support.js fetches React over the network before booting, so
   `window.DCApp` is always defined by the time the factory is called.

   Contents
     1. State
     2. Mobile navigation drawer
     3. renderVals()  — every {{ binding }} the template consumes
     4. Scroll ticker + lifecycle
     5. Effects (cursor, HUD, reveal, scramble, counters, tilt, mesh, …)
   ========================================================================== */
window.DCApp = function (DCLogic, React) {

  class Component extends DCLogic {
    constructor(p){ super(p); this.rootRef = React.createRef(); this._cleanups = []; this._subs = []; }

    /* ---------------------------------------------------------------------
       1. State
     2. Mobile navigation drawer
       --------------------------------------------------------------------- */

    state = {
      menu: false
    };

    /* ---------------------------------------------------------------------
       2. Mobile navigation drawer

       Below 860px the header links slide in from the right as a sidebar (see
       the .dfnav-* rules in css/styles.css). Only the open flag lives here;
       everything visual is CSS so the desktop row is untouched.
       --------------------------------------------------------------------- */

    static NAV_BREAKPOINT = 860;

    setMenu(open){
      if (this.state.menu === open) return;
      document.documentElement.classList.toggle('dfnav-open', open);
      this.setState({ menu: open });
    }

    toggleMenu(){ this.setMenu(!this.state.menu); }

    closeMenu(){ this.setMenu(false); }

    initNavMenu(){
      const onKey = (e) => {
        if (e.key === 'Escape' && this.state.menu) this.closeMenu();
      };
      // Rotating a phone or dragging a desktop window back over the
      // breakpoint would otherwise leave the drawer open behind a nav row
      // that is visible again.
      const onResize = () => {
        if (this.state.menu && window.innerWidth > Component.NAV_BREAKPOINT) this.closeMenu();
      };
      document.addEventListener('keydown', onKey);
      window.addEventListener('resize', onResize);
      this._cleanups.push(() => {
        document.removeEventListener('keydown', onKey);
        window.removeEventListener('resize', onResize);
        document.documentElement.classList.remove('dfnav-open');
      });
    }

    /* ---------------------------------------------------------------------
       3. renderVals() — the single object the template binds against.
          Every {{ name }} in index.html resolves to a key returned here.
       --------------------------------------------------------------------- */

    renderVals(){
      const S = this.state;
      return {
        rootRef: this.rootRef,
        menuOpenClass: S.menu ? 'is-open' : '',
        menuLabel: S.menu ? 'Close menu' : 'Open menu',
        menuExpanded: S.menu ? 'true' : 'false',
        toggleMenu: () => this.toggleMenu(),
        closeMenu: () => this.closeMenu()
      };
    }

    /* ---------------------------------------------------------------------
       4. Scroll ticker + lifecycle

       Everything scroll-driven runs off one rAF loop rather than a scroll
       listener — scroll events are unreliable in embedded hosts. Effects
       register a callback with sub(); teardown goes on this._cleanups.
       --------------------------------------------------------------------- */

    sub(fn){ this._subs.push(fn); }

    startTicker(){
      let raf = 0, lastY = -1, lastH = -1, frame = 0;
      const loop = () => {
        raf = requestAnimationFrame(loop);
        frame++;
        const y = window.scrollY || document.documentElement.scrollTop || 0;
        const h = window.innerHeight;
        const changed = (y !== lastY) || (h !== lastH);
        if (!changed && frame % 30 !== 0) return;
        const dy = lastY < 0 ? 0 : y - lastY;
        lastY = y; lastH = h;
        for (let i = 0; i < this._subs.length; i++){
          try { this._subs[i](y, dy, h); } catch(e){}
        }
      };
      raf = requestAnimationFrame(loop);
      this._cleanups.push(() => { if (raf) cancelAnimationFrame(raf); });
    }

    componentDidMount(){
      const root = this.rootRef.current || document.body;
      this.initReveal(root);
      this.initScramble(root);
      this.initCounts(root);
      this.initBars(root);
      this.initTiers(root);
      this.initTilt(root);
      this.initMarquee(root);
      this.initMesh(root);
      this.initHud(root);
      this.initLetters(root);
      this.initMagnets(root);
      this.initCursor(root);
      this.initNavMenu();
      this.startTicker();
    }

    componentWillUnmount(){ this._subs = []; this._cleanups.forEach(f => { try { f(); } catch(e){} }); this._cleanups = []; }

    /* Fire `cb(node)` once per node, the first tick it enters the viewport.
       `opts.margin` (default .12) shrinks the trigger line as a fraction of
       the viewport height. */
    obs(nodes, cb, opts){
      if (!nodes.length) return;
      const margin = (opts && opts.margin) || 0.12;
      let pending = nodes.slice();
      const check = () => {
        if (!pending.length) return;
        const vh = window.innerHeight || document.documentElement.clientHeight;
        const still = [];
        for (let i = 0; i < pending.length; i++){
          const n = pending[i];
          const r = n.getBoundingClientRect();
          const visible = r.top < vh * (1 - margin) && (r.height > 0 || r.width > 0);
          if (visible) { try { cb(n); } catch(e){} } else still.push(n);
        }
        pending = still;
      };
      this.sub(check);
      check();
      const t = setTimeout(check, 300);
      this._cleanups.push(() => clearTimeout(t));
    }

    /* ---------------------------------------------------------------------
       5. Effects
       --------------------------------------------------------------------- */

    initCursor(root){
      if (window.matchMedia('(pointer: coarse)').matches) return;
      const cross = root.querySelector('[data-cursor]');
      const ring = root.querySelector('[data-cursor-ring]');
      const label = root.querySelector('[data-cursor-label]');
      const arms = Array.from(root.querySelectorAll('[data-cursor-h],[data-cursor-h2],[data-cursor-v],[data-cursor-v2]'));
      const brackets = Array.from(root.querySelectorAll('[data-br]'));
      if (!cross || !ring) return;
      document.documentElement.style.cursor = 'none';

      let x = window.innerWidth / 2, y = window.innerHeight / 2, rx = x, ry = y;
      let scale = 1, tScale = 1, raf = 0, shown = false, wasHit = null;

      const interactive = (el) => {
        let n = el;
        for (let i = 0; i < 5 && n; i++){
          if (n.tagName === 'A' || n.tagName === 'BUTTON' || n.tagName === 'SUMMARY' ||
              n.tagName === 'INPUT' || n.tagName === 'TEXTAREA') return n;
          n = n.parentElement;
        }
        return null;
      };
      const labelFor = (el) => {
        if (el.tagName === 'SUMMARY') return el.parentElement && el.parentElement.open ? 'CLOSE' : 'OPEN';
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return 'TYPE';
        // Discord CTAs point at the real invite URL, not the old #discord anchor.
        if (el.tagName === 'A') return (el.getAttribute('href') || '').indexOf('discord.gg') !== -1 ? 'JOIN' : 'JUMP';
        return 'SELECT';
      };

      const onMove = (e) => {
        x = e.clientX; y = e.clientY;
        if (!shown){ shown = true; cross.style.opacity = '1'; ring.style.opacity = '1'; }
        const hit = interactive(e.target);
        const state = hit ? hit.tagName + labelFor(hit) : '';
        if (state === wasHit) return;
        wasHit = state;
        tScale = hit ? 1.55 : 1;
        brackets.forEach(b => { b.style.opacity = hit ? '1' : '0'; });
        const c = hit ? '#FF3D6E' : '#00E5D0';
        arms.forEach(a => { a.style.background = c; });
        if (label){
          label.textContent = hit ? labelFor(hit) : '';
          label.style.opacity = hit ? '1' : '0';
          label.style.color = c;
        }
      };
      const onLeave = () => { shown = false; cross.style.opacity = '0'; ring.style.opacity = '0'; };
      const onDown = () => { tScale = wasHit ? 1.15 : 0.7; };
      const onUp = () => { tScale = wasHit ? 1.55 : 1; };

      const loop = () => {
        raf = requestAnimationFrame(loop);
        const nx = rx + (x - rx) * 0.19, ny = ry + (y - ry) * 0.19;
        const vx = nx - rx, vy = ny - ry;
        rx = nx; ry = ny;
        scale += (tScale - scale) * 0.16;
        const speed = Math.min(1, Math.hypot(vx, vy) / 26);
        cross.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
        ring.style.transform = 'translate3d(' + rx.toFixed(1) + 'px,' + ry.toFixed(1) + 'px,0) rotate(' +
          (vx * 0.9).toFixed(2) + 'deg) scale(' + (scale * (1 + speed * 0.22)).toFixed(3) + ',' + (scale * (1 - speed * 0.12)).toFixed(3) + ')';
      };
      raf = requestAnimationFrame(loop);

      window.addEventListener('mousemove', onMove, { passive: true });
      document.addEventListener('mouseleave', onLeave);
      window.addEventListener('mousedown', onDown, { passive: true });
      window.addEventListener('mouseup', onUp, { passive: true });
      this._cleanups.push(() => {
        document.documentElement.style.cursor = '';
        if (raf) cancelAnimationFrame(raf);
        window.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseleave', onLeave);
        window.removeEventListener('mousedown', onDown);
        window.removeEventListener('mouseup', onUp);
      });
    }

    // Drives the left-edge scroll progress line and the parallax on the big
    // outlined section numerals.
    initHud(root){
      const bar = root.querySelector('[data-progress]');
      const ghosts = Array.from(root.querySelectorAll('[data-ghost]'));
      const tick = () => {
        const doc = document.documentElement;
        const max = Math.max(1, doc.scrollHeight - window.innerHeight);
        const y = window.scrollY || doc.scrollTop || 0;
        const p = Math.min(1, Math.max(0, y / max));
        if (bar) bar.style.height = (p * 100).toFixed(2) + '%';
        const vh = window.innerHeight;
        for (let i = 0; i < ghosts.length; i++){
          const g = ghosts[i];
          const r = g.getBoundingClientRect();
          if (r.bottom < -200 || r.top > vh + 200) continue;
          const d = (r.top + r.height / 2 - vh / 2) / vh;
          g.style.transform = 'translate3d(0,' + (d * -22).toFixed(1) + 'px,0)';
        }
      };
      this.sub(tick);
      tick();
    }

    // Cursor magnetism on the hero wordmark letters. Pointer-driven, so there is
    // nothing to do on touch devices.
    initLetters(root){
      const letters = Array.from(root.querySelectorAll('[data-letter]'));
      if (!letters.length) return;
      if (window.matchMedia('(pointer: coarse)').matches) return;
      let raf = 0, cx = 0, cy = 0;
      const onMove = (e) => {
        cx = e.clientX; cy = e.clientY;
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          for (let i = 0; i < letters.length; i++){
            const l = letters[i];
            const r = l.getBoundingClientRect();
            if (r.bottom < 0 || r.top > window.innerHeight) continue;
            const dx = (cx - (r.left + r.width / 2)) / Math.max(1, window.innerWidth);
            const dy = (cy - (r.top + r.height / 2)) / Math.max(1, window.innerHeight);
            const dist = Math.hypot(dx, dy);
            // Wider reach and a stronger throw than the surrounding magnets:
            // the wordmark is meant to read as the most alive thing on screen.
            const pull = Math.max(0, 1 - dist * 1.4);
            const ease = pull * pull * (3 - 2 * pull);
            l.style.transform = 'translate3d(' + (dx * 40 * ease).toFixed(2) + 'px,' + (dy * 26 * ease).toFixed(2) + 'px,' + (ease * 100).toFixed(1) + 'px) rotateY(' + (dx * 22 * ease).toFixed(2) + 'deg) rotateX(' + (-dy * 13 * ease).toFixed(2) + 'deg) scale(' + (1 + ease * 0.04).toFixed(3) + ')';
          }
        });
      };
      // Hand off from the letterin entrance animation before taking over transform.
      const start = setTimeout(() => {
        letters.forEach(l => { l.style.animation = 'none'; l.style.transition = 'transform .32s cubic-bezier(.16,1,.3,1)'; });
        window.addEventListener('mousemove', onMove, { passive: true });
      }, 2000);
      this._cleanups.push(() => { clearTimeout(start); window.removeEventListener('mousemove', onMove); if (raf) cancelAnimationFrame(raf); });
    }

    initMagnets(root){
      if (window.matchMedia('(pointer: coarse)').matches) return;
      const nodes = Array.from(root.querySelectorAll('[data-magnet]'));
      const offs = [];
      nodes.forEach(n => {
        n.style.transition = 'transform .25s cubic-bezier(.16,1,.3,1), background .12s linear, color .12s linear';
        const move = (e) => {
          const r = n.getBoundingClientRect();
          const dx = e.clientX - (r.left + r.width / 2);
          const dy = e.clientY - (r.top + r.height / 2);
          n.style.transform = 'translate3d(' + (dx * .22).toFixed(1) + 'px,' + (dy * .3).toFixed(1) + 'px,0)';
        };
        const leave = () => { n.style.transform = 'translate3d(0,0,0)'; };
        n.addEventListener('mousemove', move);
        n.addEventListener('mouseleave', leave);
        offs.push(() => { n.removeEventListener('mousemove', move); n.removeEventListener('mouseleave', leave); });
      });
      this._cleanups.push(() => offs.forEach(f => f()));
    }

    initReveal(root){
      const nodes = Array.from(root.querySelectorAll('[data-reveal]'));
      nodes.forEach(n => {
        n.style.opacity = '0';
        n.style.transform = 'translateY(18px)';
        n.style.transition = 'opacity .7s cubic-bezier(.16,1,.3,1), transform .7s cubic-bezier(.16,1,.3,1)';
      });
      const show = n => { n.style.opacity = '1'; n.style.transform = 'none'; };
      this.obs(nodes, show);
      const t = setTimeout(() => nodes.forEach(show), 4000);
      this._cleanups.push(() => clearTimeout(t));

      const rules = Array.from(root.querySelectorAll('[data-rule]'));
      rules.forEach(r => { r.style.transform = 'scaleX(0)'; r.style.transition = 'transform 1s cubic-bezier(.16,1,.3,1)'; });
      this.obs(rules, r => { r.style.transform = 'scaleX(1)'; });
    }

    initScramble(root){
      const CH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#*+<>[]';
      const nodes = Array.from(root.querySelectorAll('[data-scramble]'));
      const run = (el) => {
        const final = el.textContent;
        const len = final.length;
        if (len > 220) return;
        // The scrambled string is the same length as the final one, but the
        // filler glyphs are not the same width, so the heading can wrap onto
        // an extra line mid-animation and shove everything below it down.
        // Freeze the box at the height the settled text occupies and clip any
        // transient overflow, then hand the height back to the flow.
        const box = el.getBoundingClientRect().height;
        const prevMin = el.style.minHeight, prevMax = el.style.maxHeight, prevOv = el.style.overflow;
        if (box){
          el.style.minHeight = box + 'px';
          el.style.maxHeight = box + 'px';
          el.style.overflow = 'hidden';
        }
        const release = () => {
          el.style.minHeight = prevMin; el.style.maxHeight = prevMax; el.style.overflow = prevOv;
        };
        let frame = 0;
        const total = Math.min(48, 14 + Math.floor(len / 3));
        const id = setInterval(() => {
          frame++;
          const settled = Math.floor((frame / total) * len);
          let out = '';
          for (let i = 0; i < len; i++){
            const c = final[i];
            if (i < settled || c === ' ' || c === '\n') out += c;
            else out += CH[(Math.random() * CH.length) | 0];
          }
          el.textContent = out;
          if (frame >= total) { clearInterval(id); el.textContent = final; release(); }
        }, 26);
        this._cleanups.push(() => { clearInterval(id); release(); });
      };
      this.obs(nodes, run);
    }

    initCounts(root){
      const nodes = Array.from(root.querySelectorAll('[data-count]'));
      this.obs(nodes, el => {
        const target = parseFloat(el.getAttribute('data-count'));
        const suffix = el.getAttribute('data-suffix') || '';
        const dur = 1100; const t0 = performance.now();
        const step = (t) => {
          const p = Math.min(1, (t - t0) / dur);
          const e = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * e) + suffix;
          if (p < 1) requestAnimationFrame(step); else el.textContent = target + suffix;
        };
        requestAnimationFrame(step);
      });
    }

    initBars(root){
      const nodes = Array.from(root.querySelectorAll('[data-bar]'));
      this.obs(nodes, el => { el.style.width = el.getAttribute('data-bar') + '%'; });
    }

    initTiers(root){
      const nodes = Array.from(root.querySelectorAll('[data-tier]'));
      this.obs(nodes, (el) => {
        el.style.transform = 'translateZ(0) translateY(0)';
        el.style.opacity = '1';
        el.style.borderColor = '#FF3D6E';
        const s = el.querySelector('[data-tier-status]');
        if (s){ s.textContent = '[ UNLOCKED ]'; s.style.color = '#00E5D0'; }
      });
    }

    initTilt(root){
      const wrap = root.querySelector('[data-tilt]');
      const inner = root.querySelector('[data-tilt-inner]');
      if (!wrap || !inner) return;
      if (window.matchMedia('(pointer: coarse)').matches) return;
      let raf = 0, tx = 0, ty = 0;
      const onMove = (e) => {
        const w = window.innerWidth, h = window.innerHeight;
        tx = (e.clientX / w - 0.5) * 2;
        ty = (e.clientY / h - 0.5) * 2;
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          inner.style.transform = 'rotateY(' + (tx * 10).toFixed(2) + 'deg) rotateX(' + (-ty * 7).toFixed(2) + 'deg) translateZ(0)';
        });
      };
      window.addEventListener('mousemove', onMove, { passive: true });
      this._cleanups.push(() => { window.removeEventListener('mousemove', onMove); if (raf) cancelAnimationFrame(raf); });
    }

    initMarquee(root){
      const m = root.querySelector('[data-marquee]');
      const m2 = root.querySelector('[data-marquee2]');
      if (!m && !m2) return;
      // Constant speed, constant direction — no scroll coupling.
      if (m){ m.style.animationDuration = '34s'; m.style.animationDirection = 'normal'; }
      if (m2){ m2.style.animationDuration = '28s'; m2.style.animationDirection = 'reverse'; }
    }

    /* ---------------------------------------------------------------------
       Hero backdrop — a rotating tesseract (4D hypercube).

       Sixteen vertices at every combination of +/-1 in four axes; two
       vertices share an edge when they differ in exactly one coordinate,
       which gives 32 edges. The double rotation happens in the XW and YZ
       planes, so the projection reads as a cube turning itself inside out
       through a cube — the inner cell swells outward and the outer one
       collapses inward, forever. Two projections stack: 4D -> 3D by w, then
       the usual 3D -> 2D by z, so both give depth cues.

       A node cloud orbits the hull and wires into the nearest cell vertices,
       keeping the "wired rack" texture the rest of the page is built on.
       --------------------------------------------------------------------- */

    initMesh(root){
      const cv = root.querySelector('[data-mesh]');
      if (!cv) return;
      const ctx = cv.getContext('2d');
      if (!ctx) return;

      // Edge classes drive colour: 0 = inner cell, 1 = strut between cells
      // (accent), 2 = node wiring (faint), 3 = outer cell.
      const V = [], E = [];
      // `lift` marks a vertex as part of the hypercube itself. The node
      // cloud orbits well outside |w| <= 1, where the 4D projection would
      // divide by near-zero, so those points skip it and stay in 3D.
      const push = (x,y,z,ww,lift) => { V.push([x,y,z,ww,lift ? 1 : 0]); return V.length - 1; };

      const cellIdx = [];
      for (let i = 0; i < 16; i++){
        cellIdx.push(push(
          (i & 1) ? 1 : -1,
          (i & 2) ? 1 : -1,
          (i & 4) ? 1 : -1,
          (i & 8) ? 1 : -1,
          true
        ));
      }
      for (let i = 0; i < 16; i++){
        for (let bit = 0; bit < 4; bit++){
          const j = i ^ (1 << bit);
          if (j < i) continue;                       // one edge per pair
          const cls = bit === 3 ? 1 : ((i & 8) ? 3 : 0);
          E.push([cellIdx[i], cellIdx[j], cls]);
        }
      }

      // A sparse dust ring, points only. Any wiring here read as long
      // diagonals across the whole hero and swallowed the hull.
      const NODES = 18, nodeIdx = [];
      for (let i = 0; i < NODES; i++){
        const th = (i / NODES) * Math.PI * 2;
        const r = 2.2 + (i % 4) * 0.24;
        const y = (((i * 37) % 100) / 100) * 3.1 - 1.55;
        nodeIdx.push(push(Math.cos(th) * r, y, Math.sin(th) * r * 0.75, 0, false));
      }

      let w = 0, h = 0, dpr = 1;
      const resize = () => {
        dpr = Math.min(window.innerWidth < 768 ? 1.5 : 2, window.devicePixelRatio || 1);
        const r = cv.getBoundingClientRect();
        w = Math.max(1, r.width); h = Math.max(1, r.height);
        cv.width = w * dpr; cv.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      };
      resize();
      window.addEventListener('resize', resize, { passive: true });

      let scrollY = window.scrollY || 0;
      this.sub((y) => { scrollY = y; });

      // The hull turns on every screen. Phones just get a cheaper frame:
      // capped device pixel ratio (see resize) and roughly 30fps instead of
      // 60, so the hero keeps moving without cooking the battery. Nothing
      // else stops the loop but a hidden tab.
      const small = () => window.innerWidth < 768;
      let raf = 0, t0 = performance.now(), stopped = false, last = -1e9;

      const draw = (now) => {
        // Throttle on small screens: skip the frame, keep the loop alive.
        if (small() && now - last < 32){ raf = requestAnimationFrame(draw); return; }
        last = now;
        const t = (now - t0) / 1000;

        // 4D double rotation. The XW rate is the one you read as the
        // inside-out turn; YZ is slower so the two never resync into a
        // plain spin.
        // Phase offsets, so the first frame lands on an angled pose instead
        // of a flat head-on square.
        const aw = 0.85 + t * 0.34 + scrollY * 0.0011;
        const az = t * 0.21;
        const caw = Math.cos(aw), saw = Math.sin(aw);
        const caz = Math.cos(az), saz = Math.sin(az);

        // Cursor-independent: a slow drift on Y plus a gentle self-driven
        // nod on X, so the hull keeps moving on its own with the pointer idle.
        const rotY = 0.6 + t * 0.18 + scrollY * 0.0008;
        const rotX = -0.12 + Math.sin(t * 0.23) * 0.16;
        const cy = Math.cos(rotY), sy = Math.sin(rotY), cx = Math.cos(rotX), sx = Math.sin(rotX);
        // Phones get the desktop composition, scaled down: hull off to the
        // right of the wordmark rather than centred in a tall hero, where it
        // ended up behind the body copy. 0.31 is where the wordmark sits in
        // the canvas at phone heights.
        const mob = w < 768;
        const cxp = w * (w > 900 ? 0.72 : (mob ? 0.66 : 0.5));
        const cyp = h * (mob ? 0.31 : 0.5);
        const scale = Math.min(w, h) * (w > 900 ? 0.155 : (mob ? 0.13 : 0.26));

        const P = V.map(v => {
          let x = v[0], y = v[1], z = v[2], ww = v[3];
          let p4 = 1;
          if (v[4]){
            // XW plane
            const x4 = x * caw - ww * saw; ww = x * saw + ww * caw; x = x4;
            // YZ plane
            const y4 = y * caz - z * saz; z = y * saz + z * caz; y = y4;
            // 4D -> 3D. |w| stays under sqrt(2) here, so 2.9 never divides
            // to zero and the swell stays bounded.
            p4 = 2.9 / (2.9 - ww);
            x *= p4; y *= p4; z *= p4;
          }
          // 3D -> 2D, as before.
          const x1 = x * cy - z * sy, z1 = x * sy + z * cy;
          const y1 = y * cx - z1 * sx, z2 = y * sx + z1 * cx;
          const persp = 4.6 / (4.6 + z2);
          return [cxp + x1 * scale * persp, cyp + y1 * scale * persp, persp, p4];
        });

        ctx.clearRect(0, 0, w, h);
        for (let i = 0; i < E.length; i++){
          const e = E[i], a = P[e[0]], b = P[e[1]];
          const depth = (a[2] + b[2]) / 2;
          const alpha = Math.max(0, Math.min(1, (depth - 0.62) * 2.2));
          // The cell nearer in w draws heavier, so the inside-out swap is
          // legible instead of two cubes of equal weight overlapping.
          const near = Math.max(0, Math.min(1, ((a[3] + b[3]) / 2 - 0.75) * 1.5));
          if (e[2] === 1){
            ctx.lineWidth = 1;
            ctx.strokeStyle = 'rgba(0,229,208,' + (alpha * (0.5 + near * 0.5)).toFixed(3) + ')';
          } else if (e[2] === 2){
            ctx.lineWidth = 1;
            ctx.strokeStyle = 'rgba(230,236,255,' + (alpha * 0.1).toFixed(3) + ')';
          } else {
            ctx.lineWidth = 1 + near * 0.8;
            ctx.strokeStyle = 'rgba(230,236,255,' + (alpha * (0.4 + near * 0.45)).toFixed(3) + ')';
          }
          ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
        }
        ctx.lineWidth = 1;
        for (let i = 0; i < cellIdx.length; i++){
          const p = P[cellIdx[i]];
          const s = Math.max(1.4, p[2] * p[3] * 3.4);
          ctx.fillStyle = (i & 8) ? 'rgba(255,61,110,.85)' : 'rgba(0,229,208,.85)';
          ctx.fillRect(p[0] - s/2, p[1] - s/2, s, s);
        }
        for (let i = 0; i < nodeIdx.length; i++){
          const p = P[nodeIdx[i]];
          const s = Math.max(.6, p[2] * 2.1);
          ctx.fillStyle = (i % 7 === 0) ? 'rgba(255,61,110,.9)' : 'rgba(230,236,255,.42)';
          ctx.fillRect(p[0] - s/2, p[1] - s/2, s, s);
        }
        if (!stopped) raf = requestAnimationFrame(draw);
      };

      raf = requestAnimationFrame(draw);

      const onVis = () => {
        if (document.hidden) { stopped = true; if (raf) cancelAnimationFrame(raf); }
        else { stopped = false; t0 = performance.now() - 1; last = -1e9; raf = requestAnimationFrame(draw); }
      };
      document.addEventListener('visibilitychange', onVis);

      this._cleanups.push(() => {
        stopped = true;
        if (raf) cancelAnimationFrame(raf);
        window.removeEventListener('resize', resize);
        document.removeEventListener('visibilitychange', onVis);
      });
    }
  }

  return Component;
};
