"""Renders a human-readable visual PDF page for a GermanInvoice, using one
of 3 built-in branding styles ("XPDF Vorlage #1-3"). Used as the visual
carrier before embedding CII XML (see :mod:`controllers.facturx_service`),
so the resulting Factur-X PDF actually displays the real invoice data
instead of static placeholder text.
"""

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

import fitz

from models.en16931 import GermanInvoice

logger = logging.getLogger(__name__)

BLACK = (0, 0, 0)
GRAY = (0.4, 0.4, 0.4)
MARGIN = 50
RIGHT = 545


@dataclass(frozen=True)
class TemplateStyle:
    """Visual branding for one built-in template."""

    label: str
    accent: Tuple[float, float, float]
    logo_shape: str  # "circle" | "square" | "triangle"
    tagline: str


TEMPLATE_STYLES = {
    1: TemplateStyle("Vorlage #1", (0.13, 0.35, 0.78), "circle", "Klassisches Rechnungsdesign"),
    2: TemplateStyle("Vorlage #2", (0.10, 0.55, 0.30), "square", "Modernes, reduziertes Design"),
    3: TemplateStyle("Vorlage #3", (0.80, 0.35, 0.05), "triangle", "Kräftiges Akzentdesign"),
}


class UnknownTemplateError(Exception):
    """Raised when an unknown template id is requested."""


