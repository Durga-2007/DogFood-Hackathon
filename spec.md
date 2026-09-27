<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DOGFOOD — Build the platform that will judge you</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="img/favicon-180.png">

<!-- Global stylesheet. Component-level styling stays inline in the template below. -->
<link rel="stylesheet" href="css/styles.css?v=202609141617">
<style>
/* ---- Judges panel (seated) ---------------------------------------------- */
.df-jgrid { display:grid; grid-template-columns:1fr; gap:14px; list-style:none; margin:0 0 34px; padding:0; }
/* Nine headliners: three columns divide evenly, so no orphan row on desktop. */
@media (min-width:760px) { .df-jgrid { grid-template-columns:repeat(2,1fr); } }
@media (min-width:1180px) { .df-jgrid { grid-template-columns:repeat(3,1fr); } }
/* Any count that does leave one card alone on the last row: let it span instead. */
@media (min-width:760px) and (max-width:1179px) { .df-jcard:last-child:nth-child(odd) { grid-column:1 / -1; } }
@media (min-width:1180px) { .df-jcard:last-child:nth-child(3n+1) { grid-column:1 / -1; } }
.df-jcard { display:flex; flex-direction:row; border:1px solid #1B2540; background:#0B1020; overflow:hidden; transition:border-color .18s linear; }
.df-jcard:hover { border-color:#26355C; }
.df-jcard__media { flex:none; width:160px; align-self:stretch; overflow:hidden; background:#0E1428; }
@media (max-width:520px) { .df-jcard { flex-direction:column; } .df-jcard__media { width:100%; aspect-ratio:1; } }
.df-jphoto { width:100%; height:100%; object-fit:cover; filter:grayscale(1) contrast(.98); transition:filter .3s ease, transform .3s ease; }
.df-jcard:hover .df-jphoto { filter:grayscale(0) contrast(1); transform:scale(1.03); }
.df-jphoto--empty, .df-chip__photo--empty { display:grid; place-items:center; font-family:'Archivo Black',sans-serif; color:#26355C; background:#0E1428; }
.df-jphoto--empty { font-size:3rem; }
.df-jcard__body { display:flex; flex-direction:column; gap:7px; padding:16px 18px 18px; min-width:0; flex:1; }
.df-jcard__name { margin:0; font:800 16px/1.2 'Syne',sans-serif; letter-spacing:.01em; color:#E6ECFF; }
.df-jcard__meta { font:400 15px/1.3 'VT323',monospace; letter-spacing:.12em; text-transform:uppercase; color:#FF3D6E; }
.df-jcard__bio { margin:0; font:400 12px/1.8 'JetBrains Mono',monospace; color:#AEBAD6; }
.df-li { margin-top:auto; padding-top:6px; display:inline-flex; align-items:center; gap:6px; font:400 15px/1 'VT323',monospace; letter-spacing:.14em; text-transform:uppercase; color:#6B7A9E; text-decoration:none; transition:color .18s linear; }
.df-li:hover { color:#00E5D0; }
.df-panel-label { border-bottom:1px solid #1B2540; padding-bottom:8px; margin-bottom:18px; font:400 15px/1 'VT323',monospace; letter-spacing:.16em; color:#6B7A9E; }
.df-marquee { overflow:hidden; padding-block:4px; }
.df-marquee--auto { mask-image:linear-gradient(to right,transparent,black 5%,black 95%,transparent); -webkit-mask-image:linear-gradient(to right,transparent,black 5%,black 95%,transparent); }
.df-marquee__track { display:flex; gap:12px; width:max-content; }
.df-marquee--auto .df-marquee__track { animation:df-marquee 150s linear infinite; }
.df-marquee--auto:hover .df-marquee__track { animation-play-state:paused; }
@keyframes df-marquee { to { transform:translateX(-50%); } }
.df-chip { flex:0 0 148px; min-height:210px; display:flex; flex-direction:column; align-items:center; text-align:center; gap:4px; padding:12px 10px 14px; border:1px solid #1B2540; background:#0B1020; color:inherit; text-decoration:none; transition:border-color .18s linear; }
.df-chip:hover { border-color:#26355C; }
.df-chip__photo { width:96px; height:96px; object-fit:cover; margin-bottom:8px; filter:grayscale(1) contrast(.98); transition:filter .3s ease; }
.df-chip__photo--empty { font-size:2rem; }
.df-chip:hover .df-chip__photo { filter:grayscale(0) contrast(1); }
.df-chip__name { font:800 12.5px/1.25 'Syne',sans-serif; color:#E6ECFF; }
.df-chip__company { font:400 14px/1.25 'VT323',monospace; letter-spacing:.1em; text-transform:uppercase; color:#6B7A9E; }
@media (prefers-reduced-motion: reduce) {
  .df-marquee--auto { overflow-x:auto; mask-image:none; -webkit-mask-image:none; }
  .df-marquee--auto .df-marquee__track { animation:none; }
  .df-marquee--auto .df-chip[aria-hidden='true'] { display:none; }
}
</style>

<!-- dc-runtime: parses the x-dc template in the body and mounts it with React.
     Keep literal tag names out of comments here — the runtime re-parses this
     file with a regex and would match them. -->
<script src="js/support.js"></script>
<!-- Page logic. Defines window.DCApp, which the data-dc-script block at the
     bottom of this file calls. Must load before the runtime boots. -->
<script src="js/app.js"></script>
</head>
<body>
<x-dc>
<helmet data-dc-atomics>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=JetBrains+Mono:wght@400;500;700&family=Playfair+Display:ital,wght@0,700;1,700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Archivo:wght@400;600&family=Anton&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=Syne:wght@600;800&family=VT323&family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<!-- Global CSS lives in styles.css, linked from the document head above. -->
</helmet>

<div ref="{{ rootRef }}" style="position:relative;background:#0B1020;color:#E6ECFF;min-height:100vh;overflow-x:hidden">

<div data-grain style="position:fixed;inset:0;z-index:90;pointer-events:none;opacity:.04;background-image:url(data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='160'%20height='160'%3E%3Cfilter%20id='n'%3E%3CfeTurbulence%20type='fractalNoise'%20baseFrequency='0.85'%20numOctaves='3'/%3E%3C/filter%3E%3Crect%20width='160'%20height='160'%20filter='url(%23n)'/%3E%3C/svg%3E)"></div>
<div data-scanlines style="position:fixed;inset:0;z-index:89;pointer-events:none;opacity:.15;background-image:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.55) 3px,rgba(0,0,0,.55) 4px)"></div>
<div style="position:fixed;left:0;right:0;top:0;height:26vh;z-index:91;pointer-events:none;background:linear-gradient(180deg,transparent,rgba(230,236,255,.06) 60%,rgba(255,61,110,.10));animation:sweep 2.4s cubic-bezier(.4,0,.2,1) .15s 1 both"></div>
<div style="position:fixed;left:0;top:0;bottom:0;width:2px;z-index:92;pointer-events:none;background:#131C36"><span data-progress style="display:block;width:100%;height:0%;background:#FF3D6E"></span></div>
<div data-cursor style="user-select:none;-webkit-user-select:none;position:fixed;left:0;top:0;z-index:95;pointer-events:none;opacity:0;transition:opacity .2s linear;will-change:transform">
  <span data-cursor-h style="position:absolute;left:-9px;top:0;width:7px;height:1px;background:#00E5D0"></span>
  <span data-cursor-h2 style="position:absolute;left:2px;top:0;width:7px;height:1px;background:#00E5D0"></span>
  <span data-cursor-v style="position:absolute;left:0;top:-9px;width:1px;height:7px;background:#00E5D0"></span>
  <span data-cursor-v2 style="position:absolute;left:0;top:2px;width:1px;height:7px;background:#00E5D0"></span>
  <span data-cursor-dot style="position:absolute;left:-1px;top:-1px;width:2px;height:2px;background:#FF3D6E"></span>
</div>
<div data-cursor-ring style="user-select:none;-webkit-user-select:none;position:fixed;left:0;top:0;z-index:94;pointer-events:none;opacity:0;transition:opacity .2s linear;will-change:transform">
  <span data-br style="position:absolute;left:-15px;top:-15px;width:7px;height:7px;border-left:1px solid #FF3D6E;border-top:1px solid #FF3D6E;transition:opacity .18s linear;opacity:0"></span>
  <span data-br style="position:absolute;left:8px;top:-15px;width:7px;height:7px;border-right:1px solid #FF3D6E;border-top:1px solid #FF3D6E;transition:opacity .18s linear;opacity:0"></span>
  <span data-br style="position:absolute;left:8px;top:8px;width:7px;height:7px;border-right:1px solid #FF3D6E;border-bottom:1px solid #FF3D6E;transition:opacity .18s linear;opacity:0"></span>
  <span data-br style="position:absolute;left:-15px;top:8px;width:7px;height:7px;border-left:1px solid #FF3D6E;border-bottom:1px solid #FF3D6E;transition:opacity .18s linear;opacity:0"></span>
  <span data-cursor-label style="position:absolute;left:22px;top:9px;white-space:nowrap;font:400 15px/1 'VT323',monospace;letter-spacing:.14em;color:#00E5D0;opacity:0;transition:opacity .18s linear"></span>
</div>

<header style="position:fixed;top:0;left:0;right:0;z-index:80;background:#0B1020;border-bottom:1px solid #00E5D0">
  <div style="overflow:hidden;border-bottom:1px solid #16203A;background:#0B1020">
    <div data-marquee style="user-select:none;-webkit-user-select:none;display:flex;width:max-content;animation:mq 34s linear infinite;will-change:transform">
      <div style="display:flex;gap:0;flex:none;font:500 10px/1 'JetBrains Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:#FF3D6E;padding:6px 0">
        <span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span>
      </div>
      <div aria-hidden="true" style="display:flex;gap:0;flex:none;font:500 10px/1 'JetBrains Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:#FF3D6E;padding:6px 0">
        <span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span><span style="padding:0 15px">Build the platform that will judge you</span><span style="padding:0 15px">·</span>
      </div>
    </div>
  </div>
  <nav class="dfnav" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 16px;padding:4px clamp(12px,2vw,24px);min-height:40px">
    <div style="user-select:none;-webkit-user-select:none;display:flex;align-items:center;gap:11px;font:700 11px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:#E6ECFF;animation:boot .5s ease .2s both">
      <a href="https://raptors.dev" target="_blank" rel="noopener" aria-label="Hackathon Raptors" style="display:block;flex:none;line-height:0"><img src="img/raptors-icon.png" alt="Hackathon Raptors" draggable="false" style="user-select:none;-webkit-user-select:none;-webkit-user-drag:none;display:block;height:19px;width:auto;flex:none"></a>
      <span style="width:1px;height:14px;background:#1B2540;flex:none"></span>
      <a href="/" style="color:inherit;font:inherit;letter-spacing:inherit" style-hover="color:#FF3D6E">DOGFOOD<span style="color:#4A5A80;font-weight:400">®</span></a>
    </div>
    <button class="dfnav-burger" onClick="{{ toggleMenu }}" aria-label="{{ menuLabel }}" aria-expanded="{{ menuExpanded }}" aria-controls="dfnav-drawer">
      <span class="dfnav-burger-box" aria-hidden="true"><span class="dfnav-burger-bar"></span><span class="dfnav-burger-bar"></span><span class="dfnav-burger-bar"></span></span>
    </button>
    <div class="dfnav-scrim {{ menuOpenClass }}" onClick="{{ closeMenu }}" aria-hidden="true"></div>
    <div id="dfnav-drawer" class="dfnav-links {{ menuOpenClass }}">
      <button class="dfnav-close" onClick="{{ closeMenu }}" aria-label="Close menu">[ CLOSE &times; ]</button>
      <a href="#about" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .30s both" style-hover="color:#E6ECFF">About</a>
      <a href="#tiers" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .34s both" style-hover="color:#E6ECFF">Tiers</a>
      <a href="#timeline" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .38s both" style-hover="color:#E6ECFF">Timeline</a>
      <a href="#scoring" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .42s both" style-hover="color:#E6ECFF">Scoring</a>
      <a href="#prizes" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .46s both" style-hover="color:#E6ECFF">Prizes</a>
      <a href="#rules" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .50s both" style-hover="color:#E6ECFF">Rules</a>
      <a href="#judges" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .54s both" style-hover="color:#E6ECFF">Judges</a>
      <a href="#faq" onClick="{{ closeMenu }}" style="color:#6B7A9E;animation:boot .4s ease .58s both" style-hover="color:#E6ECFF">FAQ</a>
      <a href="/spec" onClick="{{ closeMenu }}" style="color:#00E5D0;animation:boot .4s ease .60s both" style-hover="color:#E6ECFF">Spec</a>
      <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener" data-magnet="1" onClick="{{ closeMenu }}" style="display:inline-flex;align-items:center;gap:8px;background:#FF3D6E;color:#0B1020;font-weight:700;letter-spacing:.16em;padding:7px 13px;border:1px solid #FF3D6E;transition:background .12s linear,transform .08s linear;animation:boot .4s ease .62s both" style-hover="background:#0B1020;color:#FF3D6E" style-active="transform:translateY(1px) scale(.98)">Go to Discord <span>&gt;&gt;&gt;</span></a>
    </div>
  </nav>
</header>

<section style="position:relative;min-height:max(89dvh,850px);padding:clamp(108px,13.5vh,144px) clamp(12px,2vw,24px) 0;display:flex;flex-direction:column;justify-content:space-between;border-bottom:1px solid #00E5D0;overflow:hidden">
  <canvas data-mesh style="position:absolute;top:0;right:0;width:100%;height:100%;opacity:.62;pointer-events:none"></canvas>
  <div style="position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(90deg,rgba(230,236,255,.045) 1px,transparent 1px),linear-gradient(0deg,rgba(230,236,255,.045) 1px,transparent 1px);background-size:calc(100%/12) 120px"></div>

  <div style="position:relative;flex:1;display:grid;grid-template-columns:minmax(0,1fr);align-content:center;gap:0;padding:clamp(12px,4vh,48px) 0">
    <div style="display:flex;flex-wrap:wrap;gap:14px 26px;font:400 17px/1 'VT323',monospace;letter-spacing:.1em;text-transform:uppercase;color:#6B7A9E;margin-bottom:clamp(34px,8vh,96px);animation:boot .5s ease .7s both">
      <span>[ UNIT / DF-01 ]</span><span style="color:#4A5A80">51.5310°N 0.0500°E</span><span style="color:#4A5A80">REV 2.6</span>
      <span style="display:inline-flex;align-items:center;gap:8px;color:#00E5D0"><span data-live style="width:6px;height:6px;background:#00E5D0;display:inline-block;animation:blink 1.4s steps(1) infinite"></span>SYS READY · REGISTRATION OPEN</span>
    </div>

    <div data-tilt style="perspective:1200px;perspective-origin:30% 50%">
      <div data-tilt-inner style="transform-style:preserve-3d;transition:transform .2s cubic-bezier(.16,1,.3,1);will-change:transform;position:relative;display:inline-block;max-width:100%">
        <h1 style="user-select:none;-webkit-user-select:none;margin:0;font-family:'Archivo Black','Arial Black',sans-serif;font-size:clamp(3.3rem,14.3vw,13rem);line-height:.86;letter-spacing:-.045em;text-transform:uppercase;color:#E6ECFF;position:relative;animation:bootw .8s cubic-bezier(.16,1,.3,1) .8s both">
          <span aria-hidden="true" style="position:absolute;left:0;top:0;color:#FF3D6E;transform:translate3d(-14px,14px,-90px);opacity:.32">DOGFOOD</span>
          <span aria-hidden="true" style="position:absolute;left:0;top:0;color:#1B2540;transform:translate3d(-9px,9px,-60px)">DOGFOOD</span>
          <span aria-hidden="true" style="position:absolute;left:0;top:0;color:#24304F;transform:translate3d(-4px,4px,-30px)">DOGFOOD</span>
          <span style="position:relative;display:block;transform-style:preserve-3d">
            <span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) .85s both">D</span><span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) .91s both">O</span><span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) .97s both">G</span><span data-letter style="display:inline-block;transform-style:preserve-3d;color:#FF3D6E;animation:letterin .7s cubic-bezier(.16,1,.3,1) 1.03s both">F</span><span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) 1.09s both">O</span><span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) 1.15s both">O</span><span data-letter style="display:inline-block;transform-style:preserve-3d;animation:letterin .7s cubic-bezier(.16,1,.3,1) 1.21s both">D</span>
          </span>
        </h1>
      </div>
    </div>
  </div>

  <div style="position:relative;display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border-top:1px solid #00E5D0;margin-top:clamp(24px,6vh,64px)">
    <div style="flex:1 1 300px;min-width:0;background:#0B1020;padding:26px 24px 26px 0;animation:boot .6s ease 1.1s both">
      <h2 style="margin:0;font:700 clamp(1.1rem,2.1vw,1.6rem)/1.15 'Archivo Black',sans-serif;letter-spacing:-.02em;text-transform:uppercase;color:#E6ECFF">Build the platform<br><span style="color:#FF3D6E">that will judge you.</span></h2>
      <p style="margin:16px 0 0;font:400 10.5px/1.9 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#6B7A9E">September 25-28, 2026 · Online<br>Free · $2,500 in prizes</p>
      <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener" data-magnet="1" style="display:inline-flex;align-items:center;gap:10px;margin-top:22px;background:#FF3D6E;color:#0B1020;font:700 11px/1 'JetBrains Mono',monospace;letter-spacing:.18em;text-transform:uppercase;padding:14px 20px;border:1px solid #FF3D6E;transition:background .12s linear,color .12s linear,transform .08s linear" style-hover="background:#0B1020;color:#FF3D6E" style-active="transform:translateY(1px) scale(.98)">[ Go to Discord ]</a>
    </div>
    <div style="flex:2 1 380px;background:#0B1020;padding:26px 24px;min-width:0;animation:boot .6s ease 1.25s both">
      <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E;margin-bottom:14px">[ BRIEF / 00 ]</div>
      <p style="margin:0;max-width:66ch;font:400 clamp(.82rem,1.05vw,.95rem)/1.75 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Thirty-five hackathons in, across 85 countries, we know exactly what a submission and judging platform should do. So does every organizer who has ever run one. What none of us has is a modern, open, self-hostable platform that does it. This is the hackathon where you build it. <span style="background:#FF3D6E;color:#0B1020;padding:0 4px">The winning project is the one we run.</span></p>
    </div>
  </div>
  <div style="position:relative;display:flex;justify-content:space-between;font:400 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:#3A4A70;padding:12px 0 16px"><span>/// SCROLL</span><span>HACKATHON RAPTORS ™</span></div>
</section>

<section id="about" style="padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">01</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 01 / BY THE NUMBERS ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border:1px solid #1B2540">
    <div data-reveal style="flex:2 1 320px;min-width:0;background:#0B1020;padding:30px 24px;display:flex;flex-direction:column;justify-content:space-between;min-height:230px">
      <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">UNIT / N-01 <span style="color:#FF3D6E">+</span></div>
      <div><span data-count="35" style="font-family:'Archivo Black',sans-serif;font-size:clamp(4rem,10vw,9rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E;display:block">35</span></div>
      <p style="margin:14px 0 0;max-width:46ch;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">hackathons Hackathon Raptors has run since 2023, across 85+ countries. The spec for this event comes out of that.<sup style="color:#FF3D6E"><a href="#ref-15" aria-label="Jump to reference 15">[15]</a></sup></p>
    </div>
    <div data-reveal style="flex:1 1 230px;min-width:0;background:#0B1020;padding:30px 24px;display:flex;flex-direction:column;justify-content:space-between;min-height:230px">
      <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">UNIT / N-02 <span style="color:#FF3D6E">+</span></div>
      <div><span data-count="0" style="font-family:'Archivo Black',sans-serif;font-size:clamp(4rem,8vw,7rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E;display:block">0</span></div>
      <p style="margin:14px 0 0;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">major hackathon platforms publish an official public API. The whole ecosystem runs on scrapers and CSV export.<sup style="color:#FF3D6E"><a href="#ref-14" aria-label="Jump to reference 14">[14]</a></sup></p>
    </div>
    <div data-reveal style="flex:1 1 230px;min-width:0;background:#0B1020;padding:30px 24px;display:flex;flex-direction:column;justify-content:space-between;min-height:230px">
      <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">UNIT / N-03 <span style="color:#FF3D6E">+</span></div>
      <div><span data-count="5" data-suffix=" hours" style="font-family:'Archivo Black',sans-serif;font-size:clamp(3rem,6vw,5rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E;display:block">5 hours</span></div>
      <p style="margin:14px 0 0;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">for one judge to score 30 projects, by the largest platform's own estimate.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup></p>
    </div>
    <div data-reveal style="flex:2 1 320px;min-width:0;background:#FF3D6E;color:#0B1020;padding:30px 24px;display:flex;flex-direction:column;justify-content:space-between;min-height:200px">
      <div style="font:400 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:rgba(10,10,10,.6)">UNIT / N-04 · COUNTDOWN</div>
      <div><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(4rem,10vw,9rem);line-height:.85;letter-spacing:-.05em;color:#0B1020;display:block">72h</span></div>
      <p style="margin:14px 0 0;font:700 12px/1.7 'JetBrains Mono',monospace;color:#0B1020">to build the thing that replaces all of it.</p>
    </div>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:44px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">02</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 02 / THE PROBLEM ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <h2 data-scramble style="margin:0 0 40px;max-width:20ch;font-family:'Archivo Black',sans-serif;font-size:clamp(2rem,6.5vw,5.5rem);line-height:.92;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Running a hackathon is a data problem wearing a party hat.</h2>

  <figure data-reveal style="margin:0 0 52px;border:1px solid #1B2540;background:#0E1428">
    <figcaption style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:#55658C"><span style="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.16em;color:#E6ECFF">FIG. 01 — EVENT PIPELINE / 10 STAGES</span><span style="color:#FF3D6E">FAILURE SURFACE: STAGE 07</span></figcaption>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,108px),1fr));gap:1px;background:#16203A">
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">01</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Registration</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">02</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Teams</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">03</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Submissions</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">04</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Eligibility</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">05</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Assignment</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">06</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Scoring</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#2A0F1E;padding:16px 10px;display:flex;flex-direction:column;gap:8px;outline:1px solid #FF3D6E;outline-offset:-1px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#FF3D6E">07</span><span style="font:700 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Normalization</span><span data-bar="100" style="display:block;height:2px;width:0;background:#FF3D6E;transition:width 1.2s cubic-bezier(.16,1,.3,1)"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">08</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Results</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">09</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Certificates</span><span style="height:2px;background:#26355C"></span></div>
      <div style="background:#0E1428;padding:16px 10px;display:flex;flex-direction:column;gap:8px"><span style="font:700 9px/1 'Space Mono',monospace;letter-spacing:.2em;color:#3A4A70">10</span><span style="font:400 10px/1.35 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#6B7A9E">Archive</span><span style="height:2px;background:#26355C"></span></div>
    </div>
    <div style="display:flex;gap:2px;padding:10px 16px;border-top:1px solid #1B2540;align-items:flex-end;height:26px">
      <span style="width:2px;height:100%;background:#FF3D6E"></span><span style="width:1px;height:60%;background:#3A4A70"></span><span style="width:4px;height:100%;background:#3A4A70"></span><span style="width:1px;height:40%;background:#3A4A70"></span><span style="width:2px;height:80%;background:#3A4A70"></span><span style="width:6px;height:100%;background:#3A4A70"></span><span style="width:1px;height:50%;background:#3A4A70"></span><span style="width:3px;height:100%;background:#3A4A70"></span><span style="width:1px;height:70%;background:#3A4A70"></span><span style="width:5px;height:100%;background:#3A4A70"></span><span style="width:2px;height:45%;background:#3A4A70"></span><span style="width:1px;height:100%;background:#3A4A70"></span><span style="width:4px;height:65%;background:#3A4A70"></span><span style="width:2px;height:100%;background:#FF3D6E"></span>
    </div>
  </figure>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(24px,4vw,64px);align-items:start">
    <div data-reveal style="display:flex;flex-direction:column;gap:22px;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">
      <p style="margin:0;text-wrap:pretty">Registration, teams, submissions, eligibility, judge assignment, scoring, normalization, results, certificates, and an archive somebody can query two years later. Ten stages, each with its own state, each feeding the next. Get one wrong and the part that suffers is the judging, which is the part participants actually came for.</p>
      <p style="margin:0;text-wrap:pretty">Hackathon Raptors has run thirty-five events on this pipeline since 2023, across 85 countries and roughly a dozen a year. That is where the specification for this hackathon comes from. We know which stage breaks first, which one nobody budgets for, and which one every organizer ends up doing by hand on the Sunday night. We have opinions earned the expensive way.</p>
      <p style="margin:0;text-wrap:pretty">The obvious question is why nobody just uses the platforms that already exist. We studied them closely, and the answer is more interesting than "they cost money."</p>
      <p style="margin:0;text-wrap:pretty">The incumbents <span style="color:#E6ECFF;text-decoration:line-through;text-decoration-color:#FF3D6E;text-decoration-thickness:2px">converged</span>. Devpost, Devfolio, TAIKAI, DoraHacks, HackerEarth and Unstop all ship the same nine things: an event microsite, registration, team formation, project submission, a public gallery, judge scoring, community voting, an organizer dashboard, and a CSV export.<sup style="color:#FF3D6E"><a href="#ref-2" aria-label="Jump to reference 2">[2]</a><a href="#ref-6" aria-label="Jump to reference 6">[6]</a><a href="#ref-9" aria-label="Jump to reference 9">[9]</a><a href="#ref-11" aria-label="Jump to reference 11">[11]</a></sup> That list is not exotic. It is a weekend of work for a team that knows what it is doing.</p>
      <p style="margin:0;text-wrap:pretty">Then they <span style="color:#E6ECFF;text-decoration:line-through;text-decoration-color:#FF3D6E;text-decoration-thickness:2px">stopped</span>. The largest platform in the category <strong style="color:#E6ECFF;font-weight:700">cannot weight its judging criteria differently</strong>. Its own documentation tells organizers who need weighted criteria to judge offline in a spreadsheet.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> Devfolio advertises "automatic score normalization" as a headline feature and, like everyone else, <strong style="color:#E6ECFF;font-weight:700">publishes nothing about how it works</strong>.<sup style="color:#FF3D6E"><a href="#ref-6" aria-label="Jump to reference 6">[6]</a><a href="#ref-7" aria-label="Jump to reference 7">[7]</a></sup> Community voting is universally conceded to be gameable: the standard advice is to keep the prize small and hide results until you have manually reviewed the votes.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> And <strong style="color:#E6ECFF;font-weight:700">not one of them has an official public API</strong>, so the integration layer of an entire industry is unofficial scrapers and downloaded spreadsheets.<sup style="color:#FF3D6E"><a href="#ref-14" aria-label="Jump to reference 14">[14]</a></sup></p>
    </div>
    <div data-reveal style="display:flex;flex-direction:column;gap:22px">
      <blockquote data-dither style="margin:0;padding:32px 26px;border:1px solid #FF3D6E;position:relative;overflow:hidden">
        <span style="position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle at center,rgba(10,10,10,.9) 1px,transparent 1.4px);background-size:3px 3px;mix-blend-mode:multiply;opacity:.85"></span>
        <p style="margin:0;position:relative;font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:clamp(1.5rem,3.4vw,2.9rem);line-height:1.06;letter-spacing:-.02em;color:#E6ECFF;animation:glitch 7s steps(1) 3s infinite">Build the platform that will judge you.</p>
        <div style="position:relative;margin-top:20px;font:400 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:#00E5D0">[ PULL QUOTE / DEGRADED · 1-BIT ]</div>
      </blockquote>
      <p style="margin:0;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Meanwhile the open-source tier proves the appetite is real. Gavel came out of HackMIT with a genuine idea inside it: stop asking judges for absolute scores and ask them which of two projects is better, then recover a global ranking with a Bradley-Terry estimator.<sup style="color:#FF3D6E"><a href="#ref-12" aria-label="Jump to reference 12">[12]</a></sup> JunctionApp, Dribdat, Quill and Hibiscus all exist and are all self-hostable.<sup style="color:#FF3D6E"><a href="#ref-13" aria-label="Jump to reference 13">[13]</a></sup> What nobody has assembled is a modern, self-hostable, API-first whole that a working organizer can run on Monday.</p>
      <p style="margin:0;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">That is the gap. It is real, it is narrow, and it fits in 72 hours.</p>
      <p style="margin:0;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Dogfood is a 72-hour hackathon with one product in it. Everyone builds the same thing against the same spec: a submission and judging portal. We publish the spec, a real anonymised dataset, and an acceptance suite you run against your own build. You ship it open source. We take the winner, self-host it, and run our events on it.</p>
      <p style="margin:0;padding:18px 20px;border-left:2px solid #FF3D6E;background:#121A32;font:700 14px/1.7 'JetBrains Mono',monospace;color:#E6ECFF">We are not asking you to build a demo of a platform. We are asking you to build ours.</p>
    </div>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:14px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">03</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 03 / DOSSIER · WHAT HAPPENS TO THE WINNER ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;font:400 10px/1 'JetBrains Mono',monospace;letter-spacing:.18em;color:#4A5A80;margin-bottom:36px">
    <span>CLASSIFICATION / OPEN</span><span>FILE DF-2026-W</span><span>SHEET 1 OF 1</span><span>REV 2.6</span>
  </div>
  <h2 data-scramble style="margin:0 0 12px;font-family:'Archivo Black',sans-serif;font-size:clamp(2rem,6vw,5rem);line-height:.92;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF;max-width:16ch">What happens to the winner</h2>
  <p style="margin:0 0 40px;font:400 12px/1.7 'JetBrains Mono',monospace;letter-spacing:.06em;color:#6B7A9E">The part every other hackathon leaves vague, stated plainly.</p>

  <div style="display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border:1px solid #FF3D6E">
    <div data-reveal style="flex:2 1 340px;min-width:0;background:#0E1428;padding:28px 24px"><div style="font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:14px">01 / You keep your work.</div><p style="margin:0;max-width:60ch;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Ship under MIT or Apache-2.0. The repo is yours. We do not ask for an assignment, a transfer, a CLA, or an exclusivity clause. There is nothing to sign.</p></div>
    <div data-reveal style="flex:1 1 260px;min-width:0;background:#0E1428;padding:28px 24px"><div style="font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:14px">02 / We fork it and run it.</div><p style="margin:0;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">The winning project gets forked, self-hosted, and put into production for Hackathon Raptors events. That is the prize behind the prize.</p></div>
    <div data-reveal style="flex:1 1 260px;min-width:0;background:#0E1428;padding:28px 24px"><div style="font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:14px">03 / You get credited where it counts.</div><p style="margin:0;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Not a thank-you tweet. A credit line on every event page the platform powers, for as long as it powers them.</p></div>
    <div data-reveal style="flex:1 1 260px;min-width:0;background:#0E1428;padding:28px 24px"><div style="font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:14px">04 / We upstream back.</div><p style="margin:0;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Every fix, hardening pass and feature we add on top gets sent back to your repository as a pull request. If you want them, take them. If you have moved on, the fork carries on and the credit stays.</p></div>
    <div data-reveal style="flex:2 1 340px;min-width:0;background:#0E1428;padding:28px 24px"><div style="font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:14px">05 / This is not a maybe.</div><p style="margin:0;max-width:60ch;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">We run roughly a dozen events a year and we intend to run the next decade of them on whatever wins. We are not shopping for inspiration. We are commissioning software, in the open, and paying for it.</p></div>
  </div>
  <p data-reveal style="margin:1px 0 0;padding:24px;border:1px solid #1B2540;border-top:0;background:#0B1020;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#6B7A9E;text-wrap:pretty"><span style="color:#FF3D6E">///</span> One honest caveat, because you deserve it before you spend a weekend: if the top entries are close, we may adopt one and borrow ideas from another, with credit to both. We will say so publicly and in detail. What we will not do is quietly take your architecture and call it ours.</p>
</section>

<section id="tiers" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">04</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 04 / THE TIER LADDER ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:clamp(20px,4vw,56px);align-items:end;margin-bottom:clamp(30px,5vw,60px)">
    <h2 data-scramble style="margin:0;font-family:'Archivo Black',sans-serif;font-size:clamp(2rem,6vw,5rem);line-height:.92;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">The Tier Ladder</h2>
    <p style="margin:0;max-width:52ch;font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:clamp(1.05rem,1.8vw,1.5rem);line-height:1.35;letter-spacing:-.01em;color:#E6ECFF;text-wrap:pretty">No tracks. One product, four tiers. Every team builds against the same published spec, and your score is how far up the ladder you climbed and how cleanly you did it.</p>
  </div>

  <div style="perspective:1600px;perspective-origin:50% 20%">
  <div style="display:flex;flex-direction:column;gap:14px;transform-style:preserve-3d">

    <div data-tier style-hover="border-color:#E6ECFF;background:#121A32" style="background:#0B1020;border:1px solid #1B2540;padding:clamp(20px,3vw,34px);transform:translateZ(-120px) translateY(30px);opacity:.35;transition:transform .8s cubic-bezier(.16,1,.3,1),opacity .8s ease,border-color .4s linear;margin-left:0;margin-right:clamp(0px,9vw,180px);max-width:100%">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid #1B2540;padding-bottom:14px;margin-bottom:20px">
        <div style="display:flex;align-items:baseline;gap:16px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">T1</span><span style="font:600 15px/1 'Archivo',sans-serif;letter-spacing:.34em;text-transform:uppercase;color:#E6ECFF">Core</span></div>
        <span data-tier-status style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">[ LOCKED ]</span>
      </div>
      <p style="margin:0 0 18px;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Required.</strong> A submission that does not clear T1 is not judged. This is the floor, not the target.</p>
      <ul style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px 28px;font:400 12.5px/1.6 'JetBrains Mono',monospace;color:#AEBAD6">
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Authentication and sessions</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>A real role model: visitor, participant, judge, organizer, admin</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Event creation with configurable dates, tracks and prizes</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Team formation by invite link</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Project submission with draft-and-edit until the deadline</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Deadline enforcement that actually holds</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Public gallery with search and filter</span></li>
      </ul>
      <p style="margin:20px 0 0;padding-top:16px;border-top:1px dashed #1B2540;font:400 11.5px/1.75 'JetBrains Mono',monospace;color:#6B7A9E"><strong style="color:#E6ECFF">Reference:</strong> the submission field set is stable across every platform we studied. Name, tagline, long description, thumbnail, image gallery, hosted demo video URL, repository URL, live link, tech tags, track, plus organizer-defined custom questions.<sup style="color:#FF3D6E"><a href="#ref-4" aria-label="Jump to reference 4">[4]</a><a href="#ref-5" aria-label="Jump to reference 5">[5]</a></sup></p>
    </div>

    <div data-tier style-hover="border-color:#E6ECFF;background:#121A32" style="background:#0B1020;border:1px solid #1B2540;padding:clamp(20px,3vw,34px);transform:translateZ(-120px) translateY(30px);opacity:.35;transition:transform .8s cubic-bezier(.16,1,.3,1),opacity .8s ease,border-color .4s linear;margin-left:clamp(0px,3vw,60px);margin-right:clamp(0px,6vw,120px)">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid #1B2540;padding-bottom:14px;margin-bottom:20px">
        <div style="display:flex;align-items:baseline;gap:16px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">T2</span><span style="font:600 15px/1 'Archivo',sans-serif;letter-spacing:.34em;text-transform:uppercase;color:#E6ECFF">Judging</span></div>
        <span data-tier-status style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">[ LOCKED ]</span>
      </div>
      <p style="margin:0 0 18px;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Where the real engineering starts.</p>
      <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Judge invitation and assignment, by batch or algorithmically</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Scoring against a <strong style="color:#E6ECFF">weighted</strong>, organizer-configurable rubric. The market leader cannot weight criteria at all<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup>, and its closest rival ships one fixed five-criterion rubric that every event on the platform shares<sup style="color:#FF3D6E"><a href="#ref-8" aria-label="Jump to reference 8">[8]</a></sup></span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><strong style="color:#E6ECFF">Role isolation, enforced in the backend.</strong> A judge must never see another judge's scores. A track judge must never see another track. If this only works because the UI hides a button, it does not work.</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Live progress dashboard so an organizer can see who has not started</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><strong style="color:#E6ECFF">Cross-judge normalization</strong>, with your method documented and defended</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>CSV export at every stage</span></li>
      </ul>
    </div>

    <div data-tier style-hover="border-color:#E6ECFF;background:#121A32" style="background:#0B1020;border:1px solid #1B2540;padding:clamp(20px,3vw,34px);transform:translateZ(-120px) translateY(30px);opacity:.35;transition:transform .8s cubic-bezier(.16,1,.3,1),opacity .8s ease,border-color .4s linear;margin-left:clamp(0px,6vw,120px);margin-right:clamp(0px,3vw,60px)">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid #1B2540;padding-bottom:14px;margin-bottom:20px">
        <div style="display:flex;align-items:baseline;gap:16px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">T3</span><span style="font:600 15px/1 'Archivo',sans-serif;letter-spacing:.34em;text-transform:uppercase;color:#E6ECFF">Public</span></div>
        <span data-tier-status style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">[ LOCKED ]</span>
      </div>
      <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Community voting with configurable access: open link, email-gated, or authenticated<sup style="color:#FF3D6E"><a href="#ref-3" aria-label="Jump to reference 3">[3]</a></sup></span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Or something better than one-person-one-vote, if you can defend it. Quadratic voting, where casting n votes on one project costs the square root of n in influence, is the most credible attempt anyone has shipped at stopping a loud minority from deciding the outcome<sup style="color:#FF3D6E"><a href="#ref-10" aria-label="Jump to reference 10">[10]</a></sup></span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Comments on gallery projects</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Results hidden from everyone but organizers during the voting window<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup></span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Randomised project ordering on ballots, to kill position bias<sup style="color:#FF3D6E"><a href="#ref-3" aria-label="Jump to reference 3">[3]</a></sup></span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Anti-abuse that means something: rate limits, duplicate detection, and an audit trail an organizer can read without a database client</span></li>
      </ul>
    </div>

    <div data-tier style-hover="border-color:#E6ECFF;background:#121A32" style="background:#0B1020;border:1px solid #1B2540;padding:clamp(20px,3vw,34px);transform:translateZ(-120px) translateY(30px);opacity:.35;transition:transform .8s cubic-bezier(.16,1,.3,1),opacity .8s ease,border-color .4s linear;margin-left:clamp(0px,9vw,180px);margin-right:0">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid #1B2540;padding-bottom:14px;margin-bottom:20px">
        <div style="display:flex;align-items:baseline;gap:16px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">T4</span><span style="font:600 15px/1 'Archivo',sans-serif;letter-spacing:.34em;text-transform:uppercase;color:#E6ECFF">Stretch</span></div>
        <span data-tier-status style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">[ LOCKED ]</span>
      </div>
      <ul style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px 28px;font:400 12.5px/1.6 'JetBrains Mono',monospace;color:#AEBAD6">
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>A REST API and webhooks covering every action the UI can take</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Certificate and record generation</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Signed, publicly verifiable judge participation records</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>An embeddable gallery widget</span></li>
        <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Bulk import and export, so an organizer can leave as easily as they arrived</span></li>
      </ul>
    </div>
  </div>
  </div>

  <figure data-reveal style="margin:26px 0 0;border:1px solid #1B2540;background:#0E1428">
    <figcaption style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:#55658C"><span style="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.16em;color:#E6ECFF">FIG. 04 — JUDGE ASSIGNMENT / BATCHED, DISJOINT</span><span style="color:#FF3D6E">NO JUDGE SEES A PEER'S BALLOT</span></figcaption>
    <svg viewBox="0 0 600 240" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:auto;background:#0E1428">
      <line x1="0" y1="40" x2="600" y2="40" stroke="#16203A" stroke-width="1"></line>
      <line x1="0" y1="200" x2="600" y2="200" stroke="#16203A" stroke-width="1"></line>
      <line x1="130" y1="60" x2="470" y2="60" stroke="#1B2540" stroke-width="1"></line>
      <line x1="130" y1="60" x2="470" y2="120" stroke="#00E5D0" stroke-width="1" opacity="0.75"></line>
      <line x1="130" y1="105" x2="470" y2="60" stroke="#00E5D0" stroke-width="1" opacity="0.75"></line>
      <line x1="130" y1="105" x2="470" y2="180" stroke="#1B2540" stroke-width="1"></line>
      <line x1="130" y1="150" x2="470" y2="120" stroke="#00E5D0" stroke-width="1" opacity="0.75"></line>
      <line x1="130" y1="150" x2="470" y2="180" stroke="#1B2540" stroke-width="1"></line>
      <line x1="130" y1="195" x2="470" y2="180" stroke="#FF3D6E" stroke-width="1.5"></line>
      <line x1="130" y1="195" x2="470" y2="60" stroke="#1B2540" stroke-width="1"></line>
      <circle cx="130" cy="60" r="5" fill="#00E5D0"></circle>
      <circle cx="130" cy="105" r="5" fill="#00E5D0"></circle>
      <circle cx="130" cy="150" r="5" fill="#00E5D0"></circle>
      <circle cx="130" cy="195" r="5" fill="#FF3D6E"></circle>
      <rect x="464" y="54" width="12" height="12" fill="#E6ECFF"></rect>
      <rect x="464" y="114" width="12" height="12" fill="#E6ECFF"></rect>
      <rect x="464" y="174" width="12" height="12" fill="#E6ECFF"></rect>
      <text x="20" y="24" fill="#55658C" font-family="Space Mono, monospace" font-size="11" letter-spacing="2">JUDGES</text>
      <text x="510" y="24" fill="#55658C" font-family="Space Mono, monospace" font-size="11" letter-spacing="2">PROJECTS</text>
      <text x="20" y="64" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">J-01</text>
      <text x="20" y="109" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">J-02</text>
      <text x="20" y="154" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">J-03</text>
      <text x="20" y="199" fill="#FF3D6E" font-family="Space Mono, monospace" font-size="11">J-04</text>
      <text x="510" y="64" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">P-118</text>
      <text x="510" y="124" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">P-204</text>
      <text x="510" y="184" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="11">P-391</text>
      <text x="20" y="228" fill="#3A4A70" font-family="Space Mono, monospace" font-size="10" letter-spacing="1.5">BATCH 03 / 40 PROJECTS · 30 JUDGES · 3 REVIEWS PER PROJECT</text>
    </svg>
  </figure>

  <figure data-reveal style="margin:14px 0 0;border:1px solid #1B2540;background:#0E1428;overflow-x:auto">
    <figcaption style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:#55658C"><span style="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.16em;color:#E6ECFF">FIG. 02 — ROLE ISOLATION MATRIX / BACKEND-ENFORCED</span><span style="color:#00E5D0">● EXPECTED</span></figcaption>
    <table style="width:100%;min-width:560px;font:400 10.5px/1 'Space Mono',monospace">
      <thead><tr>
        <th style="text-align:left;padding:12px 14px;border-bottom:1px solid #1B2540;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#55658C">Actor</th>
        <th style="padding:12px 8px;border-bottom:1px solid #1B2540;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#55658C">Own scores</th>
        <th style="padding:12px 8px;border-bottom:1px solid #1B2540;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#55658C">Peer scores</th>
        <th style="padding:12px 8px;border-bottom:1px solid #1B2540;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#55658C">Other track</th>
        <th style="padding:12px 8px;border-bottom:1px solid #1B2540;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#55658C">Aggregate</th>
        <th style="padding:12px 8px;border-bottom:1px solid #1B2540;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#55658C">Audit log</th>
      </tr></thead>
      <tbody>
        <tr><td style="padding:12px 14px;border-bottom:1px solid #141D38;color:#E6ECFF;letter-spacing:.1em">VISITOR</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td></tr>
        <tr><td style="padding:12px 14px;border-bottom:1px solid #141D38;color:#E6ECFF;letter-spacing:.1em">PARTICIPANT</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td></tr>
        <tr><td style="padding:12px 14px;border-bottom:1px solid #141D38;color:#E6ECFF;letter-spacing:.1em">JUDGE</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#FF3D6E">✗</td></tr>
        <tr><td style="padding:12px 14px;border-bottom:1px solid #141D38;color:#E6ECFF;letter-spacing:.1em">ORGANIZER</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;border-bottom:1px solid #141D38;text-align:center;color:#00E5D0">+</td></tr>
        <tr><td style="padding:12px 14px;color:#E6ECFF;letter-spacing:.1em">ADMIN</td><td style="padding:12px 8px;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;text-align:center;color:#00E5D0">+</td><td style="padding:12px 8px;text-align:center;color:#00E5D0">+</td></tr>
      </tbody>
    </table>
    <div style="padding:10px 16px;border-top:1px solid #1B2540;font:400 9.5px/1.6 'Space Mono',monospace;letter-spacing:.16em;color:#3A4A70">+ PERMITTED &nbsp;·&nbsp; ✗ DENIED AT THE API, NOT IN THE UI &nbsp;·&nbsp; VERIFIED BY ACCEPTANCE SUITE T2.03</div>
  </figure>
  <p data-reveal style="margin:20px 0 0;padding:20px 24px;border:1px solid #FF3D6E;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Climb honestly.</strong> A clean, correct T2 scores above a broken T4 every time. Judges are reading for what works, not what is listed in your README.</p>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">05</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 05 / WHAT COUNTS AS DONE ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(24px,4vw,64px);align-items:start">
    <div>
      <h2 data-scramble style="margin:0 0 16px;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">What counts as done</h2>
      <p style="margin:0 0 26px;font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:clamp(1.05rem,1.8vw,1.5rem);line-height:1.35;letter-spacing:-.01em;color:#6B7A9E">The one rule that makes this judgeable, and it is verifiable in about a minute.</p>
      <p data-reveal style="margin:0 0 18px;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><kbd style="font-family:'JetBrains Mono',monospace;background:#FF3D6E;color:#0B1020;padding:2px 6px;font-weight:700">docker compose up</kbd> <strong style="color:#E6ECFF">produces a working portal.</strong> On localhost. Seeded with the fixture data we publish at kickoff. No cloud account, no API key, no external service, no signup.</p>
      <p data-reveal style="margin:0;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">The acceptance suite runs against your build</strong> and prints a tier-by-tier pass report. Publish that output in your repository. A judge should be able to confirm which tier you reached without reading a line of your code.</p>
    </div>
    <div data-reveal style="border:1px solid #FF3D6E">
      <div style="padding:14px 20px;border-bottom:1px solid #00E5D0;font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E">[ CLOSED LOOPHOLES, NAMED UP FRONT ]</div>
      <ul style="list-style:none;margin:0;padding:0">
        <li style="padding:18px 20px;border-bottom:1px solid #1B2540;display:flex;gap:12px;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#FF3D6E">&rarr;</span><span>A hosted database service is a dependency on someone else's uptime and someone else's invoice. It must run locally.</span></li>
        <li style="padding:18px 20px;border-bottom:1px solid #1B2540;display:flex;gap:12px;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#FF3D6E">&rarr;</span><span>Authentication-as-a-service is the same problem wearing a nicer hat. Build it or use something self-hosted.</span></li>
        <li style="padding:18px 20px;border-bottom:1px solid #1B2540;display:flex;gap:12px;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#FF3D6E">&rarr;</span><span>A staging URL is not a submission. We need to run it, not visit it.</span></li>
        <li style="padding:18px 20px;display:flex;gap:12px;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#FF3D6E">&rarr;</span><span>"Works on my machine" has never once been true.</span></li>
      </ul>
      <p style="margin:0;padding:18px 20px;border-top:1px solid #00E5D0;background:#121A32;font:700 12.5px/1.75 'JetBrains Mono',monospace;color:#E6ECFF">If it does not come up on a laptop with the network off, we cannot adopt it, and adoption is the entire point of the event.</p>
    </div>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">06</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 06 / DELIVERABLES ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(24px,4vw,56px);align-items:start">
    <div>
      <h2 data-scramble style="margin:0 0 14px;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Deliverables</h2>
      <p style="margin:0 0 26px;font:400 12.5px/1.85 'IBM Plex Mono',monospace;color:#6B7A9E">After 72 hours we want software an organizer could run. Not a design system. Not a slide deck.</p>
      <div data-reveal style="display:flex;flex-direction:column;gap:16px;font:400 13px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">
        <p style="margin:0"><strong style="color:#E6ECFF">A working portal.</strong> It starts with one command, seeds itself, and takes a project from submission through judging to published results.</p>
        <p style="margin:0"><strong style="color:#E6ECFF">An acceptance report.</strong> The output of our suite against your build, committed to the repository. This is your tier claim and your receipt at the same time.</p>
        <p style="margin:0"><strong style="color:#E6ECFF">Honest documentation.</strong> <samp style="color:#FF3D6E">ARCHITECTURE.md</samp> for how it fits together, <samp style="color:#FF3D6E">DATA-MODEL.md</samp> for the schema and how an organizer gets data in and out, <samp style="color:#FF3D6E">JUDGING.md</samp> for your scoring maths. These are read by judges and they carry weight.</p>
      </div>
      <div data-reveal style="margin-top:26px;border-top:1px solid #1B2540;padding-top:20px">
        <div style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:16px">You'll submit:</div>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;font:400 12.5px/1.65 'JetBrains Mono',monospace;color:#AEBAD6">
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>Public GitHub repo under an OSI-approved license</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>docker compose up</samp> to a seeded, working portal</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>acceptance-report.txt</samp>: the suite output, tier by tier</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>README.md</samp>: what it does, how to run it, what it does not do yet</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>ARCHITECTURE.md</samp>: the shape of the system and why</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>DATA-MODEL.md</samp>: schema, plus import and export paths</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span><samp>JUDGING.md</samp>: assignment strategy, scoring maths, normalization method, defended</span></li>
          <li style="display:flex;gap:10px"><span style="color:#FF3D6E">&rarr;</span><span>5-minute demo video walking one full event lifecycle: create, submit, judge, publish</span></li>
        </ul>
      </div>
    </div>
    <div>
      <div style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:16px">[ ANATOMY OF A SUBMISSION ]</div>
      <p style="margin:0 0 18px;font:400 12.5px/1.85 'IBM Plex Mono',monospace;color:#6B7A9E">What a serious submission looks like on disk.</p>
      <pre data-reveal class="tree-block" style="margin:0;max-width:100%;padding:clamp(14px,1.4vw,22px) clamp(12px,1.4vw,20px);border:1px solid #FF3D6E;background:#0E1428;overflow-x:auto;font-family:'Courier Prime',monospace;font-weight:700;line-height:1.8;color:#AEBAD6"> your-portal/
 ├── README.md              <span style="color:#FF3D6E">← what it does, how to run, honest limits</span>
 ├── ARCHITECTURE.md        <span style="color:#FF3D6E">← the shape of the system and why</span>
 ├── DATA-MODEL.md          <span style="color:#FF3D6E">← schema, import and export paths</span>
 ├── JUDGING.md             <span style="color:#FF3D6E">← assignment, scoring maths, normalization</span>
 ├── docker-compose.yml     <span style="color:#FF3D6E">← one command to a seeded, running portal</span>
 ├── src/                   <span style="color:#FF3D6E">← your code, all of it written this weekend</span>
 ├── tests/                 <span style="color:#FF3D6E">← your own tests, beyond the acceptance suite</span>
 ├── acceptance-report.txt  <span style="color:#FF3D6E">← our suite's output, tier by tier</span>
 ├── LICENSE                <span style="color:#FF3D6E">← MIT or Apache-2.0</span>
 └── .dogfood.toml          <span style="color:#FF3D6E">← tiers claimed, one-line pitch</span></pre>
      <div data-reveal style="margin-top:20px;display:flex;flex-direction:column;gap:14px;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">
        <p style="margin:0"><strong style="color:#E6ECFF">One command runs it.</strong> <samp style="color:#FF3D6E">docker compose up</samp>, seeded, working. If a judge has to read your CI config to figure out how to start it, you have failed this rule.</p>
        <p style="margin:0"><strong style="color:#E6ECFF">The acceptance report is the receipt.</strong> Claim T3 in your README and pass T2 in the report, and you score T2 with a note about the gap.</p>
        <p style="margin:0"><strong style="color:#E6ECFF">JUDGING.md counts.</strong> It feeds straight into Judging Integrity (25%). "We averaged the scores" is an answer, and it is a weak one. Tell us what you did about the judge who marks everything a 3.</p>
        <p style="margin:0"><strong style="color:#E6ECFF">Honest tier claims beat inflated ones.</strong> A team that says "we reached T2, here is the T3 work we started and did not finish" scores above a team claiming T4 with three broken endpoints.</p>
        <p style="margin:0;color:#6B7A9E">Layout is advisory. Judges read what you actually ship.</p>
      </div>
    </div>
  </div>
</section>

<section id="scoring" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">07</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 07 / SCORING ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(20px,4vw,56px);align-items:end;margin-bottom:44px">
    <h2 data-scramble style="margin:0;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5.5vw,4.5rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Scoring</h2>
    <p style="margin:0;max-width:56ch;font-family:'DM Serif Display',serif;font-style:italic;font-weight:400;font-size:clamp(1.15rem,2vw,1.65rem);line-height:1.3;letter-spacing:-.01em;color:#E6ECFF">Each project is rated on a 5-point scale across four weighted criteria. Final ranking is the weighted average across all judges who evaluated the project.</p>
  </div>

  <div style="display:flex;flex-direction:column;gap:1px;background:#1B2540;border:1px solid #1B2540">
    <div data-reveal style="background:#0E1428;padding:26px clamp(16px,2.5vw,30px);display:grid;grid-template-columns:minmax(0,1fr);gap:16px">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:baseline"><h3 style="margin:0;font:600 clamp(1.05rem,1.9vw,1.5rem)/1.15 'Archivo',sans-serif;letter-spacing:-.01em;text-transform:uppercase;color:#E6ECFF">Tier Completion &amp; Correctness</h3><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">40%</span></div>
      <div style="height:10px;background:#141D38;border:1px solid #1B2540"><span data-bar="40" style="display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,#FF3D6E,#FF3D6E 6px,#0E1428 6px,#0E1428 8px);transition:width 1.1s cubic-bezier(.16,1,.3,1)"></span></div>
      <p style="margin:0;max-width:88ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">How far up the ladder you got, verified by the acceptance suite rather than by your README. T1 is a gate, not a score. Above that, correctness beats breadth: a clean T2 outranks a T4 with three features that half-work. Honest gap reporting is rewarded, inflated claims are penalised here.</p>
    </div>
    <div data-reveal style="background:#0E1428;padding:26px clamp(16px,2.5vw,30px);display:grid;gap:16px">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:baseline"><h3 style="margin:0;font:600 clamp(1.05rem,1.9vw,1.5rem)/1.15 'Archivo',sans-serif;letter-spacing:-.01em;text-transform:uppercase;color:#E6ECFF">Judging Integrity</h3><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">25%</span></div>
      <div style="height:10px;background:#141D38;border:1px solid #1B2540"><span data-bar="25" style="display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,#FF3D6E,#FF3D6E 6px,#0E1428 6px,#0E1428 8px);transition:width 1.1s cubic-bezier(.16,1,.3,1)"></span></div>
      <p style="margin:0;max-width:88ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">The hard part, weighted like it. Is role isolation enforced in the backend or painted on the frontend? Is your normalization method documented and defensible, or did you average the scores and hope? Is there an audit trail an organizer can actually read? Did you think about vote abuse before a judge asked?</p>
    </div>
    <div data-reveal style="background:#0E1428;padding:26px clamp(16px,2.5vw,30px);display:grid;gap:16px">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:baseline"><h3 style="margin:0;font:600 clamp(1.05rem,1.9vw,1.5rem)/1.15 'Archivo',sans-serif;letter-spacing:-.01em;text-transform:uppercase;color:#E6ECFF">Adoptability &amp; Operability</h3><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">20%</span></div>
      <div style="height:10px;background:#141D38;border:1px solid #1B2540"><span data-bar="20" style="display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,#FF3D6E,#FF3D6E 6px,#0E1428 6px,#0E1428 8px);transition:width 1.1s cubic-bezier(.16,1,.3,1)"></span></div>
      <p style="margin:0;max-width:88ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Could we run this on Monday? One command to running. Seeded with real data. Documentation a stranger can follow without asking you a question. A migration path in and out, because a platform you cannot leave is a trap. A clean license with no surprises.</p>
    </div>
    <div data-reveal style="background:#0E1428;padding:26px clamp(16px,2.5vw,30px);display:grid;gap:16px">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:baseline"><h3 style="margin:0;font:600 clamp(1.05rem,1.9vw,1.5rem)/1.15 'Archivo',sans-serif;letter-spacing:-.01em;text-transform:uppercase;color:#E6ECFF">Code Quality &amp; Innovation</h3><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.6vw,3rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">15%</span></div>
      <div style="height:10px;background:#141D38;border:1px solid #1B2540"><span data-bar="15" style="display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,#FF3D6E,#FF3D6E 6px,#0E1428 6px,#0E1428 8px);transition:width 1.1s cubic-bezier(.16,1,.3,1)"></span></div>
      <p style="margin:0;max-width:88ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Does it read as idiomatic to a senior reviewer in your stack? Is the schema one a database person would defend? And the part we cannot specify in advance: the decision that made a judge stop and say they would steal it.</p>
    </div>
  </div>

  <figure data-reveal style="margin:28px 0 0;border:1px solid #1B2540;background:#0B1020">
    <figcaption style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:#55658C"><span style="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.16em;color:#E6ECFF">FIG. 03 — WEIGHT DISTRIBUTION / FINAL SCORE</span><span>Σ = 100 · SCALE 1–5</span></figcaption>
    <div style="display:flex;height:56px">
      <div style="flex:40;background:#FF3D6E;display:flex;align-items:center;padding-left:14px;font:700 10px/1 'Space Mono',monospace;letter-spacing:.18em;color:#0B1020;min-width:0;overflow:hidden">40 TIER</div>
      <div style="flex:25;background:#B32A50;display:flex;align-items:center;padding-left:14px;font:700 10px/1 'Space Mono',monospace;letter-spacing:.18em;color:#0B1020;min-width:0;overflow:hidden">25 INTEGRITY</div>
      <div style="flex:20;background:#6B1730;display:flex;align-items:center;padding-left:14px;font:700 10px/1 'Space Mono',monospace;letter-spacing:.18em;color:#E6ECFF;min-width:0;overflow:hidden">20 ADOPT</div>
      <div style="flex:15;background:#1B2540;display:flex;align-items:center;padding-left:14px;font:700 10px/1 'Space Mono',monospace;letter-spacing:.18em;color:#6B7A9E;min-width:0;overflow:hidden">15 CODE</div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:1px;background:#16203A;border-top:1px solid #1B2540">
      <div style="background:#0B1020;padding:18px 16px">
        <div style="font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.2em;color:#55658C;margin-bottom:14px">RAW JUDGE SPREAD / 5 JUDGES</div>
        <div style="display:flex;align-items:flex-end;gap:8px;height:74px">
          <span style="flex:1;height:52%;background:#3A4A70"></span><span style="flex:1;height:88%;background:#3A4A70"></span><span style="flex:1;height:34%;background:#3A4A70"></span><span style="flex:1;height:61%;background:#3A4A70"></span><span style="flex:1;height:100%;background:#3A4A70"></span>
        </div>
        <div style="margin-top:10px;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.16em;color:#3A4A70">σ = 0.94 · UNCALIBRATED</div>
      </div>
      <div style="background:#0B1020;padding:18px 16px">
        <div style="font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.2em;color:#FF3D6E;margin-bottom:14px">NORMALIZED / SAME 5 JUDGES</div>
        <div style="display:flex;align-items:flex-end;gap:8px;height:74px">
          <span style="flex:1;height:64%;background:#FF3D6E"></span><span style="flex:1;height:72%;background:#FF3D6E"></span><span style="flex:1;height:58%;background:#FF3D6E"></span><span style="flex:1;height:67%;background:#FF3D6E"></span><span style="flex:1;height:76%;background:#FF3D6E"></span>
        </div>
        <div style="margin-top:10px;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.16em;color:#55658C">σ = 0.31 · METHOD DOCUMENTED</div>
      </div>
      <div style="background:#0B1020;padding:18px 16px;display:flex;flex-direction:column;justify-content:space-between">
        <div style="font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.2em;color:#55658C">RANK MOVEMENT</div>
        <div style="display:flex;flex-direction:column;gap:7px;font:400 10.5px/1 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E">
          <span><span style="color:#00E5D0">▲ 4</span> &nbsp;PROJECT 17</span>
          <span><span style="color:#00E5D0">▲ 1</span> &nbsp;PROJECT 04</span>
          <span><span style="color:#FF3D6E">▼ 3</span> &nbsp;PROJECT 22</span>
          <span><span style="color:#FF3D6E">▼ 6</span> &nbsp;PROJECT 09</span>
        </div>
        <div style="font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.16em;color:#3A4A70">FIXTURE SET · 40 PROJECTS</div>
      </div>
    </div>
  </figure>

  <div style="margin-top:52px;display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:12px 24px;padding-bottom:16px;border-bottom:1px solid #1B2540">
    <div style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E">[ BONUS CHALLENGES ]</div>
    <p style="margin:0;font:400 12.5px/1.6 'IBM Plex Mono',monospace;color:#6B7A9E">Optional. Pick one and nail it. Do not half-do all four.</p>
  </div>

  <div style="display:flex;flex-wrap:wrap;gap:clamp(18px,2.5vw,32px);margin-top:24px;align-items:stretch">
    <div style="flex:2 1 380px;min-width:0;display:flex"><div data-reveal style="overflow-x:auto"><table style="width:100%;min-width:320px;border:1px solid #1B2540;font:400 12px/1.5 'JetBrains Mono',monospace">
        <thead><tr style="background:#121A32"><th style="text-align:left;padding:12px 14px;border-bottom:1px solid #00E5D0;font:700 10px/1 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#6B7A9E">Challenge</th><th style="text-align:left;padding:12px 14px;border-bottom:1px solid #00E5D0;font:700 10px/1 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#6B7A9E">Difficulty</th><th style="text-align:right;padding:12px 14px;border-bottom:1px solid #00E5D0;font:700 10px/1 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#6B7A9E">Points</th></tr></thead>
        <tbody>
          <tr style="transition:background .12s linear" style-hover="background:#151F3C"><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#E6ECFF">Normalization Proof</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#6B7A9E">Hard</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;text-align:right;color:#FF3D6E;font-weight:700">+5</td></tr>
          <tr style="transition:background .12s linear" style-hover="background:#151F3C"><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#E6ECFF">Pairwise Mode</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#6B7A9E">Hard</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;text-align:right;color:#FF3D6E;font-weight:700">+5</td></tr>
          <tr style="transition:background .12s linear" style-hover="background:#151F3C"><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#E6ECFF">Threat Model</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;color:#6B7A9E">Medium</td><td style="padding:12px 14px;border-bottom:1px solid #16203A;text-align:right;color:#FF3D6E;font-weight:700">+3</td></tr>
          <tr style="transition:background .12s linear" style-hover="background:#151F3C"><td style="padding:12px 14px;color:#E6ECFF">API First</td><td style="padding:12px 14px;color:#6B7A9E">Medium</td><td style="padding:12px 14px;text-align:right;color:#FF3D6E;font-weight:700">+3</td></tr>
        </tbody>
      </table></div></div>
    <div style="flex:1 1 250px;min-width:0;display:flex;flex-wrap:wrap;align-items:stretch;gap:1px;background:#1B2540;border:1px solid #1B2540">
      <div style="background:#0E1428;padding:18px 16px;flex:1 1 120px;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:8px">
        <span style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,4.5vw,3.4rem);line-height:.9;letter-spacing:-.05em;color:#FF3D6E">+16</span>
        <span style="font:400 15px/1.4 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">MAXIMUM IF YOU TOOK ALL FOUR. NOBODY SHOULD.</span>
        <span style="font:400 15px/1.4 'VT323',monospace;letter-spacing:.14em;color:#00E5D0">BONUSES BREAK TIES. THEY DO NOT CHANGE YOUR SCORE.</span>
      </div>
      <div style="background:#0E1428;padding:18px 16px;flex:1 1 120px;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:8px">
        <span style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,4.5vw,3.4rem);line-height:.9;letter-spacing:-.05em;color:#00E5D0">1</span>
        <span style="font:400 15px/1.4 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">DONE PROPERLY BEATS FOUR STARTED.</span>
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1px;background:#1B2540;border:1px solid #1B2540;margin-top:clamp(18px,2.5vw,32px)">
    <div data-reveal style="background:#0E1428;padding:20px"><div style="display:flex;justify-content:space-between;gap:12px;font:400 17px/1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:12px"><span>Normalization Proof</span><span style="color:#FF3D6E">+5 · Hard</span></div><p style="margin:0;font:400 12px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">Implement cross-judge score normalization and prove it works on the fixture data. Show the raw scores, the normalized scores, and the ranking change. Document the method well enough that a statistician would not wince. Every commercial platform claims to do this and none of them will tell you how.<sup style="color:#FF3D6E"><a href="#ref-6" aria-label="Jump to reference 6">[6]</a><a href="#ref-7" aria-label="Jump to reference 7">[7]</a></sup></p></div>
        <div data-reveal style="background:#0E1428;padding:20px"><div style="display:flex;justify-content:space-between;gap:12px;font:400 17px/1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:12px"><span>Pairwise Mode</span><span style="color:#FF3D6E">+5 · Hard</span></div><p style="margin:0;font:400 12px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">Ship pairwise comparison as an alternative judging mode: show a judge two projects, ask which is better, recover a global ranking with a Bradley-Terry style estimator. This is the Gavel approach, and it sidesteps cross-judge calibration entirely by never asking for an absolute score.<sup style="color:#FF3D6E"><a href="#ref-12" aria-label="Jump to reference 12">[12]</a></sup> Hard to get right, extremely satisfying when it works.</p></div>
        <div data-reveal style="background:#0E1428;padding:20px"><div style="display:flex;justify-content:space-between;gap:12px;font:400 17px/1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:12px"><span>Threat Model</span><span style="color:#FF3D6E">+3 · Medium</span></div><p style="margin:0;font:400 12px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">A written, defensible threat model for voting and submission abuse. Sybil votes, ballot stuffing, submission scraping, judge collusion, deadline gaming. Name the attacks you stopped, and name the ones you did not. The honest list is worth more than the heroic one.</p></div>
        <div data-reveal style="background:#0E1428;padding:20px"><div style="display:flex;justify-content:space-between;gap:12px;font:400 17px/1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:12px"><span>API First</span><span style="color:#FF3D6E">+3 · Medium</span></div><p style="margin:0;font:400 12px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">Every action available in the UI is available through a documented API, with a published OpenAPI spec. Nobody else in this category has one.<sup style="color:#FF3D6E"><a href="#ref-14" aria-label="Jump to reference 14">[14]</a></sup> Be the first.</p></div>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">08</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 08 / OUT OF SCOPE ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:clamp(20px,3vw,44px);align-items:flex-start">
    <div style="flex:1 1 280px;max-width:360px;min-width:0;display:flex;flex-direction:column;gap:18px;position:sticky;top:118px">
      <h2 data-scramble style="margin:0;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,4.6vw,3.6rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Out of Scope</h2>
      <p style="margin:0;font:400 12.5px/1.85 'IBM Plex Mono',monospace;color:#6B7A9E">Save yourself the trouble. These will not score well.</p>
      <div style="display:flex;flex-wrap:wrap;align-items:stretch;gap:1px;background:#1B2540;border:1px solid #1B2540">
        <div style="flex:1 1 120px;min-width:0;background:#0B1020;padding:18px 16px;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:8px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.4vw,2.6rem);line-height:.9;letter-spacing:-.05em;color:#FF3D6E">09</span><span style="font:400 15px/1.35 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">WAYS TO SCORE NOTHING</span></div>
        <div style="flex:1 1 120px;min-width:0;background:#0B1020;padding:18px 16px;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:8px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.8rem,3.4vw,2.6rem);line-height:.9;letter-spacing:-.05em;color:#00E5D0">1</span><span style="font:400 15px/1.35 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">TEST THEY ALL FAIL</span></div>
      </div>
      <p style="margin:0;padding:18px 20px;border:1px solid #FF3D6E;font:700 12.5px/1.75 'JetBrains Mono',monospace;color:#E6ECFF">We are not against using a framework. We are against handing us something we cannot run.</p>
    </div>
    <ul data-reveal style="flex:999 1 440px;min-width:0;list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px;background:#1B2540;border:1px solid #1B2540">
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">01</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Design mockups, Figma files, or a frontend with hardcoded data behind it</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">02</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Anything that needs a cloud account, a hosted database, or an auth provider to start</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">03</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">An authentication demo that stops at the login screen</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">04</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">A gallery with no judging, or judging with no gallery, this is one product</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">05</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Role checks that live only in the frontend, if I can curl another judge's scores it is not isolation</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">06</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">LLM dumps with no architecture document and nobody able to defend the schema in writing</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">07</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Closed source, or a license that is not OSI-approved</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">08</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Anything requiring custom hardware, GUI toolchains, or proprietary services, keep it laptop-friendly</span>
      </li>
      <li style="display:grid;grid-template-columns:38px 20px minmax(0,1fr);align-items:baseline;gap:0 12px;background:#0B1020;padding:15px 18px">
        <span style="font:400 11px/1.7 'Space Mono',monospace;letter-spacing:.12em;color:#3A4A70">09</span>
        <span style="font:700 12.5px/1.7 'JetBrains Mono',monospace;color:#FF3D6E">✗</span>
        <span style="font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">A rewrite of an existing open-source platform with the name changed</span>
      </li>
    </ul>
  </div>
</section>

<section id="timeline" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">09</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 09 / TIMELINE · ALL TIMES UTC · 2026 ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <h2 data-scramble style="margin:0 0 26px;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5.5vw,4.5rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Timeline</h2>

  <figure data-reveal style="margin:0 0 44px;border:1px solid #1B2540;background:#0B1020">
    <figcaption style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;font:400 9.5px/1 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:#55658C"><span style="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.16em;color:#E6ECFF">FIG. 05 — THE 72-HOUR WINDOW</span><span>T-0 = 25.09.2026 / 18:00 UTC</span></figcaption>
    <svg viewBox="0 0 900 130" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:auto">
      <rect x="0" y="52" width="900" height="26" fill="#121A32"></rect>
      <rect x="0" y="52" width="300" height="26" fill="#16203A"></rect>
      <rect x="300" y="52" width="300" height="26" fill="#1B2540"></rect>
      <rect x="600" y="52" width="300" height="26" fill="#2A0F1E"></rect>
      <line x1="0" y1="52" x2="900" y2="52" stroke="#00E5D0" stroke-width="1"></line>
      <line x1="0" y1="78" x2="900" y2="78" stroke="#1B2540" stroke-width="1"></line>
      <line x1="0" y1="44" x2="0" y2="86" stroke="#00E5D0" stroke-width="2"></line>
      <line x1="300" y1="44" x2="300" y2="86" stroke="#00E5D0" stroke-width="1"></line>
      <line x1="600" y1="44" x2="600" y2="86" stroke="#00E5D0" stroke-width="1"></line>
      <line x1="899" y1="40" x2="899" y2="90" stroke="#FF3D6E" stroke-width="3"></line>
      <line x1="75" y1="60" x2="75" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="150" y1="58" x2="150" y2="72" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="225" y1="60" x2="225" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="375" y1="60" x2="375" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="450" y1="58" x2="450" y2="72" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="525" y1="60" x2="525" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="675" y1="60" x2="675" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="750" y1="58" x2="750" y2="72" stroke="#3A4A70" stroke-width="1"></line>
      <line x1="825" y1="60" x2="825" y2="70" stroke="#3A4A70" stroke-width="1"></line>
      <text x="6" y="34" fill="#00E5D0" font-family="Space Mono, monospace" font-size="13" letter-spacing="2">T-0 KICKOFF</text>
      <text x="306" y="34" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="13" letter-spacing="2">+24H</text>
      <text x="606" y="34" fill="#6B7A9E" font-family="Space Mono, monospace" font-size="13" letter-spacing="2">+48H</text>
      <text x="893" y="34" fill="#FF3D6E" font-family="Space Mono, monospace" font-size="13" letter-spacing="2" text-anchor="end">+72H FREEZE</text>
      <text x="6" y="108" fill="#3A4A70" font-family="Space Mono, monospace" font-size="12" letter-spacing="1.5">SCHEMA / AUTH / SUBMISSION</text>
      <text x="306" y="108" fill="#3A4A70" font-family="Space Mono, monospace" font-size="12" letter-spacing="1.5">JUDGING / NORMALIZATION</text>
      <text x="606" y="108" fill="#8A4A66" font-family="Space Mono, monospace" font-size="12" letter-spacing="1.5">ACCEPTANCE / DOCS / VIDEO</text>
    </svg>
  </figure>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(20px,3vw,44px);align-items:start">
    <div>
      <div style="font:700 10.5px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#6B7A9E;padding-bottom:12px;border-bottom:1px solid #1B2540;margin-bottom:6px">[ PRE-EVENT ]</div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">AUG 24, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Registration opens. Join the <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener">Discord</a>, start sketching your schema.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 04, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Judging panel announced.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 21, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Team formation. 1-4 people per team. Solo welcome.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 23, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Raptors Conference, online and free. Unrelated event, same community, worth your afternoon.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 24, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6"><samp style="color:#E6ECFF">spec.md</samp> published. Read it before the clock starts. No code yet.<br><a href="/spec" style="display:inline-block;margin-top:10px;color:#00E5D0;border-bottom:1px solid #00E5D0">Read the spec &gt;&gt;&gt;</a></p></div>
    </div>

    <div>
      <div style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;padding-bottom:12px;border-bottom:1px solid #00E5D0;margin-bottom:6px">[ HACKATHON · 72H ]</div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #FF3D6E;background:#121A32"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 25, 2026 @ 18:00 UTC</div><p style="margin:0;padding-right:14px;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#E6ECFF">Kickoff. <samp>fixtures.json</samp> and the acceptance suite released. Hacking begins.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #FF3D6E;background:#121A32"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 28, 2026 @ 18:00 UTC</div><p style="margin:0;padding-right:14px;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#E6ECFF">Code freeze. Submissions due. Acceptance reports verified.</p></div>

      <div style="font:700 10.5px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#6B7A9E;padding:34px 0 12px;border-bottom:1px solid #1B2540;margin-bottom:6px">[ POST-EVENT ]</div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">SEP 28 → OCT 08, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Judging window. Each project reviewed independently by multiple judges on structured forms across the window. Weighted scores and written feedback to every team.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">OCT 05, 2026 @ 18:00 UTC</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">The Write Up Quest closes.</p></div>
      <div data-reveal style="position:relative;padding:16px 0 16px 26px;border-left:1px solid #1B2540"><span style="position:absolute;left:-4px;top:22px;width:7px;height:7px;background:#FF3D6E"></span><div style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.16em;color:#FF3D6E;margin-bottom:8px">OCT 09, 2026</div><p style="margin:0;font:400 12.5px/1.7 'JetBrains Mono',monospace;color:#AEBAD6">Winners announced. Adoption decision announced with them.</p></div>
    </div>
  </div>
</section>

<section id="prizes" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">10</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 10 / PRIZES ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <h2 data-scramble style="margin:0 0 8px;font-family:'Archivo Black',sans-serif;font-size:clamp(2rem,7vw,6rem);line-height:.9;letter-spacing:-.045em;text-transform:uppercase;color:#E6ECFF">$2,500 total prize pool.</h2>
  <figure data-reveal style="margin:28px 0 0;border:1px solid #1B2540;background:#1B2540;display:flex;flex-wrap:wrap;gap:1px">
    <div class="pool-fig__chart" style="min-width:0;background:#0E1428;padding:22px;display:flex;justify-content:center;align-items:center">
      <svg viewBox="0 0 200 200" style="width:180px;height:180px;transform:rotate(-90deg)">
        <circle cx="100" cy="100" r="70" fill="none" stroke="#16203A" stroke-width="22"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#FF3D6E" stroke-width="22" stroke-dasharray="140.7 439.8" stroke-dashoffset="0"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#B32A50" stroke-width="22" stroke-dasharray="88.0 439.8" stroke-dashoffset="-140.7"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#00E5D0" stroke-width="22" stroke-dasharray="61.6 439.8" stroke-dashoffset="-228.7"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#00A38F" stroke-width="22" stroke-dasharray="35.2 439.8" stroke-dashoffset="-290.3"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#2A6E68" stroke-width="22" stroke-dasharray="26.4 439.8" stroke-dashoffset="-325.5"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#7B88AD" stroke-width="22" stroke-dasharray="17.6 439.8" stroke-dashoffset="-351.9"></circle>
        <circle cx="100" cy="100" r="70" fill="none" stroke="#4A5A80" stroke-width="22" stroke-dasharray="70.4 439.8" stroke-dashoffset="-369.5"></circle>
      </svg>
    </div>
    <div style="flex:3 1 320px;background:#0E1428;padding:22px;display:flex;flex-direction:column;justify-content:center;gap:11px;min-width:0">
      <div style="font-family:'Anton',sans-serif;font-size:13px;letter-spacing:.18em;color:#E6ECFF;margin-bottom:2px">FIG. 06 — POOL ALLOCATION / USD 2,500</div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#FF3D6E;flex:none"></span><span style="flex:1;min-width:0">1ST — GRAND PRIZE</span><span style="color:#E6ECFF">$800</span><span style="color:#3A4A70">32%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#B32A50;flex:none"></span><span style="flex:1;min-width:0">2ND — RUNNER-UP</span><span style="color:#E6ECFF">$500</span><span style="color:#3A4A70">20%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#00E5D0;flex:none"></span><span style="flex:1;min-width:0">3RD PLACE</span><span style="color:#E6ECFF">$350</span><span style="color:#3A4A70">14%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#00A38F;flex:none"></span><span style="flex:1;min-width:0">4TH PLACE</span><span style="color:#E6ECFF">$200</span><span style="color:#3A4A70">8%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#2A6E68;flex:none"></span><span style="flex:1;min-width:0">5TH PLACE</span><span style="color:#E6ECFF">$150</span><span style="color:#3A4A70">6%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#7B88AD;flex:none"></span><span style="flex:1;min-width:0">BEST JUDGING ENGINE</span><span style="color:#E6ECFF">$100</span><span style="color:#3A4A70">4%</span></div>
      <div style="display:flex;align-items:center;gap:10px;font:400 11px/1 'Space Mono',monospace;letter-spacing:.14em;color:#AEBAD6"><span style="width:11px;height:11px;background:#4A5A80;flex:none"></span><span style="flex:1;min-width:0">WRITE UP QUEST — $100 × 4</span><span style="color:#E6ECFF">$400</span><span style="color:#3A4A70">16%</span></div>
    </div>
  </figure>
  <div style="height:32px"></div>
  <div style="display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border:1px solid #FF3D6E">
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#FF3D6E" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:16px;top:20px;transform:rotate(-11deg)">
        <circle cx="32" cy="30" r="27" stroke="#00E5D0" stroke-width="1" stroke-dasharray="3 6"></circle>
        <path d="M18 9h28v10a14 14 0 0 1-28 0z"></path>
        <path d="M18 12h-7a7 7 0 0 0 7 7"></path>
        <path d="M46 12h7a7 7 0 0 1-7 7"></path>
        <path d="M32 33v7"></path>
        <path d="M25 40h14l3 8H22z"></path>
        <path d="M17 48h30v5H17z"></path>
        <path d="M25 17l5 5 8-9" stroke="#00E5D0"></path>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-01</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.8rem,5.6vw,4.6rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$800</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">1st Place</div>
        </div>
        <p style="margin:0;max-width:62ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Grand Prize, and the one we run.</strong> The portal that cleared the ladder honestly, enforced its own rules in the backend, started with one command, and read like software somebody intends to maintain. This is the project Hackathon Raptors forks and puts into production.</p>
      </div>
    </div>
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#B32A50" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:10px;top:30px;transform:rotate(13deg)">
        <path d="M15 4h7l11 22h-7z"></path>
        <path d="M49 4h-7L31 26h7z"></path>
        <circle cx="32" cy="42" r="18"></circle>
        <circle cx="32" cy="42" r="13" stroke="#00E5D0" stroke-width="1" stroke-dasharray="3 5"></circle>
        <text x="32" y="43" fill="#00E5D0" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="17" font-weight="700">2</text>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-02</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$500</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">2nd Place</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Runner-Up.</strong> Exceptional work across the board. Strong tier completion, defensible judging maths, documentation that respects the reader. Close enough that we will be reading it for ideas.</p>
      </div>
    </div>
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#00E5D0" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:22px;top:16px;transform:rotate(-7deg)">
        <path d="M2 58h60"></path>
        <path d="M6 34h18v24H6z"></path>
        <path d="M24 24h16v34H24z"></path>
        <path d="M40 42h18v16H40z" stroke="#00E5D0"></path>
        <path d="M32 5L34.3 10.8L40.6 11.2L35.7 15.2L37.3 21.3L32 17.9L26.7 21.3L28.3 15.2L23.4 11.2L29.7 10.8Z" stroke="#00E5D0" stroke-width="1.4"></path>
        <text x="15" y="46" fill="#6B7A9E" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="13" font-weight="700">2</text>
        <text x="32" y="41" fill="#6B7A9E" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="13" font-weight="700">1</text>
        <text x="49" y="50" fill="#00E5D0" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="13" font-weight="700">3</text>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-03</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$350</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">3rd Place</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Third Place.</strong> A standout, either for how far it climbed in 72 hours or for one decision nobody else made.</p>
      </div>
    </div>
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#00A38F" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:12px;top:26px;transform:rotate(16deg)">
        <path d="M22 36L14 60l18-8 18 8-8-24"></path>
        <circle cx="32" cy="23" r="17"></circle>
        <circle cx="32" cy="23" r="12" stroke="#00E5D0" stroke-width="1" stroke-dasharray="3 5"></circle>
        <text x="32" y="24" fill="#00E5D0" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="17" font-weight="700">4</text>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-04</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$200</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">4th Place</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Fourth Place.</strong> Finished the climb and left something behind worth reading. Solid tier completion, honest scope, no shortcuts hiding in the backend.</p>
      </div>
    </div>
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#2A6E68" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:20px;top:22px;transform:rotate(-19deg)">
        <path d="M32 3l23 8v18c0 15-9 24-23 29C18 53 9 44 9 29V11z"></path>
        <path d="M32 12l15 5v12c0 10-6 16-15 20-9-4-15-10-15-20V17z" stroke="#00E5D0" stroke-width="1" stroke-dasharray="4 5"></path>
        <text x="32" y="30" fill="#00E5D0" stroke="none" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="17" font-weight="700">5</text>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-05</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$150</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">5th Place</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Fifth Place.</strong> Made the top five out of everyone who started. Something in this build works better than it had any right to after 72 hours.</p>
      </div>
    </div>
    <div data-reveal class="prize-card" style="flex:1 1 calc(33.333% - 1px);min-width:250px;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#7B88AD" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:14px;top:30px;transform:rotate(9deg)">
        <circle cx="32" cy="10" r="3" stroke="#00E5D0"></circle>
        <path d="M32 13v37"></path>
        <path d="M8 20h48"></path>
        <path d="M14 20v4"></path>
        <path d="M50 20v4"></path>
        <path d="M4 24h20"></path>
        <path d="M4 24a10 10 0 0 0 20 0"></path>
        <path d="M40 24h20"></path>
        <path d="M40 24a10 10 0 0 0 20 0"></path>
        <path d="M24 50h16l4 8H20z"></path>
        <path d="M28 20l4-6 4 6z" stroke="#00E5D0" stroke-width="1.4"></path>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-06</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$100</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">Best Judging Engine</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">For the team whose judging layer was the most defensible.</strong> Assignment strategy, normalization method, role isolation, audit trail. The category prize for the problem the whole industry quietly avoids.</p>
      </div>
    </div>
    <div data-reveal class="prize-card prize-card--wide" style="flex:1 1 100%;min-width:0;background:#0B1020;padding:30px 26px">
      <svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke="#4A5A80" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" class="prize-art" style="right:38px;top:16px;transform:rotate(-10deg)">
        <path d="M10 3h26l16 16v42H10z"></path>
        <path d="M36 3v16h16"></path>
        <path d="M17 27h13M17 34h20M17 41h16M17 48h10"></path>
        <path d="M45 31l9 9-16 16-12 3 3-12z" fill="#0B1020" stroke="#00E5D0"></path>
        <path d="M42 34l9 9" stroke="#00E5D0" stroke-width="1.4"></path>
        <path d="M56 4l1.7 4.3L62 10l-4.3 1.7L56 16l-1.7-4.3L50 10l4.3-1.7z" stroke="#00E5D0" stroke-width="1.4"></path>
      </svg>
      <div style="position:relative;display:flex;flex-direction:column;gap:12px">
        <div class="prize-head" style="display:flex;flex-direction:column;gap:12px">
        <div style="font:400 17px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E">COMPARTMENT / P-07 · SIDE QUEST</div>
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2.4rem,5vw,4rem);line-height:.85;letter-spacing:-.05em;color:#FF3D6E">$400</div>
        <div style="font:400 17px/1 'Anton',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#E6ECFF">Write Up Quest</div>
        </div>
        <p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6"><strong style="color:#E6ECFF">Side quest. $100 x 4.</strong></p>
        <p style="margin:6px 0 0;max-width:72ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Building a platform in 72 hours is hard. Explaining what actually happened is rarer, and more useful to everyone else. So we are paying for it.</p>
        <dl style="margin:14px 0 0;display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border:1px solid #1B2540">
          <div style="background:#0B1020;padding:18px 20px;flex:2 1 300px;min-width:0"><dt style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:10px">What it is.</dt><dd style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Publish a write-up of your build. The schema you would redo. The normalization maths that fought you and won. The role-isolation bug you found at hour 60. The feature you cut and do not regret. The part where you realised the spec was harder than it looked.</dd></div>
          <div style="background:#0B1020;padding:18px 20px;flex:2 1 300px;min-width:0"><dt style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:10px">How they are judged.</dt><dd style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">On insight, not follower count. We are reading for technical substance: the debugging story, the benchmark that disappointed you, the design you abandoned and why. A 200-follower account writing something genuinely useful beats a viral thread that says nothing. Small accounts, this one is winnable.</dd></div>
          <div style="background:#0B1020;padding:18px 20px;flex:1 1 230px;min-width:0"><dt style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:10px">Where.</dt><dd style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">X, LinkedIn, Dev.to, your own blog, any developer-focused platform. Your call. Tag Hackathon Raptors.</dd></div>
          <div style="background:#0B1020;padding:18px 20px;flex:1 1 180px;min-width:0"><dt style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:10px">Prize.</dt><dd style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Top 4 write-ups, $100 each.</dd></div>
          <div style="background:#0B1020;padding:18px 20px;flex:1.4 1 260px;min-width:0"><dt style="font:500 11px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#FF3D6E;margin-bottom:10px">When.</dt><dd style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Write any time from kickoff. Submissions close October 5, 18:00 UTC. Winners announced October 9 with the main results.</dd></div>
        </dl>
        <p style="margin:12px 0 0;font:400 11.5px/1.8 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#4E5C7A">Optional. Does not affect your main score.</p>
      </div>
    </div>
  </div>

</section>

<section id="rules" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">11</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 11 / RULES ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:clamp(22px,3.5vw,52px);align-items:flex-start">
    <div style="flex:1 1 260px;max-width:340px;display:flex;flex-direction:column;gap:20px;position:sticky;top:118px;min-width:0">
      <h2 data-scramble style="margin:0;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Rules</h2>
      <p style="margin:0;font:400 12px/1.8 'IBM Plex Mono',monospace;color:#6B7A9E">What counts as a valid submission.</p>
      <div style="display:flex;flex-direction:column">
        <div style="font:400 15px/1 'VT323',monospace;letter-spacing:.18em;color:#00E5D0;padding-bottom:10px;border-bottom:1px solid #00E5D0">CHECKLIST · 09 ITEMS</div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">01</span><span>Open Source, OSI-Approved</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">02</span><span>One Command To Running</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">03</span><span>Clear T1 Or You Are Not Judged</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">04</span><span>New Code Only</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">05</span><span>No Hosted-Service Dependency</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">06</span><span>Claim Your Tiers Honestly</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">07</span><span>Team Size</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">08</span><span>Source Code Public</span></div>
        <div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid #16203A;font:400 11px/1.4 'Space Mono',monospace;letter-spacing:.1em;color:#6B7A9E"><span style="color:#FF3D6E">09</span><span>AI Tools Are Expected</span></div>
      </div>
      <p style="margin:0;padding:18px 20px;border:1px solid #FF3D6E;font:700 12.5px/1.75 'JetBrains Mono',monospace;color:#E6ECFF">If we cannot run it, we cannot adopt it. Every rule below is downstream of that one.</p>
    </div>
    <div data-reveal style="flex:999 1 420px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:1px;background:#1B2540;border:1px solid #1B2540;min-width:0">
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">01</span> Open Source, OSI-Approved</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">MIT or Apache-2.0 preferred. Public at submission. You keep ownership of your repository. We do not ask for an assignment, a transfer, or a CLA.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">02</span> One Command To Running</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6"><kbd style="font-family:'JetBrains Mono',monospace;color:#FF3D6E">docker compose up</kbd> brings up a working, seeded portal on a laptop. No cloud account, no hosted service, no external API. If we cannot run it, we cannot adopt it.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">03</span> Clear T1 Or You Are Not Judged</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">T1 is the floor. Auth, roles, event, submission, gallery. A project that does not reach it is not scored, however good the parts are.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">04</span> New Code Only</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">All project code written during the 72-hour window. Frameworks, libraries, boilerplate generators and AI assistance are all fair game. A pre-existing project of yours, or an existing open-source platform with the name changed, is not.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">05</span> No Hosted-Service Dependency</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">It runs offline on a laptop. This is not an aesthetic preference, it is the condition for the winner being adoptable at all.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">06</span> Claim Your Tiers Honestly</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">Declare the tiers you reached in <samp style="color:#FF3D6E">.dogfood.toml</samp>. The acceptance report is the receipt. Overclaiming costs more than the tier was worth.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">07</span> Team Size</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">1-4 people. Solo entries welcome, though this brief rewards a pair. Find teammates on the <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener">Hackathon Raptors Discord</a> before or during the event.</p></div>
      <div style="background:#0E1428;padding:20px"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">08</span> Source Code Public</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">GitHub repository, public at submission. Anonymous-username submissions accepted, but the team must be reachable for written follow-up by judges during the evaluation window.</p></div>
      <div style="background:#0E1428;padding:20px;grid-column:1 / -1"><div style="font:400 16px/1.1 'Anton',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#E6ECFF;margin-bottom:10px"><span style="color:#FF3D6E">09</span> AI Tools Are Expected</div><p style="margin:0;font:400 12.5px/1.75 'JetBrains Mono',monospace;color:#AEBAD6">Claude Code, Cursor, Aider, Copilot, local models, bring whatever you have. We do not gatekeep on whether you used AI. We gatekeep on whether the thing holds up and whether somebody on the team can defend the schema in writing. The acceptance report, <samp style="color:#FF3D6E">ARCHITECTURE.md</samp> and <samp style="color:#FF3D6E">JUDGING.md</samp> are the receipts.</p></div>
    </div>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">12</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 12 / WHO THIS IS FOR ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <h2 data-scramble style="margin:0 0 16px;max-width:24ch;font-family:'Archivo Black',sans-serif;font-size:clamp(1.7rem,4.4vw,3.4rem);line-height:.98;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">If you have ever filled in a hackathon submission form and thought "I could build this, and better", here is your invitation to prove it.</h2>
  <div style="height:36px"></div>
  <div style="display:flex;flex-wrap:wrap;gap:1px;background:#1B2540;border:1px solid #1B2540">
    <div data-reveal style="flex:2 1 340px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Full-Stack Builders</div><p style="margin:0;max-width:62ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">This is a whole product in a weekend: auth, roles, forms, gallery, dashboards, exports. If you like shipping the entire thing yourself, the tier ladder is built for you.</p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T1 → T2</div></div>
    <div data-reveal style="flex:1 1 270px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Backend &amp; API Engineers</div><p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">The interesting problems are all yours: role isolation that survives a curl, assignment algorithms, an export path that does not lose data, an API nobody else in this category bothered to build.</p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T2 → T4</div></div>
    <div data-reveal style="flex:1 1 270px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Frontend &amp; Design-System People</div><p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">The judge console and the public gallery are the product. Thirty projects to score in five hours is a UX problem before it is anything else.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> Make that not miserable and you have done something the incumbents have not.</p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T1 → T3</div></div>
    <div data-reveal style="flex:1 1 270px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Data &amp; Algorithms People</div><p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Cross-judge normalization and pairwise ranking are the genuinely hard parts, and the two Hard bonuses live here. Bradley-Terry, Crowd-BT, or something better you can defend.<sup style="color:#FF3D6E"><a href="#ref-12" aria-label="Jump to reference 12">[12]</a></sup></p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T2 + bonuses</div></div>
    <div data-reveal style="flex:1 1 270px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">Security Engineers</div><p style="margin:0;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">Role isolation, vote abuse, sybil resistance, audit trails. Every platform in this space treats community voting as a known-gameable feature they mitigate with policy rather than engineering.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> Do better.</p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T2 → T3 + Threat Model</div></div>
    <div data-reveal style="flex:2 1 340px;min-width:0;background:#0B1020;padding:26px 22px;display:flex;flex-direction:column;gap:12px"><div style="font:800 16px/1.15 'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E6ECFF">DevOps &amp; Self-Hosting Folks</div><p style="margin:0;max-width:62ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#AEBAD6">"One command to running" is not a nice-to-have here, it is 20% of the score and the reason the winner gets adopted. If you have opinions about how software should ship, this brief is downstream of all of them.</p><div style="font:400 15px/1 'Anton',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FF3D6E">Start at: T1 → adoptability</div></div>
  </div>
</section>

<section id="judges" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">13</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 13 / JUDGES ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(22px,3.5vw,52px);align-items:start;margin-bottom:clamp(26px,4vw,44px)">
    <div style="display:flex;flex-direction:column;gap:20px">
      <h2 data-scramble style="margin:0;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Judges</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,120px),1fr));gap:1px;background:#1B2540;border:1px solid #1B2540">
        <div style="background:#0E1428;padding:16px 14px;display:flex;flex-direction:column;gap:7px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">3</span><span style="font:400 15px/1.3 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">REVIEWS PER PROJECT</span></div>
        <div style="background:#0E1428;padding:16px 14px;display:flex;flex-direction:column;gap:7px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">36</span><span style="font:400 15px/1.3 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">PANEL SEATS</span></div>
        <div style="background:#0E1428;padding:16px 14px;display:flex;flex-direction:column;gap:7px"><span style="font-family:'Archivo Black',sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);line-height:1;letter-spacing:-.04em;color:#FF3D6E">11d</span><span style="font:400 15px/1.3 'VT323',monospace;letter-spacing:.14em;color:#6B7A9E">EVALUATION WINDOW</span></div>
      </div>
      <p style="margin:0;padding:16px 18px;border:1px dashed #FF3D6E;font:400 12.5px/1.85 'IBM Plex Mono',monospace;color:#6B7A9E"><em>The panel is seated and assignments are issued. Reach out at <a href="mailto:hello@raptors.dev">hello@raptors.dev</a> to nominate someone for a future event, or to be nominated.</em></p>
    </div>
    <div style="display:flex;flex-direction:column;gap:20px">
      <p style="margin:0;font-family:'DM Serif Display',serif;font-weight:400;font-size:clamp(1.15rem,2vw,1.65rem);line-height:1.3;letter-spacing:-.01em;color:#E6ECFF;text-wrap:pretty">Senior engineers, architects and technical leaders who have built and operated evaluation systems, run production software at scale, and sat on the other side of a judging form knowing it could have been better.</p>
      <div style="display:flex;flex-direction:column;gap:1px;background:#1B2540;border:1px solid #1B2540">
        <div style="background:#0E1428;padding:14px 16px;display:flex;gap:12px;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#00E5D0">&rarr;</span><span>Every project is reviewed independently, on structured forms, across the window.</span></div>
        <div style="background:#0E1428;padding:14px 16px;display:flex;gap:12px;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#00E5D0">&rarr;</span><span>Judges never see one another's ballots. The platform you build has to hold that line too.</span></div>
        <div style="background:#0E1428;padding:14px 16px;display:flex;gap:12px;font:400 12px/1.7 'JetBrains Mono',monospace;color:#AEBAD6"><span style="color:#00E5D0">&rarr;</span><span>Weighted scores and written feedback go to every team, placed or not.</span></div>
      </div>
    </div>
  </div>

  <div data-reveal style="border:1px solid #1B2540">
    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 16px;border-bottom:1px solid #1B2540;background:#0B1020;font:400 15px/1 'VT323',monospace;letter-spacing:.16em;color:#6B7A9E"><span>PANEL &middot; 36 &middot; SEATED</span><span style="color:#00E5D0">EVALUATION 29.09 &ndash; 08.10.2026</span></div>
    <div style="padding:20px 16px;background:#0E1428">
  <ul class="df-jgrid">
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/anuj-kapoor.jpg" alt="Anuj Kapoor" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Anuj Kapoor</h3>
        <div class="df-jcard__meta">Microsoft · United States</div>
        <p class="df-jcard__bio">Senior Software Engineer at Microsoft and an IEEE Senior Member, with 16 years building AI and cloud platforms at Microsoft, Amazon and Priceline. Agentic AI, multi-agent systems, enterprise automation and distributed systems, plus published research behind products serving millions of users.</p>
        <a class="df-li" href="https://www.linkedin.com/in/anuj-kapoor-38b6a899/" target="_blank" rel="noopener noreferrer" aria-label="Anuj Kapoor on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/smit-nitinkumar-shah.jpg" alt="Smit Nitinkumar Shah" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Smit Nitinkumar Shah</h3>
        <div class="df-jcard__meta">Microsoft · United States</div>
        <p class="df-jcard__bio">Senior Software Engineer at Microsoft working on large-scale cloud platforms, distributed systems, Kubernetes and confidential computing. He has led platform work across Azure security, compliance, reliability and workflow orchestration, and has judged and mentored at hackathons before this one.</p>
        <a class="df-li" href="https://www.linkedin.com/in/smit-shah-a7060b1a" target="_blank" rel="noopener noreferrer" aria-label="Smit Nitinkumar Shah on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/rupesh-kumar-prasad.jpg" alt="Rupesh Kumar Prasad" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Rupesh Kumar Prasad</h3>
        <div class="df-jcard__meta">Analog Devices · United States</div>
        <p class="df-jcard__bio">Principal architect with 18 years designing secure, scalable enterprise platforms across Azure, AWS and the Microsoft stack. Cloud architecture, identity and security, APIs, DevOps and data platforms, with an IEEE Senior Member&#x27;s habit of reading a design for what breaks under load rather than what demos well.</p>
        <a class="df-li" href="https://www.linkedin.com/in/rupeshprasad/" target="_blank" rel="noopener noreferrer" aria-label="Rupesh Kumar Prasad on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/narasimha-reddy-annapareddy.jpg" alt="Narasimha Reddy Annapareddy" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Narasimha Reddy Annapareddy</h3>
        <div class="df-jcard__meta">ChargePoint, Inc. · USA</div>
        <p class="df-jcard__bio">Software Engineering Manager for NetSuite Business Systems at ChargePoint, with 14 years in enterprise software and engineering leadership. His work is integrations across finance and supply chain operations, which is where data models either hold or quietly lose records.</p>
        <a class="df-li" href="https://linkedin.com/in/narasimha-annapareddy" target="_blank" rel="noopener noreferrer" aria-label="Narasimha Reddy Annapareddy on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/hari-krishna-bethanaboina.jpg" alt="Hari Krishna Bethanaboina" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Hari Krishna Bethanaboina</h3>
        <div class="df-jcard__meta">Martin Marietta Materials · USA</div>
        <p class="df-jcard__bio">Lead Solutions Architect at Martin Marietta Materials, where he runs enterprise transformation programmes across ERP modernization, AI-driven asset maintenance and cloud migration. Twenty three years of delivery across the US, Europe, the Middle East, Asia and Africa, on systems governing $8B in assets across 400 sites. IEEE Senior Member, Oracle ACE Associate, and a peer reviewer for IEEE, Elsevier and Springer Nature.</p>
        <a class="df-li" href="https://www.linkedin.com/in/haribethanaboina" target="_blank" rel="noopener noreferrer" aria-label="Hari Krishna Bethanaboina on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/igor-malovytsia.jpg" alt="Igor Malovytsia" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Igor Malovytsia</h3>
        <div class="df-jcard__meta">GuardSpine · United States</div>
        <p class="df-jcard__bio">CTO at GuardSpine, co-founder and mentor at the Ukrainian Rust Community, currently researching AI governance. Deep Rust background, which shows up in how he reads ownership of state and error paths in someone else&#x27;s codebase.</p>
        <a class="df-li" href="https://www.linkedin.com/in/igor-malovitsa/" target="_blank" rel="noopener noreferrer" aria-label="Igor Malovytsia on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/rushikesh-hayatnagarkar.jpg" alt="Rushikesh Hayatnagarkar" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Rushikesh Hayatnagarkar</h3>
        <div class="df-jcard__meta">United States</div>
        <p class="df-jcard__bio">Senior Product Manager and hands-on AI builder working on technical infrastructure, autonomous multi-agent systems and large-scale platforms. He scores architectural depth and code integrity alongside whether the thing survives contact with real operations, and writes feedback aimed at what a team should do after the hackathon.</p>
        <a class="df-li" href="https://www.linkedin.com/in/rushikeshhayatnagarkar/" target="_blank" rel="noopener noreferrer" aria-label="Rushikesh Hayatnagarkar on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/konstantin-mishukov.jpg" alt="Konstantin Mishukov" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Konstantin Mishukov</h3>
        <div class="df-jcard__meta">United States</div>
        <p class="df-jcard__bio">Lead iOS Engineer with more than ten years on production mobile systems. At Yandex Market he owned iOS work across search, backend-driven UI and payments serving millions of customers, and at Sberbank he was a key engineer on an award-winning business intelligence platform. Mobile architecture, code quality and data visualization, judged for production readiness.</p>
        <a class="df-li" href="https://www.linkedin.com/in/kmishukov/" target="_blank" rel="noopener noreferrer" aria-label="Konstantin Mishukov on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
    <li class="df-jcard">
      <div class="df-jcard__media"><img class="df-jphoto" src="img/judges/nail-iarmukhametov.jpg" alt="Nail Iarmukhametov" width="480" height="480" loading="lazy" decoding="async"></div>
      <div class="df-jcard__body">
        <h3 class="df-jcard__name">Nail Iarmukhametov</h3>
        <div class="df-jcard__meta">Bulgaria</div>
        <p class="df-jcard__bio">Cloud Infrastructure and DevOps Lead with ten years operating production systems on Kubernetes, AWS and Azure. Infrastructure as code, CI/CD, cloud security and reliability, which is the exact ground the one command to running requirement stands on.</p>
        <a class="df-li" href="https://www.linkedin.com/in/restaq" target="_blank" rel="noopener noreferrer" aria-label="Nail Iarmukhametov on LinkedIn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg><span>LinkedIn</span></a>
      </div>
    </li>
  </ul>
  <div class="df-panel-label"><span>// the rest of the panel</span></div>
  <div class="df-marquee df-marquee--auto" aria-label="Full judging panel">
    <div class="df-marquee__track">
      <a class="df-chip" href="https://www.linkedin.com/in/sourav-s-36a7a225" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/sourav-sinha.jpg" alt="Sourav Sinha" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Sourav Sinha</span><span class="df-chip__company">Amazon Web Services · United States Of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/nsidiropulo" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/nikolai-sidiropulo.jpg" alt="Nikolai Sidiropulo" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Nikolai Sidiropulo</span><span class="df-chip__company">Meta · United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/ayacaste/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/anton-musatov.jpg" alt="Anton Musatov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Anton Musatov</span><span class="df-chip__company">Digitail Inc. · Spain</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/arunkumarspk" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/arun-kumar-kaliamoorthy.jpg" alt="Arun Kumar Kaliamoorthy" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Arun Kumar Kaliamoorthy</span><span class="df-chip__company">GoDaddy · United States Of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/dife/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/dmitriy-fedoryshchev.jpg" alt="Dmitriy Fedoryshchev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitriy Fedoryshchev</span><span class="df-chip__company">EverCommerce · United Kingdom</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/sw1tch3roo/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/dmitry-gusev.jpg" alt="Dmitry Gusev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitry Gusev</span><span class="df-chip__company">Avito · Georgia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/dmitry-kuznetsov-685b72194/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/dmitry-kuznetsov.jpg" alt="Dmitry Kuznetsov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitry Kuznetsov</span><span class="df-chip__company">FunnelFox · Serbia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/gautam-siddhartha/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/gautam-siddhartha.jpg" alt="Gautam Siddhartha" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Gautam Siddhartha</span><span class="df-chip__company">Walmart · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/ivan-antropov-9505a969/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/ivan-antropov.jpg" alt="Ivan Antropov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Ivan Antropov</span><span class="df-chip__company">T-Bank · Russia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/igalarzab/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/jose-galarza.jpg" alt="Jose Galarza" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Jose Galarza</span><span class="df-chip__company">Wise · Singapore</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/kadharmoideen-fadurudeen-b50216174" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/kadharmoideen-fadurudeen.jpg" alt="Kadharmoideen Fadurudeen" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Kadharmoideen Fadurudeen</span><span class="df-chip__company">Adobe Inc · United States of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/niko-dolgo/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/nikolay-dolgov.jpg" alt="Nikolay Dolgov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Nikolay Dolgov</span><span class="df-chip__company">The Lightning Group · UK</span></a>
      <a class="df-chip" href="https://linkedin.com/in/pavani-totli-kuruba" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/pavani-totli-kuruba.jpg" alt="Pavani Totli Kuruba" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pavani Totli Kuruba</span><span class="df-chip__company">Lululemon · United States</span></a>
      <a class="df-chip" href="http://lnkd.in/bC3Wsz9" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/shon-thomas.jpg" alt="Shon Thomas" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shon Thomas</span><span class="df-chip__company">Yahoo · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/shriniwas-phalke-2978b147/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/shriniwas-phalke.jpg" alt="Shriniwas Phalke" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shriniwas Phalke</span><span class="df-chip__company">Walmart Global tech · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/soumyajit-mukherjee-97a56070/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/soumyajit-mukherjee.jpg" alt="Soumyajit Mukherjee" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Soumyajit Mukherjee</span><span class="df-chip__company">Shutterfly Inc · United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/krus210/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/stanislav-korolev.jpg" alt="Stanislav Korolev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Stanislav Korolev</span><span class="df-chip__company">Avito · Russia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/t-kubiak/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/tomasz-kubiak.jpg" alt="Tomasz Kubiak" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Tomasz Kubiak</span><span class="df-chip__company">Welltech · Poland</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/kursadalsan/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/kursad-alsan.jpg" alt="Kursad Alsan" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Kursad Alsan</span><span class="df-chip__company">Thailand</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/manish-gupta-9a871a10/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/manish-gupta.jpg" alt="Manish Gupta" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Manish Gupta</span><span class="df-chip__company">USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/manpreet-aneja-2a446b60/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/manpreet-kaur.jpg" alt="Manpreet Kaur" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Manpreet Kaur</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/pramodini-mahendrakar-88799515/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BGqoEp%2BIfTBm2sPCRsH6a9A%3D%3D" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/pramodini-girish-mahendrakar.jpg" alt="Pramodini Girish Mahendrakar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pramodini Girish Mahendrakar</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/pritesh-gehlot-7999b428" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/pritesh-gehlot.jpg" alt="Pritesh Gehlot" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pritesh Gehlot</span><span class="df-chip__company">UNITED STATES</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/sree4all/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/rajasree-pachuveetil.jpg" alt="Rajasree Pachuveetil" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Rajasree Pachuveetil</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/reeshavkumar" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/reeshav-kumar.jpg" alt="Reeshav Kumar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Reeshav Kumar</span><span class="df-chip__company">USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/shashankshekhar32" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/shashank-shekhar.jpg" alt="Shashank Shekhar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shashank Shekhar</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/priyasonali/" target="_blank" rel="noopener noreferrer"><img class="df-chip__photo" src="img/judges/sonali-priya.jpg" alt="Sonali Priya" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Sonali Priya</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/sourav-s-36a7a225" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/sourav-sinha.jpg" alt="Sourav Sinha" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Sourav Sinha</span><span class="df-chip__company">Amazon Web Services · United States Of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/nsidiropulo" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/nikolai-sidiropulo.jpg" alt="Nikolai Sidiropulo" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Nikolai Sidiropulo</span><span class="df-chip__company">Meta · United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/ayacaste/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/anton-musatov.jpg" alt="Anton Musatov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Anton Musatov</span><span class="df-chip__company">Digitail Inc. · Spain</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/arunkumarspk" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/arun-kumar-kaliamoorthy.jpg" alt="Arun Kumar Kaliamoorthy" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Arun Kumar Kaliamoorthy</span><span class="df-chip__company">GoDaddy · United States Of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/dife/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/dmitriy-fedoryshchev.jpg" alt="Dmitriy Fedoryshchev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitriy Fedoryshchev</span><span class="df-chip__company">EverCommerce · United Kingdom</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/sw1tch3roo/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/dmitry-gusev.jpg" alt="Dmitry Gusev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitry Gusev</span><span class="df-chip__company">Avito · Georgia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/dmitry-kuznetsov-685b72194/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/dmitry-kuznetsov.jpg" alt="Dmitry Kuznetsov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Dmitry Kuznetsov</span><span class="df-chip__company">FunnelFox · Serbia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/gautam-siddhartha/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/gautam-siddhartha.jpg" alt="Gautam Siddhartha" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Gautam Siddhartha</span><span class="df-chip__company">Walmart · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/ivan-antropov-9505a969/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/ivan-antropov.jpg" alt="Ivan Antropov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Ivan Antropov</span><span class="df-chip__company">T-Bank · Russia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/igalarzab/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/jose-galarza.jpg" alt="Jose Galarza" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Jose Galarza</span><span class="df-chip__company">Wise · Singapore</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/kadharmoideen-fadurudeen-b50216174" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/kadharmoideen-fadurudeen.jpg" alt="Kadharmoideen Fadurudeen" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Kadharmoideen Fadurudeen</span><span class="df-chip__company">Adobe Inc · United States of America</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/niko-dolgo/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/nikolay-dolgov.jpg" alt="Nikolay Dolgov" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Nikolay Dolgov</span><span class="df-chip__company">The Lightning Group · UK</span></a>
      <a class="df-chip" href="https://linkedin.com/in/pavani-totli-kuruba" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/pavani-totli-kuruba.jpg" alt="Pavani Totli Kuruba" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pavani Totli Kuruba</span><span class="df-chip__company">Lululemon · United States</span></a>
      <a class="df-chip" href="http://lnkd.in/bC3Wsz9" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/shon-thomas.jpg" alt="Shon Thomas" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shon Thomas</span><span class="df-chip__company">Yahoo · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/shriniwas-phalke-2978b147/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/shriniwas-phalke.jpg" alt="Shriniwas Phalke" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shriniwas Phalke</span><span class="df-chip__company">Walmart Global tech · USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/soumyajit-mukherjee-97a56070/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/soumyajit-mukherjee.jpg" alt="Soumyajit Mukherjee" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Soumyajit Mukherjee</span><span class="df-chip__company">Shutterfly Inc · United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/krus210/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/stanislav-korolev.jpg" alt="Stanislav Korolev" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Stanislav Korolev</span><span class="df-chip__company">Avito · Russia</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/t-kubiak/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/tomasz-kubiak.jpg" alt="Tomasz Kubiak" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Tomasz Kubiak</span><span class="df-chip__company">Welltech · Poland</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/kursadalsan/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/kursad-alsan.jpg" alt="Kursad Alsan" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Kursad Alsan</span><span class="df-chip__company">Thailand</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/manish-gupta-9a871a10/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/manish-gupta.jpg" alt="Manish Gupta" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Manish Gupta</span><span class="df-chip__company">USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/manpreet-aneja-2a446b60/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/manpreet-kaur.jpg" alt="Manpreet Kaur" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Manpreet Kaur</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/pramodini-mahendrakar-88799515/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BGqoEp%2BIfTBm2sPCRsH6a9A%3D%3D" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/pramodini-girish-mahendrakar.jpg" alt="Pramodini Girish Mahendrakar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pramodini Girish Mahendrakar</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/pritesh-gehlot-7999b428" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/pritesh-gehlot.jpg" alt="Pritesh Gehlot" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Pritesh Gehlot</span><span class="df-chip__company">UNITED STATES</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/sree4all/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/rajasree-pachuveetil.jpg" alt="Rajasree Pachuveetil" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Rajasree Pachuveetil</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/reeshavkumar" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/reeshav-kumar.jpg" alt="Reeshav Kumar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Reeshav Kumar</span><span class="df-chip__company">USA</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/shashankshekhar32" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/shashank-shekhar.jpg" alt="Shashank Shekhar" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Shashank Shekhar</span><span class="df-chip__company">United States</span></a>
      <a class="df-chip" href="https://www.linkedin.com/in/priyasonali/" target="_blank" rel="noopener noreferrer" aria-hidden="true" tabindex="-1"><img class="df-chip__photo" src="img/judges/sonali-priya.jpg" alt="Sonali Priya" width="240" height="240" loading="lazy" decoding="async"><span class="df-chip__name">Sonali Priya</span><span class="df-chip__company">United States</span></a>
    </div>
  </div>
    </div>
  </div>
</section>

<section id="faq" style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px)">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">14</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 14 / FAQ ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <h2 data-scramble style="margin:0 0 36px;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">FAQ</h2>
  <div style="border:1px solid #1B2540">
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What's the team size limit?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">1-4 people. Solo welcome. For this brief we would recommend 2-3, since the tier ladder splits cleanly across a frontend and a backend.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Can I use AI code generation?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Yes, and you should. Claude Code, Cursor, Aider, Copilot, all expected. We do not score whether you used AI. We score whether the portal runs, whether role isolation survives a curl, and whether somebody can explain the schema. The acceptance report and your docs are the receipts.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Can I use a framework, an ORM, a boilerplate generator?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Yes. All of it. Rails, Django, Laravel, Next.js, Phoenix, whatever gets you to a working product fastest. The constraint here is one-command self-hosting, not dependency count. That was a different hackathon.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What if I only reach T2?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Then you are scored on T2 and you can absolutely still win. Tier Completion is 40% and correctness beats breadth inside it. A clean, correct, well-documented T2 has beaten a broken T4 every time we have modelled this.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Does design count?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Yes, inside Code Quality and inside Adoptability. A judge console that makes 30 reviews bearable is a real contribution. But a beautiful frontend over hardcoded data scores zero on Tier Completion, which is 40%.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What exactly is in the fixture data?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">A synthetic dataset built to the shape of a real Raptors event: roughly 40 projects, 30 judges, 8 tracks, and a full set of scores. No real names, no real submissions. It is deliberately built with the edge cases every evaluation system has to survive, including a reviewer who rates everything the same, an incomplete batch, and a duplicate entry. If your portal only works on tidy input, you will find out on Friday rather than on Monday.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What is the acceptance suite?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">A test suite we publish at kickoff that runs against your running portal and reports pass or fail per tier requirement. You run it yourself, as often as you like, and commit the output. Judges run the same suite. Nobody is guessing.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Can I start coding before September 25?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">No project code. Planning, sketching schemas, reading the spec, choosing your stack, tuning prompts, all fine and encouraged. Any project code committed before kickoff disqualifies the submission.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Do I have to use Docker specifically?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6"><kbd style="font-family:'JetBrains Mono',monospace;color:#FF3D6E">docker compose up</kbd> is the default and the safest choice. If your stack has a genuinely equivalent single command that needs nothing but a laptop, use it and say so clearly in your README. The test is whether a stranger gets a running portal from one command, not which tool printed the logs.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What license do I have to use?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Any OSI-approved license. MIT or Apache-2.0 preferred, because those are the ones we can adopt without a legal conversation. Copyleft is allowed and will not cost you points.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What does Raptors actually do with the winner?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Fork it, self-host it, and run our events on it. Credit your team on every event page it powers. Send our changes back to you as pull requests. See What happens to the winner for the full statement.</p></details>
    <details style="border-bottom:1px solid #1B2540"><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>Do I keep ownership?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Yes, entirely. No assignment, no transfer, no CLA, nothing to sign. You are licensing your work to the world under an open license, and we are one of the people using it.</p></details>
    <details><summary style="display:flex;justify-content:space-between;gap:16px;padding:18px 20px;font:600 15px/1.4 'Syne',sans-serif;letter-spacing:-.005em;color:#E6ECFF;transition:background .12s linear" style-hover="background:#131C36"><span>What if two entries are both worth adopting?</span><span style="color:#FF3D6E">&gt;&gt;&gt;</span></summary><p style="margin:0;padding:0 20px 20px;max-width:80ch;font:400 12.5px/1.85 'JetBrains Mono',monospace;color:#AEBAD6">Then we will say so publicly, adopt one, and credit both, describing exactly what we took from where. We will not quietly merge someone's architecture without naming them.</p></details>
  </div>
</section>

<section style="border-top:1px solid #00E5D0;padding:clamp(56px,8vw,110px) clamp(12px,2vw,24px);background:#0E1428">
  <div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">
    <span data-ghost style="user-select:none;-webkit-user-select:none;font-family:'Archivo Black',sans-serif;font-size:clamp(2.2rem,5.4vw,4.6rem);line-height:.72;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px #26355C;flex:none;will-change:transform">15</span>
    <span style="font:400 17px/1 'Bebas Neue',sans-serif;letter-spacing:.22em;color:#00E5D0">[ 15 / WHY NOW ]</span>
    <span data-rule style="flex:1;height:1px;background:#00E5D0;transform-origin:left;display:block"></span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(24px,4vw,64px);align-items:start">
    <div>
      <h2 data-scramble style="margin:0 0 28px;font-family:'Archivo Black',sans-serif;font-size:clamp(1.9rem,5vw,4rem);line-height:.94;letter-spacing:-.04em;text-transform:uppercase;color:#E6ECFF">Why Now</h2>
      <p style="margin:0 0 26px;font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:clamp(1.2rem,2.2vw,1.9rem);line-height:1.35;letter-spacing:-.01em;color:#E6ECFF;text-wrap:pretty">Every hackathon platform in the world converged on the same nine features, and then stopped moving.</p>
      <p style="margin:0 0 20px;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">The category leader still cannot weight judging criteria and tells organizers to use a spreadsheet instead.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> Score normalization, the one genuinely hard statistical problem in the whole domain, is advertised as a feature by multiple platforms and documented by none of them.<sup style="color:#FF3D6E"><a href="#ref-6" aria-label="Jump to reference 6">[6]</a><a href="#ref-7" aria-label="Jump to reference 7">[7]</a></sup> Community voting is treated as an unsolvable abuse surface to be managed with small prizes and hidden results rather than fixed with engineering.<sup style="color:#FF3D6E"><a href="#ref-1" aria-label="Jump to reference 1">[1]</a></sup> Pricing is sales-gated across the board, so a volunteer organizer running a free event cannot even find out what it costs. And after fifteen years and millions of developers, not one of them ships a public API, leaving an entire industry to integrate through screen scrapers and downloaded spreadsheets.<sup style="color:#FF3D6E"><a href="#ref-14" aria-label="Jump to reference 14">[14]</a></sup></p>
      <p style="margin:0 0 20px;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">The open-source alternatives are better than their reputation. Gavel brought a real idea from mathematical psychology into judging and has been quietly producing fairer rankings at HackMIT for years.<sup style="color:#FF3D6E"><a href="#ref-12" aria-label="Jump to reference 12">[12]</a></sup> JunctionApp, Dribdat, Quill and Hibiscus are all real and all self-hostable.<sup style="color:#FF3D6E"><a href="#ref-13" aria-label="Jump to reference 13">[13]</a></sup> What is missing is a modern one, assembled as a whole, that a working organizer can deploy without becoming its maintainer.</p>
      <p style="margin:0 0 20px;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">We are not writing this as analysts. We are writing it as operators, from thirty-five events of knowing precisely which stage of the pipeline the tooling abandons you at.</p>
      <p style="margin:0;font:400 13px/1.85 'JetBrains Mono',monospace;color:#AEBAD6;text-wrap:pretty">Generating a CRUD app is trivial now. Building an evaluation system that is fair, that enforces its own rules, that an organizer can actually operate, and that you can hand to someone else without a handover call, is the part that still takes engineers.</p>
    </div>
    <div data-reveal style="display:flex;flex-direction:column;gap:22px">
      <p style="margin:0;padding:26px 24px;border:1px solid #FF3D6E;font:700 14px/1.8 'JetBrains Mono',monospace;color:#E6ECFF">That is the hackathon. 72 hours. One product. We run the winner.</p>
      <blockquote data-dither style="margin:0;padding:34px 26px;background:#FF3D6E;position:relative;overflow:hidden">
        <span style="position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle at center,rgba(10,10,10,.85) 1px,transparent 1.5px);background-size:4px 4px;opacity:.55"></span>
        <p style="margin:0;position:relative;font-family:'Playfair Display',serif;font-weight:700;font-size:clamp(1.6rem,3.6vw,3.1rem);line-height:1.02;letter-spacing:-.02em;color:#0B1020;animation:glitch 5.5s steps(1) 1.5s infinite">Build the platform that will judge you.</p>
      </blockquote>
      <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener" data-magnet="1" style="display:inline-flex;align-items:center;justify-content:space-between;gap:12px;background:#0B1020;color:#FF3D6E;border:1px solid #FF3D6E;font:700 12px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;padding:20px 22px;transition:background .12s linear,color .12s linear,transform .08s linear" style-hover="background:#FF3D6E;color:#0B1020" style-active="transform:translateY(1px) scale(.98)">[ Go to Discord ] <span>&gt;&gt;&gt;</span></a>
    </div>
  </div>
</section>

<section style="border-top:1px solid #1B2540;padding:clamp(40px,5vw,72px) clamp(12px,2vw,24px)">
  <div style="font:700 10.5px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#4A5A80;margin-bottom:22px">[ REFERENCES ]</div>
  <ol style="margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:10px 40px;font:400 11.5px/1.85 'Courier Prime',monospace;color:#55658C;counter-reset:none">
    <li id="ref-1"><a href="https://help.devpost.com/article/64-judging-public-voting" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[1]</span> Devpost, "Judging &amp; public voting" (equally-weighted criteria only, offline judging required for weights; ~5 hours to score 30 projects; public-vote fraud guidance). help.devpost.com</a></li>
    <li id="ref-2"><a href="https://info.devpost.com/blog/key-hackathon-platform-features" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[2]</span> Devpost, "7 key features to consider when choosing your hackathon platform provider". info.devpost.com</a></li>
    <li id="ref-3"><a href="https://info.devpost.com/blog/devpost-for-teams-releases-q1-2025" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[3]</span> Devpost for Teams, "New voting, guest access, and setup features". info.devpost.com</a></li>
    <li id="ref-4"><a href="https://help.devpost.com/article/126-know-your-submission-steps" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[4]</span> Devpost, "Know your submission steps" (the full submission field set). help.devpost.com</a></li>
    <li id="ref-5"><a href="https://guide.mlh.com/general-information/judging-and-submissions/hackathon-submission-portal/using-devpost" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[5]</span> MLH Organizer Guide, "Using Devpost". guide.mlh.com</a></li>
    <li id="ref-6"><a href="https://devfolio.co/blog/devfolios-stack-of-features/" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[6]</span> Devfolio, "Devfolio's stack of features". devfolio.co</a></li>
    <li id="ref-7"><a href="https://guide.devfolio.co/docs/guide/organizer-judging" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[7]</span> Devfolio, "Organizer judging". guide.devfolio.co</a></li>
    <li id="ref-8"><a href="https://guide.devfolio.co/docs/guide/judging" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[8]</span> Devfolio, "Judging" (the fixed five-criterion rubric). guide.devfolio.co</a></li>
    <li id="ref-9"><a href="https://dorahacks.io/" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[9]</span> DoraHacks (700+ hackathons, 32,000+ projects, BUIDL AI automated review and AI judging). dorahacks.io</a></li>
    <li id="ref-10"><a href="https://dorahacks.io/blog/news/qf-retrospective/" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[10]</span> DoraHacks, "Building effective on-chain governance mechanisms". dorahacks.io</a></li>
    <li id="ref-11"><a href="https://www.hackerearth.com/blog/hackathon-platforms" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[11]</span> HackerEarth, "11 best hackathon platforms for enterprise in 2026". hackerearth.com</a></li>
    <li id="ref-12"><a href="https://github.com/anishathalye/gavel" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[12]</span> Gavel, HackMIT's pairwise-comparison judging system (Crowd-BT / Bradley-Terry estimator). github.com/anishathalye/gavel</a></li>
    <li id="ref-13"><a href="https://github.com/dribdat/awesome-hackathon" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[13]</span> awesome-hackathon, curated list of open-source, self-hostable hackathon platforms and tools. github.com/dribdat/awesome-hackathon</a></li>
    <li id="ref-14"><a href="https://github.com/ViRb3/devpost-api" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[14]</span> Unofficial Devpost API, a scraper-based community project standing in for the API that does not exist. github.com/ViRb3/devpost-api</a></li>
    <li id="ref-15"><a href="https://raptors.dev" target="_blank" rel="noopener" style="color:#55658C;display:block" style-hover="color:#E6ECFF"><span style="color:#FF3D6E">[15]</span> Hackathon Raptors event archive, 35 events from September 2023 to July 2026. raptors.dev</a></li>
  </ol>
</section>

<div style="overflow:hidden;border-top:1px solid #00E5D0;border-bottom:1px solid #00E5D0;background:#FF3D6E">
  <div data-marquee2 style="user-select:none;-webkit-user-select:none;display:flex;width:max-content;animation:mq 28s linear infinite reverse;will-change:transform">
    <div style="display:flex;flex:none;font-family:'Archivo Black',sans-serif;font-size:clamp(1.6rem,4vw,3.2rem);line-height:1;letter-spacing:-.04em;text-transform:uppercase;color:#0B1020;padding:12px 0">
      <span style="padding:0 22px">72 HOURS</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">ONE PRODUCT</span><span style="padding:0 22px">WE RUN THE WINNER</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">+</span><span style="padding:0 22px">72 HOURS</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">ONE PRODUCT</span><span style="padding:0 22px">WE RUN THE WINNER</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">+</span>
    </div>
    <div aria-hidden="true" style="display:flex;flex:none;font-family:'Archivo Black',sans-serif;font-size:clamp(1.6rem,4vw,3.2rem);line-height:1;letter-spacing:-.04em;text-transform:uppercase;color:#0B1020;padding:12px 0">
      <span style="padding:0 22px">72 HOURS</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">ONE PRODUCT</span><span style="padding:0 22px">WE RUN THE WINNER</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">+</span><span style="padding:0 22px">72 HOURS</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">ONE PRODUCT</span><span style="padding:0 22px">WE RUN THE WINNER</span><span style="padding:0 22px;color:transparent;-webkit-text-stroke:1px #0B1020">+</span>
    </div>
  </div>
</div>
<footer id="discord" style="border-top:1px solid #00E5D0;position:relative">
  <div style="position:absolute;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(90deg,rgba(230,236,255,.05) 1px,transparent 1px),linear-gradient(0deg,rgba(230,236,255,.05) 1px,transparent 1px);background-size:calc(100%/8) 90px"></div>
  <div style="position:relative;z-index:1;padding:clamp(40px,6vw,80px) clamp(12px,2vw,24px) 0;max-width:1680px;margin:0 auto">
    <div style="display:flex;flex-wrap:wrap;gap:clamp(24px,3vw,44px) clamp(20px,2.5vw,40px);align-items:flex-start">
      <div style="flex:2.2 1 340px;min-width:0;max-width:560px">
        <div style="font-family:'Archivo Black',sans-serif;font-size:clamp(2rem,4.4vw,4.4rem);line-height:.9;letter-spacing:-.05em;color:#E6ECFF;overflow-wrap:anywhere">DOGFOOD<span style="color:#FF3D6E">®</span></div>
        <p style="margin:20px 0 0;max-width:48ch;font:400 12.5px/1.8 'JetBrains Mono',monospace;color:#6B7A9E">A <a href="https://raptors.dev" target="_blank" rel="noopener" style="color:#FF3D6E" style-hover="color:#E6ECFF">raptors.dev</a> hackathon. Build the submission and judging platform we will actually run. Open source, self-hosted, yours.</p>
        <a href="https://discord.gg/xfYPDZYqeh" target="_blank" rel="noopener" data-magnet="1" style="display:inline-flex;align-items:center;gap:10px;margin-top:24px;background:#FF3D6E;color:#0B1020;font:700 11px/1 'JetBrains Mono',monospace;letter-spacing:.18em;text-transform:uppercase;padding:14px 20px;border:1px solid #FF3D6E;transition:background .12s linear,color .12s linear,transform .08s linear" style-hover="background:#0B1020;color:#FF3D6E" style-active="transform:translateY(1px) scale(.98)">[ Go to Discord ]</a>
      </div>
      <div style="flex:1 1 150px;min-width:0">
        <div style="font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:16px">Navigate</div>
        <div style="display:flex;flex-direction:column;gap:9px;font:400 11.5px/1.35 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase">
          <a href="#about" style="color:#6B7A9E" style-hover="color:#E6ECFF">About</a>
          <a href="#tiers" style="color:#6B7A9E" style-hover="color:#E6ECFF">Tiers</a>
          <a href="#timeline" style="color:#6B7A9E" style-hover="color:#E6ECFF">Timeline</a>
          <a href="#scoring" style="color:#6B7A9E" style-hover="color:#E6ECFF">Scoring</a>
          <a href="#prizes" style="color:#6B7A9E" style-hover="color:#E6ECFF">Prizes</a>
          <a href="#rules" style="color:#6B7A9E" style-hover="color:#E6ECFF">Rules</a>
          <a href="#judges" style="color:#6B7A9E" style-hover="color:#E6ECFF">Judges</a>
          <a href="#faq" style="color:#6B7A9E" style-hover="color:#E6ECFF">FAQ</a>
          <a href="/spec" style="color:#00E5D0" style-hover="color:#E6ECFF">Spec</a>
        </div>
      </div>
      <div style="flex:1 1 150px;min-width:0">
        <div style="font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:16px">Sister events</div>
        <div style="display:flex;flex-direction:column;gap:9px;font:400 11.5px/1.35 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#6B7A9E;overflow-wrap:anywhere">
          <a href="https://www.zerodepshack.com/" target="_blank" rel="noopener" style="color:#6B7A9E" style-hover="color:#E6ECFF">Zero Dependency</a>
          <a href="https://coderesurrection.com/2026/" target="_blank" rel="noopener" style="color:#6B7A9E" style-hover="color:#E6ECFF">Port Mortem</a>
          <a href="https://codeolympics.com/2026" target="_blank" rel="noopener" style="color:#6B7A9E" style-hover="color:#E6ECFF">Code Olympics</a>
          <a href="https://slopscan.dev/" target="_blank" rel="noopener" style="color:#6B7A9E" style-hover="color:#E6ECFF">Slop Scan</a>
          <a href="https://www.raptors.dev/conference" target="_blank" rel="noopener" style="color:#6B7A9E" style-hover="color:#E6ECFF">Raptors Conference</a>
        </div>
      </div>
      <div style="flex:1.4 1 210px;min-width:0">
        <div style="font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#FF3D6E;margin-bottom:16px">Connect</div>
        <div style="display:flex;flex-direction:column;gap:9px;font:400 11.5px/1.6 'JetBrains Mono',monospace;color:#6B7A9E;overflow-wrap:anywhere">
          <a href="mailto:hello@raptors.dev" style="color:#FF3D6E">hello@raptors.dev</a>
          <span>Hackathon Raptors</span>
          <span>Community Interest Company 15557917</span>
          <span>Office 2131, 182-184 High Street North,<br>East Ham, London, E6 2JA, United Kingdom</span>
        </div>
      </div>
      <div style="border:1px solid #1B2540;background:#0E1428;padding:22px 20px;display:flex;flex-direction:column;gap:16px;align-items:flex-start;min-width:0;flex:1 1 170px">
        <div style="font:500 10px/1 'IBM Plex Mono',monospace;letter-spacing:.26em;text-transform:uppercase;color:#00E5D0">Organised by</div>
        <a href="https://raptors.dev" target="_blank" rel="noopener" aria-label="Hackathon Raptors" style="display:block;width:100%;max-width:80px;line-height:0"><img src="img/raptors-mark.png" alt="Hackathon Raptors" draggable="false" style="user-select:none;-webkit-user-select:none;-webkit-user-drag:none;display:block;width:100%;max-width:80px;height:auto"></a>
        <div style="font:400 9.5px/1.7 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#3A4A70">35 events since 2023<br>85+ countries</div>
      </div>
    </div>
    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 24px;margin:clamp(32px,5vw,64px) 0 0;padding:20px 0;border-top:1px solid #1B2540;font:400 10px/1.6 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:#4A5A80;overflow-wrap:anywhere">
      <span>© 2026 Dogfood Hackathon · Built by <a href="https://raptors.dev" target="_blank" rel="noopener" style="color:#4A5A80" style-hover="color:#E6ECFF">raptors.dev</a></span>
      <span>+ 51.5310°N 0.0500°E + REV 2.6 + UNIT / DF-01 ™</span>
    </div>
  </div>
</footer>

</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props="{&quot;$preview&quot;:{&quot;width&quot;:1440,&quot;height&quot;:900}}">
// The dc-runtime evaluates this block as text with `DCLogic` and `React` in
// scope, so it cannot use a `src`. The class itself lives in app.js.
const Component = window.DCApp(DCLogic, React);
</script>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/v31edd6df95cf4e85bb4c19e7a9bdbcba1788362987495" integrity="sha512-iIg7k2xntmwu6/uSb5tpc/hySgZc4eoL31yB29W6tJFo2akwjPWcEqnCEdJvGexCL0KEQwVYv5BlowfhVz26hg==" data-cf-beacon='{"version":"2024.11.0","token":"f5d751f73b2845f7a6caf9c88f4346c8","r":1,"spa":2}' crossorigin="anonymous"></script>
</body>
</html>
