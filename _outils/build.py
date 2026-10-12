# -*- coding: utf-8 -*-
import os, sys, html, re
sys.path.insert(0, os.path.dirname(__file__))
from data import R, NEEDS, REGIONS, KINDS, kind

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E = html.escape

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Gilda+Display&display=swap">'

T = {
 "fr": dict(
   site="À portée de main", tag="Within Reach",
   slogan="Les ressources existent. Nous les rendons visibles.",
   skip="Aller au contenu",
   emergency="Urgence :", emergency_label="danger immédiat",
   hist="Effacer l'historique", exit="Quitter rapidement", exit_short="Quitter", exit_long="rapidement",
   menu="Menu",
   nav=[("index","Accueil"),("ressources","Trouver une ressource"),("comprendre","Comprendre les ressources"),("a-propos","À propos")],
   lang_label="English", lang_code="en",
   hist_title="Effacer l'historique de navigation",
   hist_items=[
     ("Chrome sur Android","Appuyez sur <b>⋮</b> → <b>Supprimer les données de navigation</b> (ou ⋮ → Historique)."),
     ("Safari sur iPhone","Ouvrez <b>Réglages</b> → <b>Safari</b> (ou Réglages → Apps → Safari) → <b>Effacer historique et données de site</b>."),
     ("Ordinateur (Chrome, Edge, Firefox)","Appuyez sur <kbd>Ctrl</kbd> + <kbd>Maj</kbd> + <kbd>Suppr</kbd> (sur Mac : <kbd>⌘</kbd> + <kbd>Maj</kbd> + <kbd>Suppr</kbd>)."),
   ],
   hist_tip="Si effacer tout l'historique risque d'attirer l'attention, supprimez seulement les pages de ce site. La navigation privée n'enregistre pas l'historique.",
   footer_sos='Vous ne trouvez pas ce qu\'il vous faut ou souhaitez parler à quelqu\'un ? Appelez SOS violence conjugale au <a href="tel:18003639010">1 800 363-9010</a>, disponible 24/7.',
   contact="Nous joindre",
   k_tel="Tél.", k_sms="Texto", k_mail="Courriel", site_link="Site web", tool="Outil", h24="24/7",
   back="↑ Retour aux besoins", back_r="↑ Retour aux régions",
 ),
 "en": dict(
   site="Within Reach", tag="À portée de main",
   slogan="The resources exist. We make them visible.",
   skip="Skip to content",
   emergency="Emergency:", emergency_label="immediate danger",
   hist="Clear browsing history", exit="Quick exit", exit_short="Quick exit", exit_long="",
   menu="Menu",
   nav=[("index","Home"),("ressources","Find a resource"),("comprendre","Understanding resources"),("a-propos","About")],
   lang_label="Français", lang_code="fr",
   hist_title="Clear your browsing history",
   hist_items=[
     ("Chrome on Android","Tap <b>⋮</b> → <b>Delete browsing data</b> (or ⋮ → History)."),
     ("Safari on iPhone","Open <b>Settings</b> → <b>Safari</b> (or Settings → Apps → Safari) → <b>Clear History and Website Data</b>."),
     ("Computer (Chrome, Edge, Firefox)","Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Delete</kbd> (on Mac: <kbd>⌘</kbd> + <kbd>Shift</kbd> + <kbd>Delete</kbd>)."),
   ],
   hist_tip="If clearing all your history might draw attention, delete only the pages from this site. Private browsing does not save your history.",
   footer_sos='Can\'t find what you need, or want to talk to someone? Call SOS violence conjugale at <a href="tel:18003639010">1 800 363-9010</a>, available 24/7.',
   contact="Contact us",
   k_tel="Phone", k_sms="Text", k_mail="Email", site_link="Website", tool="Tool", h24="24/7",
   back="↑ Back to needs", back_r="↑ Back to regions",
 ),
}

EXIT_URL = "https://www.google.com/"
EXIT_JS = "window.location.replace('https://www.google.com/');return false;"

def ornament(extra=""):
    return f'<div class="ornament {extra}" aria-hidden="true"><span><i></i><b></b><i></i></span></div>'

def page(lang, slug, title, body, section=None):
    t = T[lang]
    pre = "" if lang == "fr" else "../"
    other = f"en/{slug}.html" if lang == "fr" else f"../{slug}.html"
    navcur = section or slug
    nav = "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == navcur else ""}>{E(lbl)}</a>' for s, lbl in t["nav"])
    hist_items = "".join(f"<div><dt>{E(a)}</dt><dd>{b}</dd></div>" for a, b in t["hist_items"])
    doc_title = t["site"] if slug == "index" else f"{title} · {t['site']}"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(doc_title)}</title>
