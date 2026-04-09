from flask import Flask, render_template_string

app = Flask(__name__)

ARTICLES = [
    {
        "title": "Cold Start Problem in Recommender Systems",
        "url": "https://www.freecodecamp.org/news/cold-start-problem-in-recommender-systems/",
        "source": "freeCodeCamp",
        "tags": ["machine learning", "recommender systems", "AI"],
        "color": "#0a0a23",
    },
    {
        "title": "What's Changing in Vector Databases in 2026",
        "url": "https://dev.to/actiandev/whats-changing-in-vector-databases-in-2026-3pbo",
        "source": "DEV.to",
        "tags": ["databases", "vector databases", "data engineering"],
        "color": "#0a0a0a",
    },
    {
        "title": "Adversarial Machine Learning: Preventing Bad Actors from Compromising AI Models",
        "url": "https://hackernoon.com/adversarial-machine-learning-is-preventing-bad-actors-from-compromising-ai-models",
        "source": "HackerNoon",
        "tags": ["machine learning", "security", "adversarial AI"],
        "color": "#00ff00",
    },
    {
        "title": "Explainable Artificial Intelligence (XAI): Making Sense of AI Decisions",
        "url": "https://medium.com/@techwithpraisejames/explainable-artificial-intelligence-xai-making-sense-of-ai-decisions-5fa655655490",
        "source": "Medium",
        "tags": ["AI", "explainability", "XAI"],
        "color": "#000000",
    },
    {
        "title": "Decision Trees in Python Scikit-Learn: A Complete Guide for Beginners",
        "url": "https://medium.com/@techwithpraisejames/decision-trees-in-python-scikit-learn-a-complete-guide-for-beginners-15cb0540180f",
        "source": "Medium",
        "tags": ["python", "scikit-learn", "decision trees", "beginners"],
        "color": "#000000",
    },
]

SOCIALS = [
    {
        "name": "YouTube",
        "url": "https://www.youtube.com/channel/UCwVDq2mG2FuNCRzAf-ypLvg",
        "icon": "youtube",
        "color": "#FF0000",
        "description": "Tech tutorials, AI walkthroughs & more",
    },
    {
        "name": "Newsletter",
        "url": "https://techwithpraisejames.substack.com/",
        "icon": "newsletter",
        "color": "#FF6719",
        "description": "Weekly insights on AI, ML & tech",
    },
    {
        "name": "GitHub",
        "url": "https://github.com/Techwithpraisejames",
        "icon": "github",
        "color": "#f0f0f0",
        "description": "Open source projects & code",
    },
]

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Praise James — Tech, AI & Everything In Between</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0a0a;--surface:#141414;--surface2:#1e1e1e;
  --text:#f0f0f0;--text2:#a0a0a0;--accent:#6c63ff;--accent2:#ff6b6b;
  --glow:rgba(108,99,255,.15);
}
html{scroll-behavior:smooth;overflow-x:hidden;scroll-snap-type:y mandatory}
body{
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
  background:var(--bg);color:var(--text);
  overflow-x:hidden;
}

/* SCROLLBAR */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--accent);border-radius:3px}

/* SECTIONS */
section{
  min-height:100vh;padding:60px 24px;
  scroll-snap-align:start;
  position:relative;
}

/* HERO */
.hero{
  display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;gap:24px;
  background:radial-gradient(ellipse at 50% 0%,rgba(108,99,255,.12) 0%,transparent 60%);
}
.hero h1{
  font-size:clamp(2.4rem,6vw,4.5rem);font-weight:800;
  letter-spacing:-1px;line-height:1.1;
}
.hero h1 .highlight{
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero p{font-size:1.15rem;color:var(--text2);max-width:540px;line-height:1.6}
.scroll-hint{
  position:absolute;bottom:32px;left:50%;transform:translateX(-50%);
  display:flex;flex-direction:column;align-items:center;gap:8px;
  color:var(--text2);font-size:.85rem;animation:bounce 2s infinite;
}
@keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(8px)}}

