from xml.etree.ElementTree import SubElement

from controllers.builders.common import add_text, format_yyyymmdd, qname


def build_document_context(root):
    context = SubElement(root, qname("rsm", "ExchangedDocumentContext"))
    guideline = SubElement(
        context,
        qname("ram", "GuidelineSpecifiedDocumentContextParameter"),
    )
    add_text(guideline, "ram", "ID", "urn:cen.eu:en16931:2017")


def build_exchanged_document(root, invoice):
    document = SubElement(root, qname("rsm", "ExchangedDocument"))
    add_text(document, "ram", "ID", invoice.number)
    add_text(document, "ram", "TypeCode", getattr(invoice, "type_code", "380"))

    issue_date = SubElement(document, qname("ram", "IssueDateTime"))
    date_node = add_text(
        issue_date,
        "udt",
        "DateTimeString",
        format_yyyymmdd(invoice.issue_date),
    )
    date_node.set("format", "102")


def build_header_delivery(transaction, invoice):
    header_delivery = SubElement(
        transaction,
        qname("ram", "ApplicableHeaderTradeDelivery"),
    )

    if invoice.delivery_date:
        delivery_event = SubElement(
            header_delivery,
            qname("ram", "ActualDeliverySupplyChainEvent"),
        )
        occurrence = SubElement(delivery_event, qname("ram", "OccurrenceDateTime"))
        date_node = add_text(
            occurrence,
            "udt",
            "DateTimeString",
            format_yyyymmdd(invoice.delivery_date),
        )
        date_node.set("format", "102")
