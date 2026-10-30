# parfumbyya — demo website

Een snelle, statische one-pager voor **parfumbyya.nl**: klanten bekijken de collectie,
vullen een mandje en sturen hun bestelling met één klik door naar WhatsApp.

Geen framework, geen build-stap: gewoon HTML, CSS en JavaScript. Direct te hosten
op GitHub Pages (of elke andere statische host).

```
parfumbyya/
├── index.html
├── .nojekyll
├── assets/
│   ├── css/styles.css
│   ├── js/
│   │   ├── config.js      ← hier pas je het WhatsApp-nummer aan
│   │   ├── products.js    ← hier pas je de collectie aan
│   │   └── app.js         ← interactie (mandje, filters, modal)
│   └── img/               ← flacon-illustraties (SVG)
├── tools/generate-images.py  (optioneel: maakt de SVG's opnieuw)
└── README.md
```

---

## 1. Lokaal bekijken

```bash
cd parfumbyya
python3 -m http.server 8000
```

Open <http://localhost:8000>. Dubbelklikken op `index.html` werkt ook.

---

## 2. Naar GitHub Pages zetten

1. Maak een repository, bijvoorbeeld `parfumbyya`.
2. Upload **de inhoud** van deze map (niet de map zelf) naar de `main`-branch.
3. Ga in GitHub naar **Settings → Pages**.
4. Kies bij *Source*: **Deploy from a branch** → branch `main`, map `/ (root)` → **Save**.
5. Na een minuut staat de site op `https://<gebruikersnaam>.github.io/parfumbyya/`.

### Eigen domein (parfumbyya.nl)

1. Zet in **Settings → Pages → Custom domain** `parfumbyya.nl` en sla op.
2. Maak bij je domeinregistrar deze DNS-records:

   | Type  | Naam | Waarde |
   |-------|------|--------|
   | A     | @    | 185.199.108.153 |
   | A     | @    | 185.199.109.153 |
   | A     | @    | 185.199.110.153 |
   | A     | @    | 185.199.111.153 |
   | CNAME | www  | `<gebruikersnaam>.github.io` |

3. Vink **Enforce HTTPS** aan zodra het certificaat klaar is.

---

## 3. Het WhatsApp-nummer instellen

Open `assets/js/config.js`:

```js
const CONFIG = {
  whatsapp: "31612345678",   // ← internationaal, zonder + of spaties
  ...
};
```

**Nu staat er een voorbeeldnummer in.** Vervang het door het echte nummer van je neef
en alle knoppen, de footer en de bestelberichten gebruiken meteen het juiste nummer.

Controleer het nummer even door `https://wa.me/31612345678` in je browser te openen:
je moet dan in WhatsApp bij het juiste contact uitkomen.

In hetzelfde bestand stel je ook in:

- `shippingCost` — verzendkosten (nu €4,95)
- `freeShippingFrom` — vanaf welk bedrag gratis verzending (nu €40)
- `email`, `instagram` — contactgegevens

---

## 4. Producten aanpassen

Alles staat in `assets/js/products.js`. Eén blok per geur:

```js
{
  id: "noir-ambre",                 // uniek, ook de bestandsnaam van de afbeelding
  name: "Noir Ambré",
  family: "Amber · Houtig",         // korte regel onder de naam
  gender: "unisex",                 // unisex | dames | heren
  badge: "Bestseller",              // "Bestseller", "Nieuw" of ""
  img: "assets/img/noir-ambre.svg",
  desc: "Warme, donkere geur met ...",
  notes: { top: "...", heart: "...", base: "..." },
  sizes: [ { ml: 50, price: 34.95 }, { ml: 100, price: 54.95 } ],
}
```

### Eigen foto's gebruiken

1. Zet je foto in `assets/img/` (bijv. `noir-ambre.jpg`), liefst staand (4:5) en
   maximaal ~1200 px breed.
2. Zet `img: "assets/img/noir-ambre.jpg"` in `products.js`.

De flacon-illustraties die er nu staan zijn zelf gegenereerd (zie
`tools/generate-images.py`) en mogen vrij gebruikt worden. Wil je ze opnieuw maken
in andere kleuren:

```bash
python3 tools/generate-images.py
```

---

## 5. Hoe bestellen werkt

1. Klant klikt op **+** of opent een geur → kiest 50 of 100 ml.
2. Mandje opent (rechts in beeld). Items worden bewaard in de browser (localStorage).
3. **Bestel via WhatsApp** opent `wa.me` met dit bericht, al ingevuld:

   ```
   Hoi! Ik wil graag bestellen bij parfumbyya:

   • Noir Ambré — 50 ml × 1 — €34,95

   Subtotaal: €34,95
   Verzending: €4,95
   Totaal: €39,90

   Mijn gegevens:
   Naam:
   Adres:
   Postcode + plaats:

   Ik hoor graag hoe ik kan betalen.
   ```

4. De klant drukt zelf op verzenden, jij bevestigt en stuurt een betaallink.

Er is dus **geen** betaalsysteem, account of database nodig — precies genoeg voor een
demo en voor de eerste verkoop.

---

## 6. Nog aanpassen voor livegang

- [ ] Echt WhatsApp-nummer in `assets/js/config.js`
- [ ] Echte producten, prijzen en foto's in `assets/js/products.js` + `assets/img/`
- [ ] KvK- en BTW-nummer in de footer (`index.html`, onderaan)
- [ ] E-mailadres en Instagram-link
- [ ] Reviews zijn voorbeelden — vervang door echte klantreviews of haal ze weg
- [ ] Voorraad/levertijd in de teksten controleren
- [ ] `demo-note` in de footer weghalen als de site live gaat

---

## Technisch

- Semantische HTML, skip-link, toetsenbordnavigatie, focus-trap in modal en mandje
- `prefers-reduced-motion` wordt gerespecteerd
- Geen tracking, geen cookies, geen externe scripts behalve Google Fonts
- Afbeeldingen zijn SVG (scherp op elk scherm, klein bestand)