<meta name="description" content="{E(t['slogan'])}">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="{pre}img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
<link rel="alternate" hreflang="{t['lang_code']}" href="{other}">
{FONTS}
<link rel="stylesheet" href="{pre}style.css">
</head>
<body>
<a class="skip" href="#contenu">{E(t['skip'])}</a>
<div class="safety" role="region" aria-label="{E(t['hist'])} / {E(t['exit'])}">
  <div class="wrap">
    <p class="safety__911"><span class="safety__label">{E(t['emergency'])} </span><a href="tel:911">911</a> <span class="safety__label">({E(t['emergency_label'])})</span></p>
    <details class="history">
      <summary>{E(t['hist'])}</summary>
      <div class="history__panel">
        <h2>{E(t['hist_title'])}</h2>
        <dl>{hist_items}</dl>
        <p class="tip">{E(t['hist_tip'])}</p>
      </div>
    </details>
    <a class="exit" href="{EXIT_URL}" rel="noreferrer" onclick="{EXIT_JS}">{E(t['exit_short'])}<span class="exit__long"> {E(t['exit_long'])}</span> ✕</a>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="{pre}img/lotus.png" alt="" width="52" height="40"><span class="brand__name">{E(t['site'])}<small>{E(t['tag'])}</small></span></a>
    <input type="checkbox" id="menu-toggle" class="menu-toggle visually-hidden">
    <label for="menu-toggle" class="menu-btn">{E(t['menu'])}</label>
    <nav class="nav" aria-label="Menu">{nav}<a class="lang" href="{other}" hreflang="{t['lang_code']}" lang="{t['lang_code']}">{E(t['lang_label'])}</a></nav>
  </div>
</header>
<main id="contenu">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p class="footer-sos">{t['footer_sos']}</p>
    <div class="footer-meta">
      <span class="slogan">{E(t['slogan'])}</span>
      <a href="a-propos.html#contact">{E(t['contact'])}</a>
      <a href="https://www.instagram.com/within_reach.ca/" rel="noreferrer">Instagram @within_reach.ca</a>
    </div>
  </div>
</footer>
</body>
</html>
'''

def digits(n): return re.sub(r"\D", "", n)

def card(r, lang):
    t = T[lang]
    url = r.get("url_en", r["url"]) if lang == "en" else r["url"]
    badge = ""
    if r.get("h24"): badge = f'<span class="badge">{t["h24"]}</span>'
    elif r.get("tool"): badge = f'<span class="badge badge--tool">{t["tool"]}</span>'
    rows = []
    for k, v, extra in r["contacts"]:
        if extra and "|" in extra: extra = extra.split("|")[0 if lang == "fr" else 1]
        x = f' <span class="x">{E(extra)}</span>' if extra else ""
        if k == "tel": rows.append(f'<li><span class="k">{t["k_tel"]}</span><a href="tel:{digits(v)}">{E(v)}</a>{x}</li>')
        if k == "sms": rows.append(f'<li><span class="k">{t["k_sms"]}</span><a href="sms:{digits(v)}">{E(v)}</a>{x}</li>')
        if k == "mail": rows.append(f'<li><span class="k">{t["k_mail"]}</span><a href="mailto:{v}">{E(v)}</a>{x}</li>')
    contacts = f'<ul class="contacts">{"".join(rows)}</ul>' if rows else ""
    note = r.get("note_" + lang)
    note = f'<p class="note">{E(note)}</p>' if note else ""
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return f'''<li><article class="card" id="r-{r["id"]}">
  <div class="card__top"><h3>{E(r["name"])}</h3>{badge}</div>
  <p>{E(r[lang])}</p>{note}
  {contacts}
  <p class="card__site"><a href="{E(url)}" target="_blank" rel="noopener noreferrer">{t["site_link"]} : {E(host)}</a></p>
