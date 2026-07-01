"""Static HTML/JS source for the local invoice upload/testing interface."""

UPLOAD_PAGE_HTML = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<title>German Invoice OCR API</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root {
    --bg: #0f172a;
    --panel: #1e293b;
    --border: #334155;
    --accent: #38bdf8;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --ok: #34d399;
    --err: #f87171;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, Segoe UI, Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 2rem;
  }
  h1 { font-size: 1.4rem; margin-bottom: 0.25rem; }
  p.subtitle { color: var(--muted); margin-top: 0; margin-bottom: 2rem; }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
  @media (max-width: 900px) {
    .grid { grid-template-columns: 1fr; }
  }
  .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
  }
  .panel h2 { margin-top: 0; font-size: 1.05rem; }
  #dropzone {
    border: 2px dashed var(--border);
    border-radius: 10px;
    padding: 2.5rem 1rem;
    text-align: center;
    color: var(--muted);
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
  }
  #dropzone.dragover {
    border-color: var(--accent);
    color: var(--accent);
  }
  #fileInput { display: none; }
  textarea, pre {
    width: 100%;
    background: #0b1220;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 0.8rem;
    white-space: pre-wrap;
    word-break: break-word;
  }
  textarea { min-height: 260px; resize: vertical; }
  pre { min-height: 120px; max-height: 420px; overflow: auto; margin: 0; }
  select {
    background: #0b1220;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.6rem;
    font-size: 0.85rem;
  }
  button {
    background: var(--accent);
    color: #0b1220;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 0.75rem;
  }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .status { font-size: 0.85rem; margin-top: 0.5rem; }
  .status.ok { color: var(--ok); }
  .status.err { color: var(--err); }
  .row { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
  label.checkbox { color: var(--muted); font-size: 0.85rem; display: flex; align-items: center; gap: 0.4rem; }
</style>
</head>
<body>
  <h1>German Invoice OCR API</h1>
  <p class="subtitle">Lokale Testoberfläche &mdash; Rechnung hochladen, extrahieren, als ZUGFeRD-XML erzeugen.</p>

  <div class="grid">
    <div class="panel">
      <h2>1. Rechnung hochladen (PDF/JPG)</h2>
      <div id="dropzone">
        Datei hier ablegen oder klicken zum Auswaehlen
        <input id="fileInput" type="file" accept=".pdf,.jpg,.jpeg,.png" />
      </div>
      <div id="extractStatus" class="status"></div>
      <h2>Extrahiertes JSON</h2>
      <pre id="extractResult">-</pre>
    </div>

    <div class="panel">
      <h2>2. GermanInvoice JSON &rarr; ZUGFeRD CII XML</h2>
      <p class="subtitle" style="margin-bottom: 0.5rem;">
        Wird nach Schritt 1 automatisch befuellt, oder hier manuell eingeben/einfuegen.
      </p>
      <textarea id="invoiceJson" placeholder="Noch keine Daten &mdash; erst eine Rechnung in Schritt 1 hochladen, oder das Beispiel laden."></textarea>
      <div class="row">
        <button id="generateXmlBtn">XML erzeugen</button>
        <button id="loadExampleBtn">Beispiel laden</button>
        <button id="nextNumberBtn">Nächste Rechnungsnummer holen</button>
        <label class="checkbox">
          <input type="checkbox" id="validateCheckbox" checked />
          EN16931 / XSD validieren
        </label>
      </div>
      <p class="subtitle" style="margin: 0.25rem 0 0;">
        "Nächste Rechnungsnummer holen" vergibt serverseitig eine fortlaufende
        Nummer (§14 UStG/GoBD) und traegt sie in <code>invoice.number</code> ein.
        Einmal vergebene Nummern werden nie wiederverwendet, auch nicht nach
        einem Neustart.
      </p>
      <div id="xmlStatus" class="status"></div>
      <h2>Ergebnis (XML oder Validierungsfehler)</h2>
      <pre id="xmlResult">-</pre>
      <div class="row">
        <button id="copyXmlBtn" disabled>XML kopieren</button>
        <button id="downloadXmlBtn" disabled>XML herunterladen</button>
      </div>

      <h2>3. ZUGFeRD-PDF erzeugen (XML + visuelle PDF-Vorlage)</h2>
      <p class="subtitle" style="margin-bottom: 0.5rem;">
        Vorlage waehlen (wird mit den echten Daten aus dem JSON oben befuellt),
        eigene PDF hochladen, oder leer lassen, um automatisch die in
        Schritt 1 hochgeladene Datei zu verwenden.
      </p>
      <div class="row">
        <select id="templateSelect">
          <option value="">-- keine Vorlage (eigene Datei/Schritt 1) --</option>
          <option value="1">XPDF Vorlage #1</option>
          <option value="2">XPDF Vorlage #2</option>
          <option value="3">XPDF Vorlage #3</option>
        </select>
        <input id="visualPdfInput" type="file" accept=".pdf" />
      </div>
      <div class="row">
        <button id="generatePdfBtn">ZUGFeRD-PDF erzeugen &amp; herunterladen</button>
      </div>
      <div id="pdfStatus" class="status"></div>
    </div>
  </div>

<script>
const EXAMPLE_INVOICE = {
  invoice: {
    number: "INV-2026-001",
    issue_date: "2026-05-06",
    delivery_date: "2026-05-06",
    due_date: "2026-05-20",
    currency: "EUR"
  },
  seller: {
    name: "Seller GmbH",
    vat_id: "DE123456789",
    address: { postcode: "10115", line_one: "Seller Str. 1", city: "Berlin", country_id: "DE" },
    contact: null
  },
  buyer: {
    name: "Buyer GmbH",
    vat_id: null,
    address: { postcode: "80331", line_one: "Buyer Str. 2", city: "Munich", country_id: "DE" },
    contact: null
  },
  payment: { iban: "DE89370400440532013000", bic: "COBADEFFXXX" },
  payment_terms: { description: "Payment due within 14 days." },
  totals: {
    tax_exclusive_amount: "100.00",
    tax_inclusive_amount: "119.00",
    tax_amount: "19.00",
    payable_amount: "119.00"
  },
  lines: [
    {
      id: "1",
      name: "Consulting service",
      quantity: "1.0000",
      unit_code: "C62",
      net_price: "100.0000",
      line_net_amount: "100.00",
      tax_rate: "19.00"
    }
  ],
  tax_breakdowns: [
    { category_code: "S", rate: "19.00", basis_amount: "100.00", calculated_amount: "19.00" }
  ]
};

const invoiceJsonEl = document.getElementById("invoiceJson");

document.getElementById("loadExampleBtn").addEventListener("click", () => {
  invoiceJsonEl.value = JSON.stringify(EXAMPLE_INVOICE, null, 2);
});

document.getElementById("nextNumberBtn").addEventListener("click", async () => {
  let invoice;
  try {
    invoice = JSON.parse(invoiceJsonEl.value);
  } catch (err) {
    setStatus(xmlStatus, "Ungueltiges JSON: " + err, "err");
    return;
  }

  try {
    const res = await fetch("/api/v1/invoices/next-number", { method: "POST" });
    const body = await res.json();

    if (!res.ok || !body.success) {
      setStatus(xmlStatus, "Fehler beim Vergeben der Rechnungsnummer: " + JSON.stringify(body.errors), "err");
      return;
    }

    invoice.invoice = invoice.invoice || {};
    invoice.invoice.number = body.data.number;
    invoiceJsonEl.value = JSON.stringify(invoice, null, 2);
    setStatus(xmlStatus, "Rechnungsnummer " + body.data.number + " vergeben und eingetragen.", "ok");
  } catch (err) {
    setStatus(xmlStatus, "Netzwerkfehler: " + err, "err");
  }
});

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const extractStatus = document.getElementById("extractStatus");
const extractResult = document.getElementById("extractResult");

// The originally uploaded file is reused as the visual PDF in step 3,
// so the user doesn't have to upload the same invoice twice.
let lastUploadedFile = null;

function setStatus(el, message, kind) {
  el.textContent = message;
  el.className = "status" + (kind ? " " + kind : "");
}

async function uploadInvoice(file) {
  setStatus(extractStatus, "Verarbeite " + file.name + " ...", "");
  extractResult.textContent = "-";
  // Only reuse this file for step 3 if it's actually a PDF (Factur-X needs
  // a real PDF as the visual carrier, not a JPG/PNG scan).
  lastUploadedFile = file.name.toLowerCase().endsWith(".pdf") ? file : null;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/v1/invoices/extract", { method: "POST", body: formData });
    const body = await res.json();

    if (!res.ok || !body.success) {
      setStatus(extractStatus, "Fehler: " + JSON.stringify(body.errors), "err");
      extractResult.textContent = JSON.stringify(body, null, 2);
      return;
    }

    extractResult.textContent = JSON.stringify(body.data, null, 2);

    if (body.data.mapped_invoice) {
      invoiceJsonEl.value = JSON.stringify(body.data.mapped_invoice, null, 2);
      setStatus(
        extractStatus,
        "Erfolgreich extrahiert und in Schritt 2 uebernommen. " +
          "Bitte pruefen (z.B. Kaeufer-Adresse, Positionen) vor dem Erzeugen.",
        "ok"
      );
    } else {
      const warnings = (body.data.mapping_warnings || []).join(", ");
      setStatus(
        extractStatus,
        "Extrahiert, aber automatische Uebernahme in Schritt 2 nicht moeglich " +
          "(fehlende Felder: " + warnings + "). Bitte manuell ergaenzen.",
        "err"
      );
    }
  } catch (err) {
    setStatus(extractStatus, "Netzwerkfehler: " + err, "err");
  }
}

