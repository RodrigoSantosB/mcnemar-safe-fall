"""Primitivas de layout no padrão visual do template CIn-UFPE.

Medidas extraídas do template oficial (templates/template_cin_ufpe.pptx, 10 × 5,625 in)
e da referência visual do repositório (templates/referencia_visual_ML_PROJ_MLP.pdf).
"""

from __future__ import annotations

import copy
from pathlib import Path

from PIL import Image
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

RED = RGBColor(0xDB, 0x1E, 0x2F)
DARK_RED = RGBColor(0xAF, 0x04, 0x21)
NAVY = RGBColor(0x0E, 0x2A, 0x36)
TEAL = RGBColor(0x1C, 0x7C, 0x8C)
ORANGE = RGBColor(0xE7, 0xA2, 0x3B)
SAND = RGBColor(0xF4, 0xC7, 0x7B)
GRAY = RGBColor(0x66, 0x66, 0x66)
MID_GRAY = RGBColor(0x88, 0x88, 0x88)
LIGHT = RGBColor(0xF2, 0xF4, 0xF5)
BORDER = RGBColor(0xDD, 0xE2, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x26, 0x32, 0x38)

TITLE_FONT = "Cambria"
BODY_FONT = "Calibri"
LABEL_FONT = "Arial"
MONO_FONT = "Consolas"

SLIDE_W, SLIDE_H = 10.0, 5.625
MARGIN = 0.5

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "slides" / "assets"
FIGS = ROOT / "results" / "figures"


# ---------------------------------------------------------------- texto

def _apply_font(run, size, color, bold=False, italic=False, font=BODY_FONT):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    f.color.rgb = color


def text(slide, x, y, w, h, paragraphs, size=12, color=TEXT, font=BODY_FONT, bold=False, italic=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=None, line_spacing=None, margin=0.0):
    """Caixa de texto. ``paragraphs``: str, lista de str ou lista de listas de runs.

    Um run é str ou tupla (texto, {opções}) com chaves size/color/bold/italic/font.
    """
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing is not None and i > 0:
            p.space_before = Pt(spacing)
        if line_spacing is not None:
            p.line_spacing = line_spacing
        runs = para if isinstance(para, list) else [para]
        for r in runs:
            txt, opts = (r, {}) if isinstance(r, str) else r
            run = p.add_run()
            run.text = txt
            _apply_font(run, opts.get("size", size), opts.get("color", color), opts.get("bold", bold),
                        opts.get("italic", italic), opts.get("font", font))
    return box


def bullets(slide, x, y, w, h, items, size=12, color=TEXT, bullet_color=RED, spacing=6):
    """Lista com marcador quadrado vermelho (estilo do template)."""
    paras = [[("■  ", {"color": bullet_color, "size": size - 4}), *(it if isinstance(it, list) else [it])]
             for it in items]
    return text(slide, x, y, w, h, paras, size=size, color=color, spacing=spacing)


# ---------------------------------------------------------------- formas

def rect(slide, x, y, w, h, fill=WHITE, line=None, radius=None, shape=None):
    kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE)
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def card(slide, x, y, w, h, fill=WHITE, accent=None):
    """Cartão branco com borda suave e, opcionalmente, faixa de destaque à esquerda."""
    c = rect(slide, x, y, w, h, fill=fill, line=BORDER, radius=0.06)
    if accent is not None:
        rect(slide, x, y + 0.08, 0.06, h - 0.16, fill=accent)
    return c


def callout(slide, x, y, w, h, lead, body, size=12.5):
    """Caixa escura com chamada em destaque (padrão "O problema:" da referência)."""
    rect(slide, x, y, w, h, fill=NAVY, radius=0.08)
    text(slide, x + 0.22, y, w - 0.44, h, [[(lead + "  ", {"color": SAND, "bold": True}), (body, {"color": WHITE})]],
         size=size, anchor=MSO_ANCHOR.MIDDLE)


def badge(slide, x, y, d, label, fill=RED, color=WHITE, size=13, font=BODY_FONT, bold=True):
    """Círculo com número/letra (substitui ícones)."""
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", 0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    _apply_font(r, size, color, bold=bold, font=font)
    return s


def arrow(slide, x, y, w, h, fill=MID_GRAY):
    return rect(slide, x, y, w, h, fill=fill, shape=MSO_SHAPE.RIGHT_ARROW)


def chevron(slide, x, y, w, h, label, fill=RED, color=WHITE, size=12, first=False):
    s = slide.shapes.add_shape(MSO_SHAPE.PENTAGON if first else MSO_SHAPE.CHEVRON,
                               Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.25 if not first else 0.1)
    tf.margin_right = Inches(0.1)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    _apply_font(r, size, color, bold=True)
    return s


def picture(slide, path, x, y, w=None, h=None):
    """Insere imagem preservando proporção; w e h atuam como caixa máxima."""
    path = Path(path)
    iw, ih = Image.open(path).size
    if w is not None and h is not None:
        scale = min(w / iw, h / ih)
        pw, ph = iw * scale, ih * scale
        x += (w - pw) / 2
        y += (h - ph) / 2
    elif w is not None:
        pw, ph = w, w * ih / iw
    else:
        pw, ph = h * iw / ih, h
    return slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(pw), Inches(ph))