</article></li>'''

def cards(rs, lang):
    return '<ul class="cards">' + "".join(card(r, lang) for r in rs) + "</ul>"

def by_name(rs): return sorted(rs, key=lambda r: r["name"].lower().replace("é","e").replace("l'",""))

def priority(rs):
    # 24/7 lines first, then the rest by name
    return sorted(rs, key=lambda r: (0 if r["id"] == "sos" else 1, 0 if r.get("h24") else 1, r["name"].lower()))

# ---------------------------------------------------------------- pages
def home(lang):
    if lang == "fr":
        b = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero__text">
      <h1>Vous cherchez du soutien&nbsp;?</h1>
      <p class="alone">Vous n'êtes pas seule.</p>
      <p>Des ressources gratuites et confidentielles sont disponibles pour les personnes qui vivent de la violence conjugale, du contrôle, des menaces ou une situation qui les met mal à l'aise ou en danger.</p>
      <p>Vous pouvez trouver de l'aide, à votre rythme.</p>
      <div class="actions">
        <a class="btn btn--primary" href="ressources.html">Trouver une ressource</a>
        <a class="btn" href="#parler">Parler à quelqu'un maintenant</a>
        <a class="btn" href="#ecrire">Je préfère écrire</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-label="Contact immédiat">
  <div class="wrap panels">
    <article class="panel" id="parler">
      <p class="eyebrow">Par téléphone</p>
      <h2>Parler à quelqu'un maintenant</h2>
      <a class="bignum" href="tel:18003639010">1 800 363-9010</a>
      <ul class="facts"><li>24/7</li><li>Gratuit</li><li>Anonyme et confidentiel</li><li>Français et anglais</li></ul>
      <p><strong>SOS violence conjugale.</strong> Une intervenante vous écoute, vous aide à évaluer votre sécurité et peut appeler une maison d'hébergement pour vous. Vous n'avez pas besoin d'être certaine que c'est de la violence pour appeler.</p>
      <p class="small muted">Violence sexuelle : Info-aide violence sexuelle, <a href="tel:18889339007">1 888 933-9007</a>.</p>
    </article>
    <article class="panel" id="ecrire">
      <p class="eyebrow">Par écrit</p>
      <h2>Je préfère écrire</h2>
      <ul class="contacts">
        <li><span class="k">Texto</span><a href="sms:4386011211">438 601-1211</a></li>
        <li><span class="k">Clavardage</span><a href="https://sosviolenceconjugale.ca/fr/clavardage" target="_blank" rel="noopener noreferrer">sosviolenceconjugale.ca/fr/clavardage</a></li>
        <li><span class="k">Courriel</span><a href="mailto:sos@sosviolenceconjugale.ca">sos@sosviolenceconjugale.ca</a></li>
      </ul>
      <p>Le même service de SOS violence conjugale, gratuit et confidentiel, par écrit. La fenêtre de clavardage s'ouvre lorsqu'une intervenante est disponible.</p>
      <p class="small muted">Si quelqu'un peut lire vos messages, pensez à effacer la conversation après l'échange.</p>
    </article>
  </div>
</section>

<section class="section" aria-labelledby="danger-titre">
  <div class="wrap">
    <div class="danger">
      <div class="danger__col">
        <h2 id="danger-titre">Vous êtes en danger immédiat&nbsp;?</h2>
        <a class="num911" href="tel:911">911</a>
        <p>Appelez le 911 (police, ambulance). Si vous ne pouvez pas appeler, demandez à une personne de confiance de le faire pour vous.</p>
      </div>
      <div class="danger__col">
        <h3>Naviguez en toute sécurité</h3>
        <p>Si vous pensez que votre téléphone, votre ordinateur ou votre historique de navigation pourrait être surveillé, privilégiez, lorsque c'est possible, un appareil auquel cette personne n'a pas accès. Vous pouvez également effacer votre historique de navigation : appuyez sur ⋮ → Supprimer les données de navigation. Le bouton «&nbsp;Effacer l'historique&nbsp;», en haut de chaque page, donne les étapes pour votre appareil.</p>
        <p><a class="exit" href="{EXIT_URL}" rel="noreferrer" onclick="{EXIT_JS}">Quitter rapidement le site ✕</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-label="Message important">
  <div class="wrap stack">
    {ornament()}
    <p class="callout">Vous n'avez pas besoin d'attendre que la situation devienne grave pour demander de l'aide. Des ressources existent pour vous accompagner, quelle que soit votre situation : violence physique ou psychologique, contrôle, surveillance, menaces, isolement ou violence sexuelle. Vous pouvez également trouver du soutien si vous vous inquiétez pour une personne proche.</p>
    <div class="actions"><a class="btn" href="ressources.html">Voir les ressources par besoin</a><a class="btn" href="comprendre.html">Je ne sais pas par où commencer</a></div>
  </div>
</section>
'''
    else:
        b = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero__text">
      <h1>Looking for support?</h1>
      <p class="alone">You are not alone.</p>
      <p>Free and confidential resources are available for people experiencing domestic violence, control, threats, or any situation that makes them feel uncomfortable or unsafe.</p>
      <p>You can find help, at your own pace.</p>
      <div class="actions">
        <a class="btn btn--primary" href="ressources.html">Find a resource</a>
        <a class="btn" href="#parler">Talk to someone now</a>
        <a class="btn" href="#ecrire">I'd rather write</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-label="Immediate contact">
  <div class="wrap panels">
    <article class="panel" id="parler">
      <p class="eyebrow">By phone</p>
      <h2>Talk to someone now</h2>
      <a class="bignum" href="tel:18003639010">1 800 363-9010</a>
      <ul class="facts"><li>24/7</li><li>Free</li><li>Anonymous and confidential</li><li>English and French</li></ul>
      <p><strong>SOS violence conjugale.</strong> A worker will listen, help you assess your safety, and can call a shelter for you. You don't need to be sure it's violence to call.</p>
      <p class="small muted">Sexual violence: Sexual Violence Helpline (Info-aide violence sexuelle), <a href="tel:18889339007">1 888 933-9007</a>.</p>
    </article>
    <article class="panel" id="ecrire">
      <p class="eyebrow">In writing</p>
      <h2>I'd rather write</h2>
      <ul class="contacts">
        <li><span class="k">Text</span><a href="sms:4386011211">438 601-1211</a></li>
        <li><span class="k">Chat</span><a href="https://sosviolenceconjugale.ca/en" target="_blank" rel="noopener noreferrer">sosviolenceconjugale.ca</a></li>
        <li><span class="k">Email</span><a href="mailto:sos@sosviolenceconjugale.ca">sos@sosviolenceconjugale.ca</a></li>
      </ul>
      <p>The same free, confidential SOS violence conjugale service, in writing. The chat window opens when a worker is available.</p>
      <p class="small muted">If someone can read your messages, consider deleting the conversation afterwards.</p>
    </article>
  </div>
