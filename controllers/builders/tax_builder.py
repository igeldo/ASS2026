from xml.etree.ElementTree import SubElement

from controllers.builders.common import add_text, qname


def build_header_taxes(header_settlement, tax_breakdowns):
    for tax_data in tax_breakdowns:
        header_tax = SubElement(header_settlement, qname("ram", "ApplicableTradeTax"))
        add_text(header_tax, "ram", "CalculatedAmount", tax_data.calculated_amount, digits=2)
        add_text(header_tax, "ram", "TypeCode", "VAT")
        add_text(header_tax, "ram", "BasisAmount", tax_data.basis_amount, digits=2)
        add_text(header_tax, "ram", "CategoryCode", tax_data.category_code)
        add_text(header_tax, "ram", "RateApplicablePercent", tax_data.rate, digits=2)


def build_monetary_summation(header_settlement, totals, currency: str):
    monetary = SubElement(
        header_settlement,
        qname("ram", "SpecifiedTradeSettlementHeaderMonetarySummation"),
    )

    add_text(monetary, "ram", "LineTotalAmount", totals.tax_exclusive_amount, digits=2)
    add_text(monetary, "ram", "TaxBasisTotalAmount", totals.tax_exclusive_amount, digits=2)

    tax_total = add_text(monetary, "ram", "TaxTotalAmount", totals.tax_amount, digits=2)
    tax_total.set("currencyID", currency)

    add_text(monetary, "ram", "GrandTotalAmount", totals.tax_inclusive_amount, digits=2)
    add_text(monetary, "ram", "DuePayableAmount", totals.payable_amount, digits=2)
