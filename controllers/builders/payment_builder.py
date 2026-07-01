from xml.etree.ElementTree import SubElement

from controllers.builders.common import add_text, format_yyyymmdd, qname


def build_payment_means(header_settlement, payment_data):
    if not payment_data or not payment_data.iban:
        return

    payment = SubElement(
        header_settlement,
        qname("ram", "SpecifiedTradeSettlementPaymentMeans"),
    )
    add_text(payment, "ram", "TypeCode", getattr(payment_data, "type_code", "58"))

    payment_info = getattr(payment_data, "information", None)
    if payment_info:
        add_text(payment, "ram", "Information", payment_info)

    account = SubElement(payment, qname("ram", "PayeePartyCreditorFinancialAccount"))
    add_text(account, "ram", "IBANID", payment_data.iban)

    if payment_data.bic:
        institution = SubElement(
            payment,
            qname("ram", "PayeeSpecifiedCreditorFinancialInstitution"),
        )
        add_text(institution, "ram", "BICID", payment_data.bic)


def build_payment_terms(header_settlement, payment_terms, invoice):
    if not payment_terms:
        return

    terms = SubElement(
        header_settlement,
        qname("ram", "SpecifiedTradePaymentTerms"),
    )
    add_text(terms, "ram", "Description", payment_terms.description)

    if invoice.due_date:
        due_date = SubElement(terms, qname("ram", "DueDateDateTime"))
        date_node = add_text(
            due_date,
            "udt",
            "DateTimeString",
            format_yyyymmdd(invoice.due_date),
        )
        date_node.set("format", "102")