</section>

<section class="section" aria-labelledby="danger-titre">
  <div class="wrap">
    <div class="danger">
      <div class="danger__col">
        <h2 id="danger-titre">Are you in immediate danger?</h2>
        <a class="num911" href="tel:911">911</a>
        <p>Call 911 (police, ambulance). If you can't call, ask someone you trust to call for you.</p>
      </div>
      <div class="danger__col">
        <h3>Browse safely</h3>
        <p>If you think your phone, computer or browsing history may be monitored, use a device that person can't access whenever possible. You can also clear your browsing history: tap ⋮ → Delete browsing data. The “Clear browsing history” button at the top of every page shows the steps for your device.</p>
        <p><a class="exit" href="{EXIT_URL}" rel="noreferrer" onclick="{EXIT_JS}">Quickly leave this site ✕</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-label="Important message">
  <div class="wrap stack">
    {ornament()}
    <p class="callout">You don't have to wait until things get serious to ask for help. Resources exist to support you, whatever your situation: physical or psychological violence, control, monitoring, threats, isolation or sexual violence. You can also find support if you are worried about someone close to you.</p>
    <div class="actions"><a class="btn" href="ressources.html">See resources by need</a><a class="btn" href="comprendre.html">I don't know where to start</a></div>
  </div>
</section>
'''
    return page(lang, "index", T[lang]["site"], b)

def subnav(lang, cur):
    items = [("ressources", "Par besoin" if lang=="fr" else "By need"),
             ("regions", "Par région" if lang=="fr" else "By region"),
             ("repertoire", "Répertoire complet" if lang=="fr" else "Full directory"),
             ("comprendre", "Comprendre les ressources" if lang=="fr" else "Understanding resources")]
    return '<nav class="subnav" aria-label="' + ("Trouver une ressource" if lang=="fr" else "Find a resource") + '">' + "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s==cur else ""}>{E(l)}</a>' for s,l in items) + "</nav>"

def find_head(lang, cur, h1, lead):
    return f'''<section class="section" style="padding-bottom:1.5rem">
  <div class="wrap section__head" style="margin-bottom:0">
    <p class="eyebrow">{"Trouver une ressource" if lang=="fr" else "Find a resource"}</p>
    <h1>{E(h1)}</h1>
    <p class="lead prose">{lead}</p>
    {subnav(lang, cur)}
  </div>