/* NAV PILLS */
.nav-pills{
  position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:100;
  display:flex;gap:4px;padding:6px;
  background:rgba(20,20,20,.85);backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,.08);border-radius:40px;
}
.nav-pills a{
  padding:8px 18px;border-radius:30px;font-size:.82rem;font-weight:600;
  color:var(--text2);text-decoration:none;transition:.25s;white-space:nowrap;
}
.nav-pills a:hover,.nav-pills a.active{
  color:var(--text);background:var(--accent);
}

/* HORIZONTAL SCROLL TRACK */
.h-section{padding-bottom:40px}
.h-section h2{
  font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;
  margin-bottom:8px;padding-left:max(24px,calc((100vw - 1100px)/2));
}
.h-section .subtitle{
  color:var(--text2);font-size:.95rem;margin-bottom:28px;
  padding-left:max(24px,calc((100vw - 1100px)/2));
}
.h-track{
  display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;
  padding:0 max(24px,calc((100vw - 1100px)/2)) 16px;
  -webkit-overflow-scrolling:touch;
}
.h-track::-webkit-scrollbar{height:4px}

/* ARTICLE CARD */
.card{
  flex:0 0 340px;scroll-snap-align:start;
  background:var(--surface);border:1px solid rgba(255,255,255,.06);
  border-radius:16px;padding:28px;
  display:flex;flex-direction:column;gap:14px;
  transition:transform .3s,box-shadow .3s,border-color .3s;
  text-decoration:none;color:var(--text);cursor:pointer;
}
.card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 40px var(--glow);
  border-color:var(--accent);
}
.card .source{
  font-size:.75rem;font-weight:700;text-transform:uppercase;
  letter-spacing:1.5px;color:var(--accent);
}
.card .card-title{font-size:1.15rem;font-weight:600;line-height:1.4}
.card .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto}
.card .tag{
  font-size:.7rem;padding:4px 10px;border-radius:20px;
  background:rgba(108,99,255,.12);color:var(--accent);font-weight:600;
}

/* SOCIAL CARD */
.social-card{
  flex:0 0 300px;scroll-snap-align:start;
  border-radius:16px;padding:32px;
  display:flex;flex-direction:column;gap:16px;
  transition:transform .3s,box-shadow .3s;
  text-decoration:none;color:var(--text);
  border:1px solid rgba(255,255,255,.06);
  position:relative;overflow:hidden;
}
.social-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:var(--card-accent);
}
.social-card:hover{
  transform:translateY(-4px) scale(1.01);
  box-shadow:0 16px 48px rgba(0,0,0,.4);
}
.social-icon{
  width:52px;height:52px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.5rem;font-weight:800;
  background:rgba(255,255,255,.06);
}
.social-card .social-name{font-size:1.3rem;font-weight:700}
.social-card .social-desc{font-size:.9rem;color:var(--text2);line-height:1.5}
.social-card .visit{
  margin-top:auto;font-size:.85rem;font-weight:600;
  color:var(--accent);display:flex;align-items:center;gap:6px;
}

/* NEWSLETTER SECTION */
.newsletter-section{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;gap:20px;
  background:radial-gradient(ellipse at 50% 50%,rgba(255,107,107,.06) 0%,transparent 60%);
}
.newsletter-section h2{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700}
.newsletter-section p{color:var(--text2);max-width:500px;line-height:1.6}

/* SEARCH */
.search-wrap{
  width:100%;max-width:560px;position:relative;margin:0 auto;
}
.search-wrap input{
  width:100%;padding:16px 20px 16px 52px;
  background:var(--surface);border:1px solid rgba(255,255,255,.1);
  border-radius:14px;color:var(--text);font-size:1rem;
  outline:none;transition:border-color .25s,box-shadow .25s;
}
.search-wrap input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--glow);
}
.search-wrap input::placeholder{color:var(--text2)}
.search-wrap .search-icon{
  position:absolute;left:18px;top:50%;transform:translateY(-50%);
  color:var(--text2);font-size:1.1rem;pointer-events:none;
}

