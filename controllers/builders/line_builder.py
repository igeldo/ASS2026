from xml.etree.ElementTree import SubElement

from controllers.builders.common import add_text, qname


def build_line_items(transaction, lines):
    for line in lines:
        build_line_item(transaction, line)


def build_line_item(transaction, line):
    line_item = SubElement(
        transaction,
        qname("ram", "IncludedSupplyChainTradeLineItem"),
    )

    line_doc = SubElement(line_item, qname("ram", "AssociatedDocumentLineDocument"))
    add_text(line_doc, "ram", "LineID", line.id)

    product = SubElement(line_item, qname("ram", "SpecifiedTradeProduct"))
    add_text(product, "ram", "Name", line.name)

    description = getattr(line, "description", None)
    if description:
        add_text(product, "ram", "Description", description)

    build_line_agreement(line_item, line)
    build_line_delivery(line_item, line)
    build_line_settlement(line_item, line)


def build_line_agreement(line_item, line):
    agreement = SubElement(line_item, qname("ram", "SpecifiedLineTradeAgreement"))

    gross_price = SubElement(agreement, qname("ram", "GrossPriceProductTradePrice"))
    add_text(gross_price, "ram", "ChargeAmount", line.net_price, digits=4)
    basis_quantity = add_text(gross_price, "ram", "BasisQuantity", "1.0000")
    basis_quantity.set("unitCode", line.unit_code)

    net_price = SubElement(agreement, qname("ram", "NetPriceProductTradePrice"))
    add_text(net_price, "ram", "ChargeAmount", line.net_price, digits=4)
    basis_quantity = add_text(net_price, "ram", "BasisQuantity", "1.0000")
    basis_quantity.set("unitCode", line.unit_code)


def build_line_delivery(line_item, line):
    delivery = SubElement(line_item, qname("ram", "SpecifiedLineTradeDelivery"))
    quantity = add_text(delivery, "ram", "BilledQuantity", line.quantity, digits=4)
    quantity.set("unitCode", line.unit_code)


def build_line_settlement(line_item, line):
    settlement = SubElement(line_item, qname("ram", "SpecifiedLineTradeSettlement"))
    tax = SubElement(settlement, qname("ram", "ApplicableTradeTax"))
    add_text(tax, "ram", "TypeCode", "VAT")
    add_text(tax, "ram", "CategoryCode", "S")
    add_text(tax, "ram", "RateApplicablePercent", line.tax_rate, digits=2)

    line_sum = SubElement(
        settlement,
        qname("ram", "SpecifiedTradeSettlementLineMonetarySummation"),
    )
    add_text(line_sum, "ram", "LineTotalAmount", line.line_net_amount, digits=2)
