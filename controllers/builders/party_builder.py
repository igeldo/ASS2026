from xml.etree.ElementTree import SubElement

from controllers.builders.common import add_text, code_or_default, qname


def build_header_agreement(transaction, data):
    header_agreement = SubElement(
        transaction,
        qname("ram", "ApplicableHeaderTradeAgreement"),
    )

    buyer_reference = getattr(data.invoice, "buyer_reference", None)
    if buyer_reference:
        add_text(header_agreement, "ram", "BuyerReference", buyer_reference)

    add_trade_party(header_agreement, "SellerTradeParty", data.seller)
    add_trade_party(header_agreement, "BuyerTradeParty", data.buyer)


def add_address(parent, address_data):
    address = SubElement(parent, qname("ram", "PostalTradeAddress"))
    add_text(address, "ram", "PostcodeCode", address_data.postcode)
    add_text(address, "ram", "LineOne", address_data.line_one)
    add_text(address, "ram", "CityName", address_data.city)
    add_text(address, "ram", "CountryID", code_or_default(address_data.country_id, "DE"))


def add_vat_registration(parent, vat_id: str):
    tax_registration = SubElement(parent, qname("ram", "SpecifiedTaxRegistration"))
    tax_id = add_text(tax_registration, "ram", "ID", vat_id)
    tax_id.set("schemeID", "VA")


def add_trade_party(parent, tag: str, party_data):
    party = SubElement(parent, qname("ram", tag))
    add_text(party, "ram", "Name", party_data.name)

    if party_data.address:
        add_address(party, party_data.address)

    if party_data.vat_id:
        add_vat_registration(party, party_data.vat_id)

    return party