</section>'''

def ressources(lang):
    fr = lang == "fr"
    tiles = "".join(f'<li><a class="tile" href="#{nid}">{E(lf if fr else le)}</a></li>' for nid, lf, le, *_ in NEEDS)
    tiles += f'<li><a class="tile tile--quiet" href="comprendre.html"><span>{"Je ne sais pas par où commencer" if fr else "I don&#39;t know where to start"}<small>{"Ce que fait chaque type de ressource" if fr else "What each type of resource does"}</small></span></a></li>'
    groups = []
    for nid, lf, le, inf, ine in NEEDS:
        rs = priority([r for r in R if nid in r["needs"]])
        groups.append(f'''<section class="group" id="{nid}" aria-labelledby="h-{nid}">
  <div class="group__head"><h2 id="h-{nid}">{E(lf if fr else le)}</h2><p class="muted">{E(inf if fr else ine)}</p></div>
  {cards(rs, lang)}
  <a class="back" href="#besoins">{T[lang]["back"]}</a>
</section>''')
    b = find_head(lang, "ressources",
        "Par besoin" if fr else "By need",
        "Les ressources ne sont pas toutes les mêmes. Trouvez le type de soutien qui correspond à votre situation." if fr else
        "Not all resources are the same. Find the kind of support that fits your situation.")
    b += f'''
<section class="section section--tint" id="besoins" style="padding-block:2rem">
  <div class="wrap"><h2 class="visually-hidden">{"Choisissez un besoin" if fr else "Choose a need"}</h2><ul class="tiles">{tiles}</ul></div>
</section>
<div class="wrap">{"".join(groups)}</div>'''
    return page(lang, "ressources", "Trouver une ressource" if fr else "Find a resource", b, section="ressources")

def regions(lang):
    fr = lang == "fr"
    toc = "".join(f'<li><a href="#{rid}">{E(lf if fr else le)}</a></li>' for rid, lf, le in REGIONS)
    groups = []
    for rid, lf, le in REGIONS:
        rs = priority([r for r in R if rid in r["regions"]])
        if rid == "province":
            intro = ("Ces lignes et services sont accessibles de partout au Québec, y compris dans les régions qui ne sont pas listées ici." if fr else
                     "These lines and services can be reached from anywhere in Québec, including regions not listed here.")
        elif rid in ("laval", "monteregie", "quebec"):
            intro = (f"Pour trouver une maison d'hébergement près de chez vous, appelez SOS violence conjugale au 1 800 363-9010 ou consultez la carte de la Fédération des maisons d'hébergement. Les <a href=\"#province\">ressources provinciales</a> desservent aussi cette région." if fr else
                     f"To find a shelter near you, call SOS violence conjugale at 1 800 363-9010 or use the Federation of Women's Shelters map. <a href=\"#province\">Province-wide resources</a> also serve this region.")
        else:
            intro = ("Ressources situées à Montréal. Les <a href=\"#province\">ressources provinciales</a> sont aussi accessibles." if fr else
                     "Resources located in Montréal. <a href=\"#province\">Province-wide resources</a> are also available.")
        body = cards(rs, lang) if rs else ""
        if not rs or rid in ("laval","monteregie","quebec"):
            extra = [r for r in R if r["id"] in ("sos","fmhf")]
            body += f'<p class="subhead">{"Pour commencer" if fr else "Where to start"}</p>' + cards(extra, lang)
        groups.append(f'''<section class="group" id="{rid}" aria-labelledby="h-{rid}">
  <div class="group__head"><h2 id="h-{rid}">{E(lf if fr else le)}</h2><p class="muted">{intro}</p></div>
  {body}
  <a class="back" href="#liste-regions">{T[lang]["back_r"]}</a>
</section>''')
    b = find_head(lang, "regions", "Par région" if fr else "By region",
        "Choisissez votre région. Les lignes d'écoute provinciales sont accessibles partout." if fr else
        "Choose your region. Province-wide support lines can be reached from anywhere.")
    b += f'''<section class="section section--tint" id="liste-regions" style="padding-block:1.5rem"><div class="wrap"><ul class="toc">{toc}</ul></div></section>