/* SEARCH RESULTS */
.search-results{
  width:100%;max-width:560px;margin:0 auto;
  display:flex;flex-direction:column;gap:12px;
  max-height:360px;overflow-y:auto;
}
.search-result{
  background:var(--surface);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:18px 22px;text-align:left;
  text-decoration:none;color:var(--text);
  transition:border-color .2s,transform .2s;display:block;
}
.search-result:hover{border-color:var(--accent);transform:translateX(4px)}
.search-result .sr-source{
  font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:1.5px;color:var(--accent2);margin-bottom:6px;
}
.search-result .sr-title{font-size:1rem;font-weight:600}
.no-results{color:var(--text2);font-size:.9rem;padding:20px}

/* CTA BUTTON */
.cta{
  display:inline-flex;align-items:center;gap:8px;
  padding:14px 32px;border-radius:40px;font-weight:700;
  font-size:.95rem;text-decoration:none;color:#fff;
  background:linear-gradient(135deg,var(--accent),#8b5cf6);
  transition:transform .2s,box-shadow .2s;
}
.cta:hover{transform:translateY(-2px);box-shadow:0 8px 30px var(--glow)}

/* FOOTER */
footer{
  padding:40px 24px;text-align:center;
  border-top:1px solid rgba(255,255,255,.06);
}
footer p{color:var(--text2);font-size:.85rem}
footer .footer-links{display:flex;justify-content:center;gap:20px;margin-top:16px}
footer a{color:var(--text2);text-decoration:none;font-size:.85rem;transition:color .2s}
footer a:hover{color:var(--accent)}

/* SWIPE INDICATOR */
.swipe-indicator{
  display:flex;gap:6px;justify-content:center;padding:12px 0;
}
.swipe-dot{
  width:8px;height:8px;border-radius:50%;
  background:rgba(255,255,255,.15);transition:background .3s,transform .3s;
}
.swipe-dot.active{background:var(--accent);transform:scale(1.3)}

/* RESPONSIVE */
@media(max-width:640px){
  .nav-pills{top:auto;bottom:16px;left:8px;right:8px;
    transform:none;justify-content:center;overflow-x:auto}
  .nav-pills a{padding:8px 14px;font-size:.75rem}
  section{padding:48px 16px;min-height:auto}
  .hero{min-height:100vh}
  .card{flex:0 0 280px;padding:22px}
  .social-card{flex:0 0 260px;padding:24px}
}

/* INFINITE SCROLL ARTICLES */
.v-articles{
  max-width:700px;margin:40px auto 0;
  display:flex;flex-direction:column;gap:16px;
}
.v-article{
  background:var(--surface);border:1px solid rgba(255,255,255,.06);
  border-radius:14px;padding:24px;
  display:flex;gap:18px;align-items:center;
  text-decoration:none;color:var(--text);
  transition:border-color .2s,transform .2s;
}
.v-article:hover{border-color:var(--accent);transform:translateX(6px)}
.v-article .v-num{
  font-size:2rem;font-weight:800;color:rgba(108,99,255,.3);
  flex-shrink:0;width:48px;text-align:center;
}
.v-article .v-info{display:flex;flex-direction:column;gap:4px}
.v-article .v-source{
  font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:1.5px;color:var(--accent);
}
.v-article .v-title{font-size:1rem;font-weight:600;line-height:1.4}

/* SECTION LABELS */
.section-label{
  font-size:.75rem;font-weight:700;text-transform:uppercase;
  letter-spacing:2px;color:var(--accent);margin-bottom:8px;
  padding-left:max(24px,calc((100vw - 1100px)/2));
}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav-pills" id="nav">
  <a href="#hero">Home</a>
  <a href="#articles">Articles</a>
  <a href="#connect">Connect</a>
  <a href="#newsletter">Newsletter</a>
</nav>

<!-- HERO -->
<section class="hero" id="hero">
  <p style="font-size:.85rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--accent)">
    Tech Writer &bull; Content Creator &bull; AI Enthusiast
  </p>
  <h1>Hey, I'm <span class="highlight">Praise James</span></h1>
  <p>
    I write about AI, machine learning, and emerging tech.
    This is your one-stop hub for everything I create &mdash; articles, videos, code, and more.
  </p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
    <a class="cta" href="#articles">Explore My Work &darr;</a>
    <a class="cta" href="https://techwithpraisejames.substack.com/" target="_blank"
       style="background:linear-gradient(135deg,#ff6b6b,#ff6719)">
      Subscribe &nearr;
    </a>
  </div>
  <div class="scroll-hint">
    <span>Scroll to explore</span>
    <span style="font-size:1.4rem">&darr;</span>
  </div>
</section>

<!-- ARTICLES — HORIZONTAL SWIPE -->
<section class="h-section" id="articles">
  <p class="section-label">Published Work</p>
  <h2>Articles &amp; Tutorials</h2>
  <p class="subtitle">Swipe or drag to browse &rarr;</p>
  <div class="h-track" id="articleTrack">
    {% for a in articles %}
    <a class="card" href="{{ a.url }}" target="_blank" rel="noopener">
      <span class="source">{{ a.source }}</span>
      <span class="card-title">{{ a.title }}</span>
      <div class="tags">
        {% for t in a.tags %}<span class="tag">{{ t }}</span>{% endfor %}
      </div>
    </a>
    {% endfor %}
  </div>
  <div class="swipe-indicator" id="articleDots"></div>

  <!-- VERTICAL INFINITE SCROLL -->
  <div class="v-articles" id="vArticles">
    {% for a in articles %}
    <a class="v-article" href="{{ a.url }}" target="_blank" rel="noopener">
      <span class="v-num">{{ "%02d"|format(loop.index) }}</span>
      <div class="v-info">
        <span class="v-source">{{ a.source }}</span>
        <span class="v-title">{{ a.title }}</span>
      </div>
    </a>
    {% endfor %}
  </div>
</section>

<!-- CONNECT — HORIZONTAL SWIPE -->
<section class="h-section" id="connect">
  <p class="section-label">Stay Connected</p>
  <h2>Find Me Everywhere</h2>
  <p class="subtitle">Swipe to see all platforms &rarr;</p>
  <div class="h-track" id="socialTrack">
    {% for s in socials %}
    <a class="social-card" href="{{ s.url }}" target="_blank" rel="noopener"
       style="background:var(--surface);--card-accent:{{ s.color }}">
      <div class="social-icon" style="color:{{ s.color }}">
        {% if s.icon == 'youtube' %}&#9654;
        {% elif s.icon == 'newsletter' %}&#9993;
        {% elif s.icon == 'github' %}&#10100;&#10101;
        {% endif %}
      </div>
      <span class="social-name">{{ s.name }}</span>
      <span class="social-desc">{{ s.description }}</span>
      <span class="visit">Visit &rarr;</span>
    </a>
    {% endfor %}
  </div>
  <div class="swipe-indicator" id="socialDots"></div>
</section>

<!-- NEWSLETTER + SEARCH -->
<section class="newsletter-section" id="newsletter">
  <p class="section-label">Newsletter</p>
  <h2>Search My Content</h2>
  <p>Find articles by topic, keyword, or technology. Or subscribe to get new ones in your inbox.</p>
  <div class="search-wrap">
    <span class="search-icon">&#128269;</span>
    <input type="text" id="searchInput" placeholder="Search articles... (e.g. AI, vector databases, Python)"
           autocomplete="off">
  </div>
  <div class="search-results" id="searchResults"></div>
  <a class="cta" href="https://techwithpraisejames.substack.com/" target="_blank"
     style="background:linear-gradient(135deg,#ff6719,#ff6b6b);margin-top:12px">
    Subscribe to Newsletter &nearr;
  </a>
</section>

<!-- FOOTER -->
<footer>
  <p>&copy; 2026 Praise James. Built with purpose.</p>
  <div class="footer-links">
    <a href="https://www.youtube.com/channel/UCwVDq2mG2FuNCRzAf-ypLvg" target="_blank">YouTube</a>
    <a href="https://techwithpraisejames.substack.com/" target="_blank">Newsletter</a>
    <a href="https://github.com/Techwithpraisejames" target="_blank">GitHub</a>
  </div>
</footer>

<script>
// Article data for search
const articles = {{ articles_json | safe }};

// SEARCH
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

searchInput.addEventListener('input', function() {
  const q = this.value.toLowerCase().trim();
  searchResults.innerHTML = '';
  if (!q) return;

  const matches = articles.filter(a =>
    a.title.toLowerCase().includes(q) ||
    a.source.toLowerCase().includes(q) ||
    a.tags.some(t => t.toLowerCase().includes(q))
  );

  if (matches.length === 0) {
    searchResults.innerHTML = '<div class="no-results">No articles found. Try a different keyword.</div>';
    return;
  }

  matches.forEach(a => {
    const el = document.createElement('a');
    el.className = 'search-result';
    el.href = a.url;
    el.target = '_blank';
    el.rel = 'noopener';
    el.innerHTML = `<div class="sr-source">${a.source}</div><div class="sr-title">${a.title}</div>`;
    searchResults.appendChild(el);
  });
});

// SWIPE DOTS
function setupDots(trackId, dotsId) {
  const track = document.getElementById(trackId);
  const dotsContainer = document.getElementById(dotsId);
  const cards = track.children;
  if (!cards.length) return;

  for (let i = 0; i < cards.length; i++) {
    const dot = document.createElement('div');
    dot.className = 'swipe-dot' + (i === 0 ? ' active' : '');
    dotsContainer.appendChild(dot);
  }

  track.addEventListener('scroll', () => {
    const scrollLeft = track.scrollLeft;
    const cardWidth = cards[0].offsetWidth + 20;
    const idx = Math.round(scrollLeft / cardWidth);
    dotsContainer.querySelectorAll('.swipe-dot').forEach((d, i) => {
      d.classList.toggle('active', i === idx);
    });
  });
}
setupDots('articleTrack', 'articleDots');
setupDots('socialTrack', 'socialDots');

// NAV ACTIVE STATE
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-pills a');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(l => {
        l.classList.toggle('active', l.getAttribute('href') === '#' + id);
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => observer.observe(s));

