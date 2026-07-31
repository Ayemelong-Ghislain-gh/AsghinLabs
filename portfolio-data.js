/* =====================================================================
   PORTFOLIO SAMPLES — EDIT THIS FILE TO ADD YOUR OWN WORK
   =====================================================================
   HOW TO ADD A NEW SAMPLE (2 steps, no other code needs to change):

   1. Drop your image file into the matching folder next to index.html:
        images/portfolio/logos/             → Logo Design
        images/portfolio/flyers/            → Flyer Design
        images/portfolio/brand-guidelines/  → Brand Guidelines
        images/portfolio/instagram/         → Instagram Posts
        images/portfolio/banners/           → Banners
        images/portfolio/ad-creatives/      → Ad Creatives

   2. Add one line to the matching array below:
        { src: "images/portfolio/logos/your-file.jpg", title: "Client / project name" }

   The gallery, tabs, and lightbox all update automatically.

   -----------------------------------------------------------------
   GROUPS: each category belongs to a "group" — this controls which
   tabs show up depending on which service card the visitor clicked.
     group: "brand"   → shown when linked from "Brand Identity Packages"
     group: "social"  → shown when linked from "Social Media Graphics"
   Want a whole new group (e.g. for "UI/UX Design")? Add categories
   with a new group name, then link to portfolio.html?group=yourgroup
   ===================================================================== */

const PORTFOLIO_ITEMS = {
  logo: [
    { src: "images/portfolio/logos/asghinlabs.jpeg", title: "AsghinLabs" },
    { src: "images/portfolio/logos/DebbiesCloset.JPEG", title: "Debbie's Closet" },
    { src: "images/portfolio/logos/FlassyImport.JPEG", title: "Flassy Import" },
    { src: "images/portfolio/logos/MMLuxe.JPEG", title: "MM Luxe" },
    { src: "images/portfolio/logos/WildaluxCosmetics.JPEG", title: "Wildalux Cosmetics" },
    { src: "images/portfolio/logos/YoungDevAfrica.JPEG", title: "Young Dev Africa" },
  ],

  flyer: [
    { src: "images/portfolio/flyers/EasyGas.JPEG", title: "Easy Gas" },
    { src: "images/portfolio/flyers/SupremeLaundry.JPEG", title: "Supreme Laundry" },
    { src: "images/portfolio/flyers/Tralopro.JPEG", title: "Tralopro" },
    { src: "images/portfolio/flyers/YokoSuperMarket.JPEG", title: "Yoko Super Market" },
    { src: "images/portfolio/flyers/YourHealthYourWealth.JPEG", title: "Your Health Your Wealth" },
  ],

  brandguidelines: [
    // { src: "images/portfolio/brand-guidelines/example.jpg", title: "Example Brand Guide" },
  ],

  instagram: [
    // { src: "images/portfolio/instagram/example.jpg", title: "Example Instagram Post" },
  ],

  banner: [
    { src: "images/portfolio/banners/HarrietsShopping.JPEG", title: "Harriet's Shopping" },
  ],

  adcreatives: [
    // { src: "images/portfolio/ad-creatives/example.jpg", title: "Example Ad Creative" },
  ],
};

// id must match a key in PORTFOLIO_ITEMS above. group controls which
// service card's "View Portfolio" link shows this tab.
const PORTFOLIO_CATEGORIES = [
  { id: "logo", label: "🎯 Logo Design", group: "brand" },
  { id: "flyer", label: "📰 Flyer Design", group: "brand" },
  { id: "brandguidelines", label: "📘 Brand Guidelines", group: "brand" },

  { id: "instagram", label: "📸 Instagram Posts", group: "social" },
  { id: "banner", label: "🖼️ Banners", group: "social" },
  { id: "adcreatives", label: "📢 Ad Creatives", group: "social" },
];

// Optional page-header text per group (falls back to a generic header)
const PORTFOLIO_GROUP_INFO = {
  brand: {
    title: "🎨 Brand Identity Portfolio",
    sub: "Logos, brand guidelines, and flyer work. Tap a category, then tap any sample for a closer look.",
  },
  social: {
    title: "📱 Social Media Graphics Portfolio",
    sub: "Instagram posts, banners, and ad creatives. Tap a category, then tap any sample for a closer look.",
  },
};