class VisualInvoiceRenderer:
    """Renders a branded, human-readable visual PDF page from a GermanInvoice."""

    def render(self, invoice: GermanInvoice, template_id: int) -> bytes:
        """
        Args:
            invoice: The structured invoice to render.
            template_id: Which built-in style to use (1, 2, or 3).

        Returns:
            A single-page PDF (as bytes) showing the invoice with the
            chosen style's logo/accent color.

        Raises:
            UnknownTemplateError: If ``template_id`` isn't 1, 2, or 3.
        """
        style = TEMPLATE_STYLES.get(template_id)
        if style is None:
            raise UnknownTemplateError(f"Unknown template id: {template_id}")

        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        currency = invoice.invoice.currency or "EUR"

        def text(x, y, s, size=10, font="helv", color=BLACK):
            page.insert_text((x, y), s, fontsize=size, fontname=font, color=color)

        def rtext(x_right, y, s, size=10, font="helv", color=BLACK):
            w = fitz.get_text_length(s, fontname=font, fontsize=size)
            page.insert_text((x_right - w, y), s, fontsize=size, fontname=font, color=color)

        def hline(y, x0=MARGIN, x1=RIGHT, width=0.75, color=BLACK):
            page.draw_line((x0, y), (x1, y), color=color, width=width)

        def address_line(address) -> Optional[str]:
            if not address:
                return None
            return f"{address.line_one}, {address.postcode} {address.city}"

        # --- Logo mark ---
        logo_center = (MARGIN + 18, 40)
        initials = "".join(w[0] for w in invoice.seller.name.split()[:2]).upper() or "??"
        if style.logo_shape == "circle":
            page.draw_circle(logo_center, 18, color=style.accent, fill=style.accent)
        elif style.logo_shape == "square":
            page.draw_rect(
                fitz.Rect(logo_center[0] - 18, logo_center[1] - 18, logo_center[0] + 18, logo_center[1] + 18),
                color=style.accent, fill=style.accent,
            )
        else:
            p1 = (logo_center[0], logo_center[1] - 20)
            p2 = (logo_center[0] - 18, logo_center[1] + 14)
            p3 = (logo_center[0] + 18, logo_center[1] + 14)
            page.draw_polyline([p1, p2, p3, p1], color=style.accent, fill=style.accent)
        w_initials = fitz.get_text_length(initials, fontname="hebo", fontsize=11)
        page.insert_text((logo_center[0] - w_initials / 2, logo_center[1] + 4), initials,
                          fontsize=11, fontname="hebo", color=(1, 1, 1))

        # --- Header ---
        text(MARGIN + 46, 45, invoice.seller.name, size=15, font="hebo", color=style.accent)
        text(MARGIN + 46, 60, style.tagline, size=8, color=GRAY)
        rtext(RIGHT, 50, "RECHNUNG", size=18, font="hebo")

        y = 75
        seller_address = address_line(invoice.seller.address)
        if seller_address:
            text(MARGIN + 46, y, seller_address, size=8, color=GRAY)
            y += 12
        if invoice.seller.vat_id:
            text(MARGIN + 46, y, f"USt-IdNr.: {invoice.seller.vat_id}", size=8, color=GRAY)

        hline(100, color=style.accent, width=1.5)

        # --- Buyer address block ---
        text(MARGIN, 130, "Rechnungsempfänger", size=8, color=GRAY)
        text(MARGIN, 145, invoice.buyer.name, size=11, font="hebo")
        buyer_address = address_line(invoice.buyer.address)
        if buyer_address:
            text(MARGIN, 159, buyer_address, size=10)

        # --- Invoice meta box ---
        meta_x = 330
        meta_rows = [
            ("Rechnungsnummer", invoice.invoice.number),
            ("Rechnungsdatum", invoice.invoice.issue_date.strftime("%d.%m.%Y")),
            (
                "Lieferdatum",
                invoice.invoice.delivery_date.strftime("%d.%m.%Y") if invoice.invoice.delivery_date else "-",
            ),
            ("Fälligkeitsdatum", invoice.invoice.due_date.strftime("%d.%m.%Y") if invoice.invoice.due_date else "-"),
        ]
        page.draw_rect(
            fitz.Rect(meta_x, 118, RIGHT, 118 + len(meta_rows) * 16 + 8),
            color=style.accent, fill=None, width=0.75,
        )
        for i, (label, value) in enumerate(meta_rows):
            row_y = 134 + i * 16
            text(meta_x + 8, row_y, label, size=8, color=GRAY)
            rtext(RIGHT - 8, row_y, value, size=9, font="hebo")

        # --- Line items table ---
        col_pos_left = MARGIN
        col_desc_left = MARGIN + 30
        col_qty_end = 340
        col_price_end = 445
        col_total_end = RIGHT

        table_top = 210
        page.draw_rect(fitz.Rect(MARGIN, table_top, RIGHT, table_top + 20), color=None, fill=style.accent)
        text(col_pos_left + 4, table_top + 14, "Pos.", size=9, font="hebo", color=(1, 1, 1))
        text(col_desc_left + 4, table_top + 14, "Beschreibung", size=9, font="hebo", color=(1, 1, 1))
        rtext(col_qty_end, table_top + 14, "Menge", size=9, font="hebo", color=(1, 1, 1))
        rtext(col_price_end, table_top + 14, "Einzelpreis", size=9, font="hebo", color=(1, 1, 1))
        rtext(col_total_end - 4, table_top + 14, "Gesamt (Netto)", size=9, font="hebo", color=(1, 1, 1))

        row_y = table_top + 20
        row_h = 22
        for idx, line in enumerate(invoice.lines, start=1):
            y = row_y + 15
            text(col_pos_left + 4, y, str(idx), size=9)
            text(col_desc_left + 4, y, line.name, size=9)
            rtext(col_qty_end, y, f"{line.quantity:.2f}", size=9)
            rtext(col_price_end, y, f"{line.net_price:.2f} {currency}", size=9)
            rtext(col_total_end - 4, y, f"{line.line_net_amount:.2f} {currency}", size=9)
            row_y += row_h

        hline(row_y, color=GRAY, width=0.5)

        # --- Totals block ---
        label_end = col_price_end
        totals = invoice.totals
        ty = row_y + 20
        for label, value in [
            ("Nettobetrag", totals.tax_exclusive_amount),
            ("Umsatzsteuer", totals.tax_amount),
        ]:
            rtext(label_end, ty, label, size=9, color=GRAY)
            rtext(RIGHT - 4, ty, f"{value:.2f} {currency}", size=9)
            ty += 16

        hline(ty + 4, x0=label_end - 150, color=GRAY, width=0.5)
        ty += 20
        rtext(label_end, ty, "Gesamtbetrag", size=11, font="hebo")
        rtext(RIGHT - 4, ty, f"{totals.tax_inclusive_amount:.2f} {currency}", size=11, font="hebo")

        # --- Footer ---
        footer_y = ty + 50
        hline(footer_y, color=style.accent, width=1.5)
        fy = footer_y + 20
        if invoice.payment_terms:
            text(MARGIN, fy, invoice.payment_terms.description, size=9)
            fy += 16
        if invoice.payment and invoice.payment.iban:
            bic_part = f"   BIC: {invoice.payment.bic}" if invoice.payment.bic else ""
            text(MARGIN, fy, f"IBAN: {invoice.payment.iban}{bic_part}", size=9)

        result = doc.tobytes()
        logger.info("Rendered visual invoice PDF using template %s", template_id)
        return result