// INFINITE SCROLL — duplicate articles to simulate endless content
const vArticles = document.getElementById('vArticles');
let loadCount = 0;
const maxLoads = 8;

function loadMore() {
  if (loadCount >= maxLoads) return;
  loadCount++;
  articles.forEach((a, i) => {
    const idx = loadCount * articles.length + i + 1;
    const el = document.createElement('a');
    el.className = 'v-article';
    el.href = a.url;
    el.target = '_blank';
    el.rel = 'noopener';
    el.innerHTML = `
      <span class="v-num">${String(idx).padStart(2, '0')}</span>
      <div class="v-info">
        <span class="v-source">${a.source}</span>
        <span class="v-title">${a.title}</span>
      </div>`;
    vArticles.appendChild(el);
  });
}

// Use IntersectionObserver for infinite scroll
const sentinel = document.createElement('div');
sentinel.style.height = '1px';
vArticles.after(sentinel);

const scrollObserver = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) loadMore();
}, { rootMargin: '200px' });

scrollObserver.observe(sentinel);
</script>

</body>
</html>
"""


@app.route("/")
def home():
    import json

    return render_template_string(
        HTML_TEMPLATE,
        articles=ARTICLES,
        socials=SOCIALS,
        articles_json=json.dumps(ARTICLES),
    )


# Vercel expects the app object
