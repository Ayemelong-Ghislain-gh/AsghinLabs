/* =====================================================================
   ACADÉMIE — SOUS-SYSTÈME FRANCOPHONE (academie.html)
   Modifiez ce fichier pour ajouter des fiches, des sujets et des cahiers
   pour le sous-système francophone. La page se reconstruit toute seule.
   Les mêmes règles que academy-data.js s'appliquent (voir ce fichier).
   ===================================================================== */

// Numéro WhatsApp qui reçoit les commandes et les inscriptions
const ACADEMY_WHATSAPP = "237682402876";

/* ---------------------------------------------------------------------
   FICHES DE COURS ET SUJETS (PDF lisibles en ligne)
   1. Placez le PDF dans files/academie/fiches/ (ou files/academie/sujets/)
   2. Ajoutez une ligne ci-dessous. "level" : 6e, 5e, 4e, 3e, Seconde,
      Première, Terminale, BEPC, Probatoire ou Baccalauréat.
   Exemple :
   { file: "files/academie/fiches/informatique-3e.pdf", cover: "images/academie/fiches/informatique-3e.jpg",
     title: "Informatique — Fiches de révision", subject: "Informatique", level: "3e", pages: 40, size: "1,2 Mo" },
   --------------------------------------------------------------------- */
const ACADEMY_NOTES = [];

const ACADEMY_PAST_QUESTIONS = [];

/* ---------------------------------------------------------------------
   CAHIERS D'EXERCICES (boutique)
   Vide pour l'instant : la page affiche « Cahiers en préparation » avec
   un bouton « Me prévenir ». Pour ajouter un cahier, copiez ce modèle :
   { id: "info-3e", subject: "Informatique", level: "3e", title: "Cahier de 3e",
     stage: "Premier cycle · Préparation au BEPC", price: 2500,
     cover: "images/academie/cahiers/info-3e.jpg", status: "available" },
   (status: "preorder" affiche un badge « Précommande »)
   --------------------------------------------------------------------- */
const ACADEMY_WORKBOOKS = [];

/* ---------------------------------------------------------------------
   RESSOURCES OFFICIELLES (sous-système francophone)
   Liens vers les sites du Ministère des Enseignements Secondaires.
   --------------------------------------------------------------------- */
const MINESEC_PAPERS = "https://minesec-distance.schoolfaqs.net/revision";
const ACADEMY_OFFICIAL = {
  papers: [
    // Ces cartes ouvrent notre propre bibliothèque (/epreuves), classée par année et par matière.
    { kind: "Premier cycle · 3e", title: "Épreuves du BEPC", desc: "105 épreuves officielles, 2017–2023, toutes matières.", url: "/epreuves#bepc", cta: "Voir les épreuves →" },
    { kind: "Premier cycle · 3e", title: "BEPC blanc", desc: "15 épreuves d'entraînement, 2018–2025.", url: "/epreuves#bepc-blanc", cta: "Voir les épreuves →" },
    { kind: "Second cycle · Première", title: "Probatoire · examens blancs", desc: "40 épreuves blanches, 2017–2025.", url: "/epreuves#probatoire-examen-blanc", cta: "Voir les épreuves →" },
    { kind: "Second cycle · Terminale", title: "Baccalauréat · examens blancs", desc: "29 épreuves blanches, 2017–2025.", url: "/epreuves#baccalaureat-blanc", cta: "Voir les épreuves →" },
  ],
  progressions: [
    { kind: "MINESEC · 2026-27", title: "Progressions officielles", desc: "Choisissez « Sous-système francophone », puis votre classe et votre matière, pour voir les leçons de l'année trimestre par trimestre.", url: "https://minesec-ige.com/progression-sheets", cta: "Trouver ma progression ↗" },
  ],
};