<div class="wrap">{"".join(groups)}</div>'''
    return page(lang, "regions", "Par région" if fr else "By region", b, section="ressources")

def repertoire(lang):
    fr = lang == "fr"
    toc = "".join(f'<li><a href="#{k}">{E(lf if fr else le)}</a></li>' for k, lf, le in KINDS)
    groups = []
    for k, lf, le in KINDS:
        rs = by_name([r for r in R if kind(r) == k])
        groups.append(f'''<section class="group" id="{k}" aria-labelledby="h-{k}">
  <div class="group__head"><h2 id="h-{k}">{E(lf if fr else le)}</h2><p class="muted">{len(rs)} {"ressources" if fr else "resources"}</p></div>
  {cards(rs, lang)}
</section>''')
    b = find_head(lang, "repertoire", "Répertoire complet" if fr else "Full directory",
        f"Les {len(R)} ressources du répertoire, classées par type." if fr else f"All {len(R)} resources in the directory, grouped by type.")
    b += f'''<section class="section section--tint" style="padding-block:1.5rem"><div class="wrap"><ul class="toc">{toc}</ul></div></section>
<div class="wrap">{"".join(groups)}</div>'''
    return page(lang, "repertoire", "Répertoire complet" if fr else "Full directory", b, section="ressources")

GLOSS = {
 "fr": [
  ("Une ligne d'écoute", "Un service téléphonique confidentiel pour parler à quelqu'un, poser des questions, ventiler et être orientée vers les bonnes ressources en toute sécurité. Souvent ouvert 24/7, parfois aussi par texto ou clavardage.", "ressources.html#ecoute"),
  ("Un centre de femmes", "Un lieu communautaire de jour qui offre de l'écoute, de l'accompagnement individuel, des activités et un réseau de soutien pour briser l'isolement. Vous n'avez pas besoin d'y habiter ni d'avoir quitté votre partenaire.", "ressources.html#psy"),
  ("Une maison d'hébergement de 1re étape (urgence)", "Un refuge sécuritaire accessible immédiatement, 24/7, pour les femmes et leurs enfants qui fuient la violence conjugale. Le séjour est de courte durée (quelques semaines), dans des espaces partagés. L'adresse reste confidentielle.", "ressources.html#hebergement"),
  ("Une maison d'hébergement de 2e étape (transition)", "Une ressource qui prend le relais après la 1re étape. Elle propose des appartements individuels et autonomes pour une durée allant jusqu'à 2 ans, afin de se reconstruire à l'abri du harcèlement post-séparation.", "ressources.html#hebergement"),
  ("Les services externes", "Plusieurs maisons d'hébergement offrent des rencontres, des suivis et des groupes à des femmes qui n'y habitent pas. Vous pouvez donc recevoir leur aide en restant chez vous.", "ressources.html#psy"),
  ("Une ressource juridique", "De l'information et des conseils gratuits sur vos droits et les démarches possibles : plainte, ordonnance de protection, séparation, garde des enfants. Consulter ne vous oblige à rien, ni à porter plainte.", "ressources.html#juridique"),
  ("Un CAVAC", "Les Centres d'aide aux victimes d'actes criminels offrent du soutien psychologique et de l'information sur le processus judiciaire, que vous ayez porté plainte ou non.", "ressources.html#juridique"),
  ("L'IVAC", "Le programme d'indemnisation des victimes d'actes criminels peut couvrir certains frais, comme une thérapie ou une perte de revenu. Une plainte à la police n'est pas obligatoire pour faire une demande.", "ressources.html#base"),
  ("Une ressource en violence sexuelle", "Un service spécialisé qui accueille, croit et accompagne les personnes touchées par la violence sexuelle, récente ou passée, dans le respect de leurs choix.", "ressources.html#sexuelle"),
 ],
 "en": [
  ("A support line", "A confidential phone service to talk to someone, ask questions, vent and be safely pointed to the right resources. Often open 24/7, sometimes also by text or chat.", "ressources.html#ecoute"),
  ("A women's centre", "A daytime community space offering listening, one-on-one support, activities and a support network to break isolation. You don't need to live there or to have left your partner.", "ressources.html#psy"),
  ("A first-stage (emergency) shelter", "A safe place available immediately, 24/7, for women and their children fleeing domestic violence. Stays are short (a few weeks) in shared spaces. The address is kept confidential.", "ressources.html#hebergement"),
  ("A second-stage (transition) shelter", "Takes over after a first-stage shelter. It offers individual, self-contained apartments for up to 2 years, to rebuild safely away from post-separation harassment.", "ressources.html#hebergement"),
  ("Outreach services", "Many shelters offer meetings, follow-up and groups to women who don't live there. You can get their help while staying at home.", "ressources.html#psy"),
  ("A legal resource", "Free information and advice about your rights and options: complaints, protection orders, separation, child custody. Contacting them does not commit you to anything, including filing a complaint.", "ressources.html#juridique"),
  ("A CAVAC", "Crime Victims Assistance Centres offer emotional support and information about the court process, whether or not you have filed a complaint.", "ressources.html#juridique"),
  ("IVAC", "Québec's crime victims compensation program can cover some costs, such as therapy or lost income. A police report is not required to apply.", "ressources.html#base"),
  ("A sexual violence resource", "A specialized service that welcomes, believes and supports people affected by sexual violence, recent or past, while respecting their choices.", "ressources.html#sexuelle"),
 ],
}

def comprendre(lang):
    fr = lang == "fr"
    items = "".join(f'<div><dt>{E(a)}</dt><dd><p>{E(b)}</p><p><a href="{l}">{"Voir ces ressources" if fr else "See these resources"} →</a></p></dd></div>' for a, b, l in GLOSS[lang])
    even = (["vous n'êtes pas certaine de qualifier la situation de violence ;", "vous ne voulez pas quitter votre partenaire ;", "vous voulez simplement parler à quelqu'un ;", "vous cherchez de l'information pour une proche."] if fr else
            ["you're not sure the situation counts as violence;", "you don't want to leave your partner;", "you just want to talk to someone;", "you're looking for information for someone close to you."])
    b = find_head(lang, "comprendre", "Comprendre les ressources" if fr else "Understanding resources",
        "Il n'est pas nécessaire de savoir exactement ce dont vous avez besoin avant de contacter une ressource. Une ligne d'écoute peut vous orienter." if fr else
        "You don't need to know exactly what you need before contacting a resource. A support line can guide you.")
    b += f'''
