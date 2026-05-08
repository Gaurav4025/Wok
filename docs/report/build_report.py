from copy import deepcopy
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET
from zipfile import ZipFile


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS}

ET.register_namespace("w", W_NS)


ROOT = Path(__file__).resolve().parent
TEMPLATE = Path("/Users/gauravkumarsingh/Downloads/End Sem Report Format.docx")
SOURCE_HTML = ROOT / "little_wok_story_report.html"
OUTPUT_DOCX = ROOT / "Little_Wok_Story_Project_Report.docx"


def w_tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"


def append_text_run(paragraph, text: str, bold: bool = False, italic: bool = False):
    run = ET.SubElement(paragraph, w_tag("r"))
    rpr = ET.SubElement(run, w_tag("rPr"))
    fonts = ET.SubElement(rpr, w_tag("rFonts"))
    fonts.set(w_tag("ascii"), "Times New Roman")
    fonts.set(w_tag("hAnsi"), "Times New Roman")
    fonts.set(w_tag("cs"), "Times New Roman")
    fonts.set(w_tag("eastAsia"), "Times New Roman")
    if bold:
        ET.SubElement(rpr, w_tag("b"))
        ET.SubElement(rpr, w_tag("bCs"))
    if italic:
        ET.SubElement(rpr, w_tag("i"))
        ET.SubElement(rpr, w_tag("iCs"))
    size = ET.SubElement(rpr, w_tag("sz"))
    size.set(w_tag("val"), "24")
    size_cs = ET.SubElement(rpr, w_tag("szCs"))
    size_cs.set(w_tag("val"), "24")
    text_node = ET.SubElement(run, w_tag("t"))
    if text.strip() != text:
        text_node.set(f"{{{XML_NS}}}space", "preserve")
    text_node.text = text


def make_paragraph(style: Optional[str] = None, align: Optional[str] = None):
    p = ET.Element(w_tag("p"))
    ppr = ET.SubElement(p, w_tag("pPr"))
    if style:
        pstyle = ET.SubElement(ppr, w_tag("pStyle"))
        pstyle.set(w_tag("val"), style)
    if align:
        jc = ET.SubElement(ppr, w_tag("jc"))
        jc.set(w_tag("val"), align)
    return p


def make_page_break():
    p = ET.Element(w_tag("p"))
    r = ET.SubElement(p, w_tag("r"))
    br = ET.SubElement(r, w_tag("br"))
    br.set(w_tag("type"), "page")
    return p


def paragraph_from_html(elem):
    classes = elem.attrib.get("class", "")
    classes = set(classes.split()) if classes else set()
    tag = elem.tag.lower()

    style = "Body"
    align = "both"
    if tag == "h1":
        style = "heading 5"
        align = "center"
    elif tag == "h2":
        style = "heading 5"
        align = "center"
    elif tag == "h3":
        style = "heading 2"
        align = "center"
    elif tag == "h4":
        style = "heading 1"
        align = "left"
    elif "center" in classes:
        align = "center"

    p = make_paragraph(style=style, align=align)

    def walk(node, bold=False, italic=False):
        if node.text:
            append_text_run(p, node.text, bold=bold, italic=italic)
        for child in list(node):
            child_bold = bold or child.tag.lower() in {"b", "strong", "th"}
            child_italic = italic or child.tag.lower() in {"i", "em"}
            walk(child, bold=child_bold, italic=child_italic)
            if child.tail:
                append_text_run(p, child.tail, bold=bold, italic=italic)

    walk(elem)
    return p


def paragraph_text(text: str, style: str = "Body", align: str = "both"):
    p = make_paragraph(style=style, align=align)
    append_text_run(p, text)
    return p


def list_paragraphs(list_elem, ordered=False):
    paragraphs = []
    for idx, li in enumerate(list_elem.findall("li"), start=1):
        prefix = f"{idx}. " if ordered else "- "
        text = prefix + "".join(li.itertext()).strip()
        paragraphs.append(paragraph_text(text))
    return paragraphs


def table_from_html(elem):
    tbl = ET.Element(w_tag("tbl"))
    tbl_pr = ET.SubElement(tbl, w_tag("tblPr"))
    tbl_w = ET.SubElement(tbl_pr, w_tag("tblW"))
    tbl_w.set(w_tag("w"), "0")
    tbl_w.set(w_tag("type"), "auto")
    tbl_borders = ET.SubElement(tbl_pr, w_tag("tblBorders"))
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        border = ET.SubElement(tbl_borders, w_tag(side))
        border.set(w_tag("val"), "single")
        border.set(w_tag("sz"), "6")
        border.set(w_tag("space"), "0")
        border.set(w_tag("color"), "000000")

    for row in elem.findall("tr"):
        tr = ET.SubElement(tbl, w_tag("tr"))
        for cell in list(row):
            tc = ET.SubElement(tr, w_tag("tc"))
            tc_pr = ET.SubElement(tc, w_tag("tcPr"))
            tc_w = ET.SubElement(tc_pr, w_tag("tcW"))
            tc_w.set(w_tag("w"), "0")
            tc_w.set(w_tag("type"), "auto")
            p = make_paragraph(style="Body", align="left")
            text = "".join(cell.itertext()).strip()
            append_text_run(p, text, bold=cell.tag.lower() == "th")
            tc.append(p)
    return tbl


def build_document_body(html_root, sect_pr):
    body = ET.Element(w_tag("body"))
    html_body = html_root.find("body")
    for child in list(html_body):
        tag = child.tag.lower()
        if tag == "div" and "page-break" in child.attrib.get("class", ""):
            body.append(make_page_break())
            continue
        if tag in {"p", "h1", "h2", "h3", "h4"}:
            body.append(paragraph_from_html(child))
            continue
        if tag == "ol":
            for p in list_paragraphs(child, ordered=True):
                body.append(p)
            continue
        if tag == "ul":
            for p in list_paragraphs(child, ordered=False):
                body.append(p)
            continue
        if tag == "table":
            body.append(table_from_html(child))
            continue
    body.append(deepcopy(sect_pr))
    return body


def main():
    html_tree = ET.parse(SOURCE_HTML)
    html_root = html_tree.getroot()

    with ZipFile(TEMPLATE, "r") as zin:
        template_xml = ET.fromstring(zin.read("word/document.xml"))
        sect_pr = template_xml.find("w:body/w:sectPr", NS)
        new_doc = ET.Element(template_xml.tag, template_xml.attrib)
        new_doc.append(build_document_body(html_root, sect_pr))
        xml_bytes = ET.tostring(new_doc, encoding="utf-8", xml_declaration=True)

        with ZipFile(OUTPUT_DOCX, "w") as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = xml_bytes
                zout.writestr(item, data)


if __name__ == "__main__":
    main()
