# À portée de main / Within Reach — instructions pour Claude

## Le projet
Initiative bénévole d'étudiant·e·s en médecine et de pharmacien·ne·s au Québec. Des affiches avec un code QR
sont posées dans des lieux publics (par exemple les toilettes pour femmes) et mènent à ce site, qui répertorie
les ressources pour les femmes vivant de la violence conjugale. Slogan : « Les ressources existent. Nous les
rendons visibles. »

Site en ligne : https://aporteedemain.netlify.app (Netlify, publié automatiquement à chaque push sur `main`).
Contact du projet : aporteedemain.withinreach@gmail.com · Instagram @within_reach.ca

L'équipe n'est pas technique : explique les changements en français simple, sans jargon.

## Comment le site est construit
- Site statique en HTML + CSS pur (aucun framework, aucune étape de build côté Netlify).
- **Ne modifie pas les fichiers .html à la main.** Ils sont générés par `_outils/build.py` :
  - `_outils/data.py` : toutes les ressources (nom, site, téléphones, régions, besoins, descriptions FR et EN),
    la liste des besoins (`NEEDS`), des régions (`REGIONS`) et des types (`KINDS`).
  - `_outils/build.py` : gabarits et textes de toutes les pages, en français et en anglais.
  - Après une modification : `python3 _outils/build.py`, puis commit et push de tout (sources + .html).
- Un seul petit script (constante `SCRIPT` dans `build.py`) détecte l'appareil pour afficher d'abord les bonnes
  étapes « Effacer l'historique ». Sans JavaScript, toutes les étapes restent visibles : garder ce comportement.
- `style.css` est écrit à la main (pas généré). Couleurs en variables CSS, mode sombre inclus.
- Pages : `index`, `ressources` (par besoin), `regions`, `repertoire`, `comprendre`, `a-propos`.
  Les mêmes pages existent en anglais dans `en/`. Toute modification de texte doit être faite dans les deux langues.

## Mesure de l'impact (projet de recherche)
- Statistiques anonymes avec **GoatCounter** (compte `aporteedemain`, tableau de bord : https://aporteedemain.goatcounter.com).
  Aucun cookie, aucune donnée personnelle. Ne jamais ajouter Google Analytics, pixel Meta ou autre traceur.
- Les clics comptés portent l'attribut `data-goatcounter-click="..."` (téléphones `tel-<id>`, textos, courriels,
  sites `site-<id>`, besoins `besoin-<id>`, régions, langue). « Quitter rapidement » et l'ouverture de
  « Effacer l'historique » sont comptés par script. Garder ces attributs quand on modifie les gabarits.
- Chaque affiche a un code QR unique vers `/q/<lieu>` ; `_redirects` renvoie vers `/?src=<lieu>`.
  Lieux dans `_outils/lieux.txt`, codes générés par `node _outils/qr.js` (variable `BASE` si le domaine change)
  dans `_outils/qr/`.

## Règles à respecter
- **Sécurité des utilisatrices avant tout.** Garder sur chaque page la barre du haut : 911, « Effacer l'historique »
  (instructions) et « Quitter rapidement » (vers google.com avec `location.replace`).
- **Jamais d'adresse de maison d'hébergement** : elles sont confidentielles. Téléphone et site web seulement.
- Les ressources et numéros doivent venir d'une source officielle (site de l'organisme) et être validés par
  l'équipe. N'invente jamais un numéro ; si tu en ajoutes un, dis-le clairement pour qu'il soit vérifié.
- Le badge « 24/7 » (`h24=True`) seulement si l'organisme l'indique lui-même.
- Le site doit rester lisible sur téléphone (la plupart des visites viennent du code QR).
- Ton : chaleureux, simple, non culpabilisant, au féminin (« Vous n'êtes pas seule »).

## Vérifier avant de publier
- Rebâtir, puis vérifier qu'aucun lien interne n'est brisé et que les pages ne débordent pas à 390 px de large
  (Playwright/Chromium est disponible dans l'environnement de Claude).
- Après le push, si le connecteur Netlify est disponible, confirmer que le déploiement du projet
  `aporteedemain` est à l'état « ready ».
