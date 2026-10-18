#!/usr/bin/env node
/*
  Génère un code QR (SVG) par lieu d'affichage.
  Chaque code mène à  <BASE>/q/<lieu>  qui redirige vers l'accueil avec ?src=<lieu>
  (voir le fichier _redirects). GoatCounter compte ainsi les scans par lieu.

  Utilisation :
    node _outils/qr.js                         -> lit _outils/lieux.txt (un lieu par ligne)
    node _outils/qr.js hopital-x cafe-y        -> lieux donnés directement
    BASE=https://nouveaudomaine.ca node _outils/qr.js   -> autre adresse du site

  Les fichiers sont créés dans _outils/qr/ : <lieu>.svg, plus planche.html (tous les codes, pour vérifier).
*/
const fs = require("fs");
const path = require("path");
const QRCode = require("./qrcode-vendor");
const ECL = require("./qrcode-vendor/QRErrorCorrectLevel");

const BASE = (process.env.BASE || "https://aporteedemain.netlify.app").replace(/\/+$/, "");
const OUT = path.join(__dirname, "qr");

function slug(s) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function svgFor(text) {
  const qr = new QRCode(-1, ECL.H); // niveau H : reste lisible même si l'affiche est un peu abîmée
  qr.addData(text);
  qr.make();
  const n = qr.getModuleCount(), q = 4, size = n + q * 2;
  let d = "";
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (qr.isDark(r, c)) d += `M${c + q},${r + q}h1v1h-1z`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges">` +
    `<rect width="${size}" height="${size}" fill="#fff"/><path fill="#12245a" d="${d}"/></svg>\n`;
}

let lieux = process.argv.slice(2);
if (!lieux.length) {
  const f = path.join(__dirname, "lieux.txt");
  if (!fs.existsSync(f)) { console.error("Aucun lieu : ajoutez-les dans _outils/lieux.txt ou en arguments."); process.exit(1); }
  lieux = fs.readFileSync(f, "utf8").split(/\r?\n/).map(l => l.replace(/#.*/, "").trim()).filter(Boolean);
}

fs.mkdirSync(OUT, { recursive: true });
const rows = [];
for (const lieu of lieux) {
  const s = slug(lieu);
  const url = `${BASE}/q/${s}`;
  const svg = svgFor(url);
  fs.writeFileSync(path.join(OUT, `${s}.svg`), svg);
  rows.push(`<figure>${svg}<figcaption><b>${lieu}</b><br>${url}</figcaption></figure>`);
  console.log(`${s}.svg  ->  ${url}`);
}
fs.writeFileSync(path.join(OUT, "planche.html"),
  `<!doctype html><meta charset="utf-8"><title>Codes QR</title><style>body{font-family:sans-serif;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:24px;padding:24px}figure{margin:0;text-align:center}svg{width:200px;height:200px}figcaption{font-size:12px;word-break:break-all}</style>${rows.join("")}`);