dropzone.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    uploadInvoice(fileInput.files[0]);
  }
});

["dragenter", "dragover"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  })
);

["dragleave", "drop"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  })
);

dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    uploadInvoice(file);
  }
});

const xmlStatus = document.getElementById("xmlStatus");
const xmlResult = document.getElementById("xmlResult");
const validateCheckbox = document.getElementById("validateCheckbox");
const copyXmlBtn = document.getElementById("copyXmlBtn");
const downloadXmlBtn = document.getElementById("downloadXmlBtn");

let lastXml = null;

function setXmlAvailable(xml) {
  lastXml = xml;
  copyXmlBtn.disabled = !xml;
  downloadXmlBtn.disabled = !xml;
}

document.getElementById("generateXmlBtn").addEventListener("click", async () => {
  let invoice;
  try {
    invoice = JSON.parse(invoiceJsonEl.value);
  } catch (err) {
    setStatus(xmlStatus, "Ungueltiges JSON: " + err, "err");
    return;
  }

  setStatus(xmlStatus, "Erzeuge XML ...", "");
  xmlResult.textContent = "-";
  setXmlAvailable(null);

  try {
    const url = "/api/v1/zugferd/xml?validate=" + (validateCheckbox.checked ? "true" : "false");
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(invoice)
    });

    if (!res.ok) {
      const body = await res.json();
      setStatus(xmlStatus, "Validierung/Fehler (HTTP " + res.status + ")", "err");
      xmlResult.textContent = JSON.stringify(body, null, 2);
      return;
    }

    const xml = await res.text();
    setStatus(
      xmlStatus,
      "XML erzeugt (EN16931: " + res.headers.get("X-EN16931-Valid") +
        ", XSD: " + res.headers.get("X-ZUGFeRD-XSD-Valid") + ")",
      "ok"
    );
    xmlResult.textContent = xml;
    setXmlAvailable(xml);
  } catch (err) {
    setStatus(xmlStatus, "Netzwerkfehler: " + err, "err");
  }
});

