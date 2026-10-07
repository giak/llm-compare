# Modèle — Éditeur

<!-- Bloc machine : inséré et réécrit par moteur/engine.py (`migrate` puis `render`).
     Le prix ci-dessous vient de moteur/state/<plateforme>.json : ne pas l'écrire à la main. -->
<!-- GEN:prix|run=AAAA-MM-JJ -->
**Sur Freebuff :** …
<!-- /GEN -->

## Identité

*(nom, éditeur, identifiants, fenêtre de contexte, modalités, date d'apparition — source primière)*

## Puissance — AA Intelligence Index v4.3.2

*(recommandé — chiffres AA avec version d'index, estimation/effort notés ; `n.d.` si non mesuré)*

## Analyse de problèmes

*(recommandé — comportement observé, écueis, fiabilité)*

## Vitesse

*(recommandé — tok/s, latence E2E, source et date)*

## Coût

*(recommandé — prix structuré, historique daté, promotion et échéance si connue)*

## Français

*(qualité de la langue, tests locaux, limites)*

## Avantages

*(puces factuelles, chaque avantage rattaché à une source)*

## Inconvénients

*(puces factuelles — y compris les prévisions contredites par les faits)*

## Verdict pour ton budget

*(recommandé — verdict daté, recalculé si le prix a bougé)*

## Sources

*(numérotées, tier 1/2/3, URL, date de lecture)*

---

**Contrat de fiche (moteur `lint`) :**
- H1 obligatoire, format `# <Nom du modèle> — <Éditeur>` : le segment avant ` — ` doit
  slugsifier en l'`id` de `moteur/state/<plateforme>.json`.
- Sections **exigées** (ordre imposé) : `Identité`, `Français`, `Avantages`,
  `Inconvénients`, `Sources`.
- Sections **recommandées** (non bloquantes, signalées par `lint`) : `Puissance`,
  `Analyse de problèmes`, `Vitesse`, `Coût`, `Verdict`.
- Le bloc `GEN:prix` est machine-owned ; toute prose autour est humaine
  (« annoter, jamais effacer »).
