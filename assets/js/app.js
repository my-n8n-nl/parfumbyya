/* =========================================================================
   parfumbyya — interactie
   Geen frameworks, geen build-stap. Werkt direct op GitHub Pages.
   ========================================================================= */
(() => {
  "use strict";

  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

  const money = (n) =>
    "€" + n.toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  /* ------------------------------------------------------------ WhatsApp */
  const waLink = (text) =>
    `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(text)}`;

  function applyWaLinks() {
    $$("[data-wa-link]").forEach((el) => {
      const text = el.dataset.waText || CONFIG.greeting;
      el.href = waLink(text);
      el.target = "_blank";
      el.rel = "noopener";
    });
    const tel = $$(".footer-col a").find((a) => a.textContent.includes("+31"));
    if (tel) tel.textContent = "WhatsApp: " + formatPhone(CONFIG.whatsapp);
  }

  function formatPhone(digits) {
    const d = String(digits);
    if (d.startsWith("31") && d.length === 11) {
      return `+31 ${d[2]} ${d.slice(3, 5)} ${d.slice(5, 7)} ${d.slice(7, 9)} ${d.slice(9)}`;
    }
    return "+" + d;
  }

  /* -------------------------------------------------------------- catalogus */
  const grid = $("#productGrid");
  const emptyState = $("#emptyState");
  let activeFilter = "alles";

  function productCard(p) {
    const from = Math.min(...p.sizes.map((s) => s.price));
    return `
      <article class="card" data-id="${p.id}">
        <button class="card-media" data-open="${p.id}" aria-label="Snel bekijken: ${p.name}">
          <img src="${p.img}" alt="" width="1000" height="1250" loading="lazy">
          ${p.badge ? `<span class="card-badge">${p.badge}</span>` : ""}
          <span class="card-quick">Snel bekijken</span>
        </button>
        <div class="card-body">
          <div class="card-info">
            <h3 class="card-title">${p.name}</h3>
            <p class="card-notes">${p.family}</p>
          </div>
          <div class="card-price">${money(from)}</div>
        </div>
        <div class="card-foot">
          <span class="card-size">vanaf ${p.sizes[0].ml} ml</span>
          <button class="card-add" data-add="${p.id}" aria-label="${p.name} in mandje">
            <svg class="icon" aria-hidden="true"><use href="#i-plus"/></svg>
          </button>
        </div>
      </article>`;
  }

  function renderGrid() {
    const list = PRODUCTS.filter((p) => {
      if (activeFilter === "alles") return true;
      if (activeFilter === "nieuw") return p.badge.toLowerCase() === "nieuw";
      return p.gender === activeFilter;
    });
    grid.innerHTML = list.map(productCard).join("");
    emptyState.hidden = list.length > 0;
    grid.querySelectorAll(".card").forEach((el, i) => {
      el.classList.add("reveal");
      el.style.transitionDelay = Math.min(i * 45, 260) + "ms";
      revealObserver.observe(el);
    });
  }

  /* --------------------------------------------------------------- mandje */
  const STORE_KEY = "parfumbyya-bag-v1";
  let bag = loadBag();

  function loadBag() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || "[]");
      return Array.isArray(raw) ? raw.filter((i) => i && i.id && i.ml) : [];
    } catch {
      return [];
    }
  }
  function saveBag() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(bag)); } catch {}
  }
  const findProduct = (id) => PRODUCTS.find((p) => p.id === id);
  const sizeOf = (p, ml) => p.sizes.find((s) => s.ml === Number(ml)) || p.sizes[0];
  const bagCount = () => bag.reduce((n, i) => n + i.qty, 0);
  const bagSubtotal = () =>
    bag.reduce((n, i) => {
      const p = findProduct(i.id);
      return p ? n + sizeOf(p, i.ml).price * i.qty : n;
    }, 0);
  const shippingFor = (subtotal) =>
    subtotal === 0 || subtotal >= CONFIG.freeShippingFrom ? 0 : CONFIG.shippingCost;

  function addToBag(id, ml, qty = 1) {
    const p = findProduct(id);
    if (!p) return;
    const size = sizeOf(p, ml);
    const line = bag.find((i) => i.id === id && Number(i.ml) === size.ml);
    if (line) line.qty += qty;
    else bag.push({ id, ml: size.ml, qty });
    saveBag();
    renderBag();
    openBag();
  }

  function setQty(id, ml, qty) {
    const line = bag.find((i) => i.id === id && Number(i.ml) === Number(ml));
    if (!line) return;
    line.qty = Math.max(1, qty);
    saveBag();
    renderBag();
  }

  function removeLine(id, ml) {
    bag = bag.filter((i) => !(i.id === id && Number(i.ml) === Number(ml)));
    saveBag();
    renderBag();
  }

  function bagMessage() {
    const lines = bag
      .map((i) => {
        const p = findProduct(i.id);
        if (!p) return "";
        const s = sizeOf(p, i.ml);
        return `• ${p.name} — ${s.ml} ml × ${i.qty} — ${money(s.price * i.qty)}`;
      })
      .filter(Boolean)
      .join("\n");

    const subtotal = bagSubtotal();
    const shipping = shippingFor(subtotal);

    return `${CONFIG.greeting}

${lines}

Subtotaal: ${money(subtotal)}
Verzending: ${shipping === 0 ? "gratis" : money(shipping)}
Totaal: ${money(subtotal + shipping)}

Mijn gegevens:
Naam:
Adres:
Postcode + plaats:

Ik hoor graag hoe ik kan betalen.`;
  }

  const bagItems = $("#bagItems");
  const bagCountEl = $("#bagCount");

  function renderBag() {
    const count = bagCount();
    bagCountEl.textContent = count;
    bagCountEl.classList.toggle("has-items", count > 0);
    $("#bagBtn").setAttribute(
      "aria-label",
      count ? `Winkelmandje openen (${count})` : "Winkelmandje openen"
    );
    $("#bagTitleCount").textContent = count ? `(${count})` : "";

    if (!bag.length) {
      bagItems.innerHTML = `
        <div class="bag-empty">
          <p>Je mandje is nog leeg.</p>
          <a class="btn btn-outline" href="#collectie" data-close-bag>Bekijk de collectie</a>
        </div>`;
    } else {
      bagItems.innerHTML = bag
        .map((i) => {
          const p = findProduct(i.id);
          if (!p) return "";
          const s = sizeOf(p, i.ml);
          return `
            <div class="bag-item">
              <img src="${p.img}" alt="" width="72" height="90" loading="lazy">
              <div>
                <h3>${p.name}</h3>
                <p>${s.ml} ml · ${p.family}</p>
                <div class="qty">
                  <button data-qty="-1" data-id="${p.id}" data-ml="${s.ml}" aria-label="Eén minder">
                    <svg class="icon" aria-hidden="true"><use href="#i-minus"/></svg>
                  </button>
                  <span>${i.qty}</span>
                  <button data-qty="1" data-id="${p.id}" data-ml="${s.ml}" aria-label="Eén meer">
                    <svg class="icon" aria-hidden="true"><use href="#i-plus"/></svg>
                  </button>
                </div>
              </div>
              <div>
                <p class="bag-item-price">${money(s.price * i.qty)}</p>
                <button class="bag-remove" data-remove data-id="${p.id}" data-ml="${s.ml}">Verwijder</button>
              </div>
            </div>`;
        })
        .join("");
    }

    const subtotal = bagSubtotal();
    const shipping = shippingFor(subtotal);
    $("#bagSubtotal").textContent = money(subtotal);
    $("#bagShipping").textContent = shipping === 0 ? "gratis" : money(shipping);
    $("#bagTotal").textContent = money(subtotal + shipping);
    $("#bagOrder").disabled = bag.length === 0;
    $("#bagOrder").style.opacity = bag.length === 0 ? ".5" : "1";
    $("#bagOrder").style.pointerEvents = bag.length === 0 ? "none" : "auto";
  }

  /* -------------------------------------------------------- focus beheer */
  let lastFocus = null;

  function trapFocus(container, e) {
    if (e.key !== "Tab") return;
    const items = $$(
      'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])',
      container
    ).filter((el) => el.offsetParent !== null);
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function lockScroll(lock) {
    document.body.style.overflow = lock ? "hidden" : "";
  }

  /* ------------------------------------------------------- product modal */
  const modal = $("#productModal");
  const modalPanel = $(".modal-panel", modal);
  let modalProduct = null;
  let modalSize = null;

  function openProduct(id, ml) {
    const p = findProduct(id);
    if (!p) return;
    modalProduct = p;
    modalSize = sizeOf(p, ml || p.sizes[0].ml);

    $("#modalImg").src = p.img;
    $("#modalImg").alt = `Flacon van ${p.name}`;
    $("#modalFamily").textContent = p.family;
    $("#modalTitle").textContent = p.name;
    $("#modalDesc").textContent = p.desc;
    $("#modalNotes").innerHTML = `
      <div><dt>Top</dt><dd>${p.notes.top}</dd></div>
      <div><dt>Hart</dt><dd>${p.notes.heart}</dd></div>
      <div><dt>Basis</dt><dd>${p.notes.base}</dd></div>`;

    $("#modalSizes").innerHTML = p.sizes
      .map(
        (s) => `<button class="size${s.ml === modalSize.ml ? " is-active" : ""}"
                  data-size="${s.ml}" aria-pressed="${s.ml === modalSize.ml}">${s.ml} ml</button>`
      )
      .join("");

    updateModalPrice();
    $("#modalOrder").onclick = () => {
      window.open(
        waLink(
          `Hoi! Ik heb interesse in ${p.name} (${modalSize.ml} ml, ${money(modalSize.price)}).\n\nIs deze nog op voorraad? Ik hoor graag hoe ik kan bestellen.`
        ),
        "_blank",
        "noopener"
      );
    };

    lastFocus = document.activeElement;
    modal.hidden = false;
    lockScroll(true);
    modalPanel.focus();
  }

  function updateModalPrice() {
    $("#modalPrice").textContent = money(modalSize.price);
    $("#modalPriceNote").textContent = `per ${modalSize.ml} ml`;
  }

  function closeProduct() {
    modal.hidden = true;
    modalProduct = null;
    lockScroll(false);
    if (lastFocus) lastFocus.focus();
  }

  /* -------------------------------------------------------- bag drawer */
  const drawer = $("#bagDrawer");
  const drawerPanel = $(".drawer-panel", drawer);

  function openBag() {
    if (!drawer.hidden) return;
    lastFocus = document.activeElement;
    drawer.hidden = false;
    lockScroll(true);
    drawerPanel.focus();
  }
  function closeBag() {
    drawer.hidden = true;
    lockScroll(false);
    if (lastFocus) lastFocus.focus();
  }

  /* --------------------------------------------------------------- events */
  document.addEventListener("click", (e) => {
    const openBtn = e.target.closest("[data-open]");
    if (openBtn) { openProduct(openBtn.dataset.open); return; }

    const addBtn = e.target.closest("[data-add]");
    if (addBtn) {
      const p = findProduct(addBtn.dataset.add);
      addToBag(p.id, p.sizes[0].ml);
      return;
    }

    const sizeBtn = e.target.closest("[data-size]");
    if (sizeBtn && modalProduct) {
      modalSize = sizeOf(modalProduct, sizeBtn.dataset.size);
      $$(".size", $("#modalSizes")).forEach((b) => {
        const on = b.dataset.size === String(modalSize.ml);
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on);
      });
      updateModalPrice();
      return;
    }

    const qtyBtn = e.target.closest("[data-qty]");
    if (qtyBtn) {
      const line = bag.find(
        (i) => i.id === qtyBtn.dataset.id && Number(i.ml) === Number(qtyBtn.dataset.ml)
      );
      if (line) setQty(line.id, line.ml, line.qty + Number(qtyBtn.dataset.qty));
      return;
    }

    const removeBtn = e.target.closest("[data-remove]");
    if (removeBtn) { removeLine(removeBtn.dataset.id, removeBtn.dataset.ml); return; }

    if (e.target.closest("[data-close-modal]")) { closeProduct(); return; }
    if (e.target.closest("[data-close-bag]")) { closeBag(); return; }

    const filterLink = e.target.closest("[data-filter-link]");
    if (filterLink) {
      setFilter(filterLink.dataset.filterLink);
    }
  });

  $("#modalAdd").addEventListener("click", () => {
    if (!modalProduct) return;
    addToBag(modalProduct.id, modalSize.ml);
    closeProduct();
  });

  $("#bagOrder").addEventListener("click", () => {
    if (!bag.length) return;
    window.open(waLink(bagMessage()), "_blank", "noopener");
  });

  $("#bagBtn").addEventListener("click", openBag);
  $$("[data-close-bag]").forEach((el) => el.addEventListener("click", closeBag));

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (!modal.hidden) closeProduct();
      else if (!drawer.hidden) closeBag();
      else if (!mobileMenu.hidden) closeMenu();
    }
    if (!modal.hidden) trapFocus(modalPanel, e);
    if (!drawer.hidden) trapFocus(drawerPanel, e);
  });

  /* --------------------------------------------------------------- filters */
  function setFilter(value) {
    activeFilter = value;
    $$(".chip").forEach((c) => {
      const on = c.dataset.filter === value;
      c.classList.toggle("is-active", on);
      c.setAttribute("aria-pressed", on);
    });
    renderGrid();
  }

  $$(".chip").forEach((chip) =>
    chip.addEventListener("click", () => setFilter(chip.dataset.filter))
  );

  /* ---------------------------------------------------------------- header */
  const header = $("#header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ----------------------------------------------------------- mobiel menu */
  const mobileMenu = $("#mobileMenu");
  const menuBtn = $("#menuBtn");

  function openMenu() {
    mobileMenu.hidden = false;
    menuBtn.setAttribute("aria-expanded", "true");
    menuBtn.setAttribute("aria-label", "Menu sluiten");
    $("use", menuBtn).setAttribute("href", "#i-close");
  }
  function closeMenu() {
    mobileMenu.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
    menuBtn.setAttribute("aria-label", "Menu openen");
    $("use", menuBtn).setAttribute("href", "#i-menu");
  }
  menuBtn.addEventListener("click", () =>
    mobileMenu.hidden ? openMenu() : closeMenu()
  );
  $$("a", mobileMenu).forEach((a) => a.addEventListener("click", closeMenu));
  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) closeMenu();
  });

  /* --------------------------------------------------------------- reveal */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
  );

  function setupReveal() {
    const targets = $$(
      ".section-head, .editorial, .quote-band, .step, .review, .faq-list, .cta-inner, .usp-grid"
    );
    targets.forEach((el) => {
      el.classList.add("reveal");
      revealObserver.observe(el);
    });
  }

  /* ------------------------------------------------------------------ init */
  $("#year").textContent = new Date().getFullYear();
  applyWaLinks();
  renderGrid();
  renderBag();
  setupReveal();
})();