<section class="section" style="padding-top:1rem">
  <div class="wrap">
    <h2 style="font-size:var(--step-2);margin-bottom:.5rem">{"Quelle est la différence entre…" if fr else "What's the difference between…"}</h2>
    <dl class="glossary">{items}</dl>
  </div>
</section>
<section class="section section--tint">
  <div class="wrap two">
    <div class="stack">
      {ornament()}
      <h2>{"Vous pouvez demander de l'aide même si…" if fr else "You can ask for help even if…"}</h2>
    </div>
    <div class="stack">
      <ul class="checklist">{"".join(f"<li>{E(x)}</li>" for x in even)}</ul>
      <div class="actions"><a class="btn btn--primary" href="index.html#parler">{"Parler à quelqu'un maintenant" if fr else "Talk to someone now"}</a></div>
    </div>
  </div>
</section>'''
    return page(lang, "comprendre", "Comprendre les ressources" if fr else "Understanding resources", b, section="comprendre")

def apropos(lang):
    fr = lang == "fr"
    team = [("Yasmine Amrouche","Étudiante en médecine, fondatrice","Medical student, founder"),
            ("Denisse Dan","Étudiante en médecine","Medical student"),
            ("Daniel Palladino","Étudiant en médecine et pharmacien","Medical student and pharmacist"),
            ("Malika Djouamaa","Étudiante en médecine et pharmacienne","Medical student and pharmacist"),
            ("Imed Chafi","Pharmacien","Pharmacist")]
    team_html = "".join(f"<li><strong>{E(n)}</strong><span>{E(f if fr else e)}</span></li>" for n, f, e in team)
    if fr:
        b = f'''
<section class="section">
  <div class="wrap two">
    <div class="stack">
      <img class="about__logo" src="img/logo.png" alt="Logo À portée de main – Within Reach : une main qui tient une fleur de lotus" width="240" height="240">
      <p class="eyebrow">À propos</p>
      <h1>Le projet</h1>
      {ornament()}
      <p class="slogan" style="font-size:var(--step-1)">Les ressources existent. Nous les rendons visibles.</p>
    </div>
    <div class="stack prose">
      <p>De nombreuses ressources spécialisées en violence conjugale existent au Québec. Pourtant, elles ne sont pas toujours connues des personnes qui pourraient en bénéficier, particulièrement lorsque demander de l'aide est difficile ou comporte des risques.</p>
      <p><strong>À portée de main</strong> vise à réduire cette barrière en rendant les ressources existantes visibles dans les espaces du quotidien.</p>
      <ul class="bullets">
        <li>Des affiches installées dans divers milieux publics, comme les toilettes pour femmes</li>
        <li>Un site qui centralise les ressources</li>
        <li>Un code QR qui donne accès au répertoire</li>
        <li>Une collaboration avec des organismes communautaires et des intervenantes</li>
      </ul>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="wrap two">
    <div class="stack"><h2>L'équipe</h2><ul class="team">{team_html}</ul></div>
    <div class="stack"><h2>Les partenaires</h2>
      <ul class="team">
        <li><strong>AMC-Qc</strong><span>Merci pour leur soutien et le financement des affiches.</span></li>
        <li><strong>Halte-Femmes de Montréal-Nord</strong><span>Merci à l'équipe et à leurs intervenantes pour leur précieuse collaboration au projet.</span></li>
      </ul>
    </div>
  </div>