copyXmlBtn.addEventListener("click", async () => {
  if (!lastXml) return;

  try {
    await navigator.clipboard.writeText(lastXml);
    setStatus(xmlStatus, "XML in die Zwischenablage kopiert.", "ok");
  } catch (err) {
    setStatus(xmlStatus, "Kopieren fehlgeschlagen: " + err, "err");
  }
});

downloadXmlBtn.addEventListener("click", () => {
  if (!lastXml) return;

  const blob = new Blob([lastXml], { type: "application/xml" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "invoice.xml";
  link.click();
  URL.revokeObjectURL(url);
});

const pdfStatus = document.getElementById("pdfStatus");
const visualPdfInput = document.getElementById("visualPdfInput");
const templateSelect = document.getElementById("templateSelect");

document.getElementById("generatePdfBtn").addEventListener("click", async () => {
  let invoice;
  try {
    invoice = JSON.parse(invoiceJsonEl.value);
  } catch (err) {
    setStatus(pdfStatus, "Ungueltiges JSON: " + err, "err");
    return;
  }

  setStatus(pdfStatus, "Erzeuge ZUGFeRD-PDF ...", "");

  const templateId = templateSelect.value;
  // Prefer an explicitly uploaded visual PDF; otherwise reuse the file
  // uploaded in step 1, so the user doesn't have to upload it twice.
  const visualPdf = visualPdfInput.files[0] || lastUploadedFile;

  if (!templateId && !visualPdf) {
    setStatus(
      pdfStatus,
      "Bitte eine Vorlage waehlen, eine PDF hochladen, oder in Schritt 1 eine Rechnung hochladen.",
      "err"
    );
    return;
  }

  const formData = new FormData();
  formData.append("invoice_json", JSON.stringify(invoice));
  // An explicitly selected template wins over an uploaded/reused PDF, since
  // choosing a template from the dropdown is a deliberate action.
  if (templateId) {
    formData.append("template_id", templateId);
  } else {
    formData.append("file", visualPdf);
  }

  try {
    const url = "/api/v1/zugferd/pdf?validate=" + (validateCheckbox.checked ? "true" : "false");
    const res = await fetch(url, { method: "POST", body: formData });

    if (!res.ok) {
      const body = await res.json();
      setStatus(pdfStatus, "Fehler (HTTP " + res.status + "): " + JSON.stringify(body.errors), "err");
      return;
    }

    const blob = await res.blob();
    const downloadUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = (invoice.invoice && invoice.invoice.number ? invoice.invoice.number : "invoice") + ".pdf";
    link.click();
    URL.revokeObjectURL(downloadUrl);

    setStatus(
      pdfStatus,
      "ZUGFeRD-PDF erzeugt und heruntergeladen (EN16931: " + res.headers.get("X-EN16931-Valid") +
        ", XSD: " + res.headers.get("X-ZUGFeRD-XSD-Valid") + ")",
      "ok"
    );
  } catch (err) {
    setStatus(pdfStatus, "Netzwerkfehler: " + err, "err");
  }
});
</script>
</body>
</html>
"""
