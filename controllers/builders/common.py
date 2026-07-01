from decimal import Decimal, ROUND_HALF_UP
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, register_namespace, tostring


NS = {
    "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
}

for prefix, uri in NS.items():
    register_namespace(prefix, uri)


def qname(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def format_decimal(value, digits: int = 2) -> str:
    quant = Decimal("1." + ("0" * digits))
    return str(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))


def add_text(parent, prefix: str, tag: str, text, digits: int | None = None):
    child = SubElement(parent, qname(prefix, tag))
    child.text = format_decimal(text, digits) if digits is not None else str(text)
    return child


def pretty_xml(element: Element) -> str:
    rough = tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")


def format_yyyymmdd(date_value) -> str:
    return date_value.strftime("%Y%m%d")


def code_or_default(value: str | None, default: str) -> str:
    if value is None:
        return default

    value = value.strip()
    if not value or value.lower() == "string":
        return default

    return value