</section>
<section class="section" id="contact">
  <div class="wrap stack prose">
    <h2>Collaborer avec nous</h2>
    <p>Vous êtes un organisme, une intervenante ou un milieu qui souhaite afficher nos affiches ? Écrivez-nous.</p>
    <ul class="contacts">
      <li><span class="k">Courriel</span><a href="mailto:aporteedemain.withinreach@gmail.com">aporteedemain.withinreach@gmail.com</a></li>
      <li><span class="k">Instagram</span><a href="https://www.instagram.com/within_reach.ca/" target="_blank" rel="noopener noreferrer">@within_reach.ca</a> <span class="x">(message direct)</span></li>
    </ul>
    <p class="small muted">Cette adresse n'est pas un service d'aide. Pour parler à quelqu'un, appelez SOS violence conjugale au 1 800 363-9010, ou le 911 en cas d'urgence.</p>
  </div>
</section>'''
    else:
        b = f'''
<section class="section">
  <div class="wrap two">
    <div class="stack">
      <img class="about__logo" src="../img/logo.png" alt="À portée de main – Within Reach logo: a hand holding a lotus flower" width="240" height="240">
      <p class="eyebrow">About</p>
      <h1>The project</h1>
      {ornament()}
      <p class="slogan" style="font-size:var(--step-1)">The resources exist. We make them visible.</p>
    </div>
    <div class="stack prose">
      <p>Many specialized domestic violence resources exist in Québec. Yet they are not always known to the people who could benefit from them, especially when asking for help is difficult or risky.</p>
      <p><strong>Within Reach</strong> aims to lower this barrier by making existing resources visible in everyday spaces.</p>
      <ul class="bullets">
        <li>Posters placed in public spaces, such as women's washrooms</li>
        <li>A website that brings the resources together</li>
        <li>A QR code that opens the directory</li>
        <li>A collaboration with community organizations and support workers</li>
      </ul>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="wrap two">
    <div class="stack"><h2>The team</h2><ul class="team">{team_html}</ul></div>
    <div class="stack"><h2>Partners</h2>
      <ul class="team">
        <li><strong>AMC-Qc</strong><span>Thank you for your support and for funding the posters.</span></li>
        <li><strong>Halte-Femmes de Montréal-Nord</strong><span>Thank you to the team and its support workers for their valuable collaboration.</span></li>
      </ul>
    </div>
  </div>
</section>
<section class="section" id="contact">
  <div class="wrap stack prose">
    <h2>Work with us</h2>
    <p>Are you an organization, a support worker or a venue that would like to display our posters? Write to us.</p>
    <ul class="contacts">
      <li><span class="k">Email</span><a href="mailto:aporteedemain.withinreach@gmail.com">aporteedemain.withinreach@gmail.com</a></li>
      <li><span class="k">Instagram</span><a href="https://www.instagram.com/within_reach.ca/" target="_blank" rel="noopener noreferrer">@within_reach.ca</a> <span class="x">(direct message)</span></li>
    </ul>
    <p class="small muted">This address is not a help service. To talk to someone, call SOS violence conjugale at 1 800 363-9010, or 911 in an emergency.</p>
  </div>
</section>'''
    return page(lang, "a-propos", "À propos" if fr else "About", b)

def main():
    os.makedirs(OUT + "/en", exist_ok=True)
    for lang in ("fr", "en"):
        d = OUT if lang == "fr" else OUT + "/en"
        for slug, fn in [("index", home), ("ressources", ressources), ("regions", regions), ("repertoire", repertoire), ("comprendre", comprendre), ("a-propos", apropos)]:
            with open(f"{d}/{slug}.html", "w", encoding="utf-8") as f:
                f.write(fn(lang))
    print("ok", len(R), "resources")

main()