def table(slide, x, y, w, h, data, col_widths=None, size=10.5, header_fill=NAVY, zebra=True,
          highlight=None, align=None):
    """Tabela no estilo da referência (cabeçalho escuro, linhas claras).

    ``highlight``: dict {(linha, coluna): RGBColor} para colorir o texto de células.
    """
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gt.table
    tbl_pr = gt._element.graphic.graphicData.tbl.tblPr
    style = tbl_pr.find(qn("a:tableStyleId"))
    if style is not None:
        style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # "No Style, Table Grid"
    if col_widths:
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = Inches(cw)
    for r in range(rows):
        tbl.rows[r].height = Inches(h / rows)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.fore_color.rgb = LIGHT if (zebra and r % 2 == 0) else WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (align[c] if align else (PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER))
            run = p.add_run()
            run.text = str(data[r][c])
            color = WHITE if r == 0 else (highlight or {}).get((r, c), TEXT)
            _apply_font(run, size, color, bold=(r == 0 or (highlight or {}).get((r, c)) is not None))
            _set_cell_border(cell, "DDE2E6")
    return gt


def _set_cell_border(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = tc_pr.find(qn(tag))
        if ln is None:
            ln = tc_pr.makeelement(qn(tag), {"w": "6350"})
            tc_pr.append(ln)
        fill = ln.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"), {"val": hex_color})
        fill.append(clr)
        ln.append(fill)


# ---------------------------------------------------------------- moldura de conteúdo

def content_chrome(slide, section, title, number, title_size=21):
    """Rótulo de seção, título, logotipo CIn e número — como na referência visual."""
    text(slide, MARGIN, 0.24, 6.5, 0.25, section.upper(), size=9, color=GRAY, bold=True, font=LABEL_FONT)
    text(slide, MARGIN, 0.47, 7.95, 0.62, title, size=title_size, color=RED, bold=True, font=TITLE_FONT,
         anchor=MSO_ANCHOR.MIDDLE)
    picture(slide, ASSETS / "logo_cin.png", 8.62, 0.22, w=1.05)
    text(slide, 9.3, 5.25, 0.45, 0.25, str(number), size=10, color=MID_GRAY, align=PP_ALIGN.RIGHT)


def source_note(slide, txt, y=5.27, w=8.6):
    text(slide, MARGIN, y, w, 0.24, txt, size=8, color=MID_GRAY, italic=True)


def notes(slide, txt):
    slide.notes_slide.notes_text_frame.text = txt


# ---------------------------------------------------------------- template

def clone_slide(prs, src):
    """Duplica um slide do template (formas, imagens e plano de fundo)."""
    new = prs.slides.add_slide(src.slide_layout)
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    rid_map = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype.endswith("/slideLayout") or rel.reltype.endswith("/notesSlide"):
            continue
        if rel.is_external:
            rid_map[rid] = new.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        else:
            rid_map[rid] = new.part.relate_to(rel.target_part, rel.reltype)
    src_csld = src._element.cSld
    new_csld = new._element.cSld
    src_bg = src_csld.find(qn("p:bg"))
    if src_bg is not None:
        new_csld.insert(0, copy.deepcopy(src_bg))
    for el in src.shapes._spTree.iterchildren():
        if el.tag in (qn("p:nvGrpSpPr"), qn("p:grpSpPr")):
            continue
        new.shapes._spTree.append(copy.deepcopy(el))
    for el in new._element.iter():
        for attr in (qn("r:embed"), qn("r:id"), qn("r:link")):
            if el.get(attr) in rid_map:
                el.set(attr, rid_map[el.get(attr)])
    return new


def set_shape_text(shape, lines):
    """Troca o texto mantendo a formatação do primeiro run de cada parágrafo existente."""
    tf = shape.text_frame
    paras = list(tf.paragraphs)
    template_p = paras[0]._p
    for p in paras[1:]:
        p._p.getparent().remove(p._p)
    for i, line in enumerate(lines):
        if i == 0:
            p_el = template_p
        else:
            p_el = copy.deepcopy(template_p)
            template_p.getparent().append(p_el)
        runs = p_el.findall(qn("a:r"))
        for r in runs[1:]:
            p_el.remove(r)
        for br in p_el.findall(qn("a:br")):
            p_el.remove(br)
        runs[0].find(qn("a:t")).text = line


def delete_slide(prs, slide):
    sld_ids = prs.slides._sldIdLst
    for sld_id in list(sld_ids):
        if prs.part.related_part(sld_id.rId) is slide.part:
            prs.part.drop_rel(sld_id.rId)
            sld_ids.remove(sld_id)
            return


def move_slide(prs, slide, index):
    sld_ids = prs.slides._sldIdLst
    for sld_id in list(sld_ids):
        if prs.part.related_part(sld_id.rId) is slide.part:
            sld_ids.remove(sld_id)
            sld_ids.insert(index, sld_id)
            return


def emu(v):
    return Emu(int(v))
