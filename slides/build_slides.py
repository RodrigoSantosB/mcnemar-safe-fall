"""Gera a apresentação a partir do template oficial CIn-UFPE.

    python slides/make_figures.py   # figuras em results/figures/
    python slides/build_slides.py   # -> slides/apresentacao_mcnemar_safe_fall.pptx
"""

from __future__ import annotations

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

from pptx_helpers import (
    ASSETS, BORDER, DARK_RED, FIGS, GRAY, LIGHT, MARGIN, MID_GRAY, MONO_FONT, NAVY, ORANGE, RED, ROOT,
    SAND, TEAL, TEXT, TITLE_FONT, WHITE, LABEL_FONT, arrow, badge, bullets, callout, card, chevron,
    clone_slide, content_chrome, delete_slide, notes, picture, rect, set_shape_text, source_note,
    table, text,
)

TEMPLATE = ROOT / "templates" / "template_cin_ufpe.pptx"
OUTPUT = ROOT / "slides" / "apresentacao_mcnemar_safe_fall.pptx"
ARTICLE = "DelCastillo-Andrés et al. (2018). Int. J. Environ. Res. Public Health 15:2669. doi:10.3390/ijerph15122669 (CC BY 4.0)"

prs = Presentation(TEMPLATE)
template_slides = list(prs.slides)
SECTION_TPL = template_slides[3]   # divisória vermelha com caixa branca e grafismo
CLOSING_TPL = template_slides[12]  # "Muito obrigado!"
BLANK = next(l for l in prs.slide_layouts if l.name == "BLANK")

counter = {"n": 0}


def new_slide():
    counter["n"] += 1
    return prs.slides.add_slide(BLANK), counter["n"]


def section_slide(block, title, topics):
    s = clone_slide(prs, SECTION_TPL)
    counter["n"] += 1
    shapes = {sh.name: sh for sh in s.shapes}
    set_shape_text(shapes["Google Shape;77;p16"], [title])
    for r in shapes["Google Shape;77;p16"].text_frame.paragraphs[0].runs:
        r.font.size = Pt(26)
    set_shape_text(shapes["Google Shape;78;p16"], [block])
    y = 2.35
    for i, t in enumerate(topics):
        badge(s, 4.55, y + i * 0.55, 0.36, f"{i + 1:02d}", fill=WHITE, color=RED, size=10.5)
        text(s, 5.05, y + i * 0.55 - 0.02, 4.4, 0.4, t, size=14, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.3, 5.25, 0.45, 0.25, str(counter["n"]), size=10, color=WHITE, align=PP_ALIGN.RIGHT)
    return s


# =============================================================== 1. Capa
s, n = new_slide()
rect(s, 0, 0, 10, 5.625, fill=RED)
text(s, 0.85, 1.25, 8.4, 1.0, "O teste exato de McNemar", size=36, color=WHITE, bold=True, font=LABEL_FONT,
     anchor=MSO_ANCHOR.BOTTOM)
text(s, 0.85, 2.25, 8.4, 0.95,
     "Mudanças pareadas em respostas dicotômicas — aplicação ao programa Safe Fall",
     size=20, color=WHITE, bold=True, font=LABEL_FONT)
text(s, 0.85, 3.2, 8.4, 0.35,
     "Artigo-base: DelCastillo-Andrés et al. (2018), Int. J. Environ. Res. Public Health 15:2669",
     size=11.5, color=WHITE, italic=True)
text(s, 3.2, 3.85, 5.2, 0.6, ["Rodrigo Santos Batista", "rsb6"], size=13, color=WHITE, bold=True,
     font=LABEL_FONT, align=PP_ALIGN.CENTER, spacing=6)
picture(s, ASSETS / "logo_cin_ufpe_branco.png", 0.85, 4.55, w=2.5)
notes(s, "Apresentação em três blocos: fundamentos do teste exato de McNemar, sua aplicação no estudo Safe Fall "
         "e uma demonstração prática em Python (notebook 01_mcnemar_safe_fall.ipynb).")

# =============================================================== 2. Sumário
s, n = new_slide()
text(s, 0.6, 0.3, 5, 0.6, "Sumário", size=26, color=RED, bold=True, font=TITLE_FONT)
picture(s, ASSETS / "logo_cin.png", 8.62, 0.22, w=1.05)
items = [
    ("Bloco I — Fundamentação", "Dados pareados, tabela 2×2, hipóteses, cálculo exato e interpretação."),
    ("Bloco II — O estudo Safe Fall", "122 crianças, cinco respostas motoras, pré e pós-intervenção."),
    ("McNemar no artigo", "Por que o teste é adequado, Tabela 1 conferida e limitações."),
    ("Bloco III — Python", "Notebook reprodutível, demonstração interativa e testes automatizados."),
    ("Outro contexto e conclusões", "Avaliação de aprendizagem: mesma estrutura estatística."),
]
for i, (h, d) in enumerate(items):
    col, row = (0, i) if i < 3 else (1, i - 3)
    x, y = 0.6 + col * 4.6, 1.3 + row * 1.25
    text(s, x, y, 0.75, 0.6, f"{i + 1:02d}", size=26, color=RED, bold=True, font=TITLE_FONT)
    text(s, x + 0.85, y + 0.02, 3.5, 0.3, h, size=13.5, color=NAVY, bold=True)
    text(s, x + 0.85, y + 0.34, 3.5, 0.6, d, size=10.5, color=GRAY)
text(s, 9.3, 5.25, 0.45, 0.25, str(n), size=10, color=MID_GRAY, align=PP_ALIGN.RIGHT)

# =============================================================== 3. Bloco I
section_slide("Bloco I", "Fundamentação estatística",
              ["O problema dos dados pareados", "Tabela 2×2 e pares discordantes", "Teste exato e interpretação"])

# =============================================================== 4. Problema
s, n = new_slide()
content_chrome(s, "Introdução", "O treinamento mudou o comportamento do grupo?", n)
flow = [("Observação", "pré-teste"), ("Intervenção", "treinamento"), ("Nova observação", "pós-teste")]
for i, (h, d) in enumerate(flow):
    chevron(s, 0.5 + i * 1.62, 1.35, 1.75, 0.62, h, fill=[GRAY, RED, TEAL][i], size=11, first=(i == 0))
    text(s, 0.5 + i * 1.62, 2.0, 1.75, 0.3, d, size=10, color=GRAY, italic=True, align=PP_ALIGN.CENTER)
bullets(s, 0.5, 2.5, 4.9, 1.6, [
    "Uma escola avalia se cada aluno executa um movimento corretamente.",
    "Os mesmos alunos são observados antes e depois do treinamento.",
    "Cada observação é dicotômica: correto ou incorreto.",
], size=12.5, spacing=8)
callout(s, 0.5, 4.2, 4.9, 0.85, "A pergunta:",
        "a proporção de acertos mudou além do que o acaso explicaria?", size=12.5)
# tabela de mudanças individuais
card(s, 5.75, 1.3, 3.75, 3.75)
text(s, 5.95, 1.4, 3.4, 0.3, "Mudanças individuais (exemplo)", size=11.5, color=TEAL, bold=True)
rows = [["Aluno", "Pré", "Pós", "Transição"],
        ["Ana", "✗", "✓", "melhorou"], ["Bruno", "✓", "✓", "manteve"], ["Caio", "✗", "✓", "melhorou"],
        ["Davi", "✓", "✗", "piorou"], ["Eva", "✗", "✗", "manteve"], ["Fábio", "✗", "✓", "melhorou"]]
hl = {}
for r in range(1, len(rows)):
    hl[(r, 3)] = TEAL if rows[r][3] == "melhorou" else RED if rows[r][3] == "piorou" else GRAY
table(s, 5.95, 1.8, 3.35, 2.45, rows, col_widths=[0.85, 0.6, 0.6, 1.3], size=11, highlight=hl)
text(s, 5.95, 4.35, 3.35, 0.6, "Só quem muda de categoria informa sobre o efeito; quem “manteve” não distingue as hipóteses.",
     size=10, color=GRAY, italic=True)
notes(s, "Comece com a intuição: comparar duas porcentagens não basta, porque são as mesmas pessoas. "
         "O que interessa é quem mudou e em que direção.")

# =============================================================== 5. O que é / quando usar
s, n = new_slide()
content_chrome(s, "Fundamentação", "O que é o teste de McNemar — e quando usá-lo", n)
defs = [
    ("Amostras pareadas", "Cada indivíduo é medido duas vezes (ou pares casados). As medidas não são independentes."),
    ("Variável dicotômica", "Duas categorias por medida: correto/incorreto, sim/não, presente/ausente."),
    ("Não paramétrico", "Não supõe normalidade nem parâmetros populacionais contínuos: trabalha com contagens."),
]
for i, (h, d) in enumerate(defs):
    y = 1.3 + i * 1.05
    badge(s, 0.5, y + 0.1, 0.5, "abc"[i], fill=[RED, TEAL, ORANGE][i], size=15)
    text(s, 1.15, y, 3.6, 0.3, h, size=13, color=NAVY, bold=True)
    text(s, 1.15, y + 0.32, 3.6, 0.65, d, size=10.5, color=TEXT)
text(s, 0.5, 4.5, 4.3, 0.6,
     [[("Objetivo: ", {"bold": True, "color": RED}),
       "testar a homogeneidade marginal — se P(correto) é igual antes e depois — usando apenas os pares que mudaram."]],
     size=10.5)
# fluxograma de decisão
card(s, 5.05, 1.25, 4.45, 3.9)
text(s, 5.25, 1.32, 4, 0.3, "Fluxograma de decisão", size=11.5, color=TEAL, bold=True)
def qbox(x, y, w, t, fill=LIGHT, color=NAVY, bold=False):
    rect(s, x, y, w, 0.5, fill=fill, radius=0.15)
    text(s, x, y, w, 0.5, t, size=10, color=color, bold=bold, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
qbox(5.25, 1.7, 2.35, "Mesmos indivíduos em 2 momentos?")
qbox(5.25, 2.6, 2.35, "Resposta com 2 categorias?")
qbox(5.25, 3.5, 2.35, "Teste de McNemar", fill=RED, color=WHITE, bold=True)
qbox(7.85, 1.7, 1.5, "χ² / 2 proporções independentes", fill=WHITE)
qbox(7.85, 2.6, 1.5, "Stuart-Maxwell / Bowker", fill=WHITE)
qbox(7.85, 3.5, 1.5, "> 2 momentos: Q de Cochran", fill=WHITE)
for y in (2.22, 3.12):
    rect(s, 6.4, y, 0.05, 0.36, fill=MID_GRAY)
    text(s, 6.5, y + 0.02, 0.5, 0.3, "sim", size=9, color=TEAL, bold=True)
for y in (1.9, 2.8):
    arrow(s, 7.62, y + 0.02, 0.2, 0.14)
    text(s, 7.55, y - 0.2, 0.4, 0.2, "não", size=9, color=RED, bold=True)
text(s, 5.25, 4.12, 4.1, 0.95,
     [[("Exato × assintótico: ", {"bold": True, "color": NAVY}),
       "o exato usa a distribuição binomial dos pares discordantes; a versão χ² é uma aproximação "
       "para muitos pares."]], size=10)
notes(s, "Diferença central para o qui-quadrado de independência: aqui as duas medidas vêm do mesmo indivíduo.")

# =============================================================== 6. Tabela 2×2
s, n = new_slide()
content_chrome(s, "Fundamentação", "A tabela de contingência 2 × 2 pareada", n)
picture(s, FIGS / "matriz_generica.png", 0.45, 1.2, w=4.3, h=3.9)
items6 = [
    [("a", {"bold": True, "italic": True}), " — continuou correto"],
    [("b", {"bold": True, "italic": True, "color": RED}), " — passou de correto para incorreto (piorou)"],
    [("c", {"bold": True, "italic": True, "color": TEAL}), " — passou de incorreto para correto (melhorou)"],
    [("d", {"bold": True, "italic": True}), " — continuou incorreto"],
]
bullets(s, 5.0, 1.3, 4.5, 1.6, items6, size=12.5, spacing=6)
card(s, 5.0, 2.95, 4.5, 1.05, accent=TEAL)
text(s, 5.25, 3.0, 4.15, 0.95,
     [[("Pares discordantes b e c ", {"bold": True, "color": TEAL}),
       "são a única informação usada pela estatística de McNemar."],
      [("a e d", {"bold": True}), " (concordantes) não alteram o p-valor."]], size=11.5, spacing=4)
callout(s, 5.0, 4.15, 4.5, 0.9, "Por quê?",
        "pós − pré = (a+c) − (a+b) = c − b. A mudança nas proporções depende só de b e c.", size=11.5)
notes(s, "Mostre que a cancela: proporção correta no pré = (a+b)/N, no pós = (a+c)/N; a diferença é (c-b)/N.")

# =============================================================== 7. Hipóteses e mecanismo
s, n = new_slide()
content_chrome(s, "Fundamentação", "Hipóteses e funcionamento do teste exato", n)
card(s, 0.5, 1.25, 4.3, 1.75, accent=RED)
text(s, 0.75, 1.32, 4.0, 1.65, [
    [("H₀: ", {"bold": True, "color": RED}), "P(incorreto → correto) = P(correto → incorreto)"],
    [("H₁: ", {"bold": True, "color": RED}), "essas probabilidades são diferentes (bilateral)"],
    [("Equivalente: ", {"bold": True, "color": NAVY}), "P(correto no pré) = P(correto no pós) — homogeneidade marginal."],
    [("α = 0,05", {"bold": True, "color": NAVY}), ", como no artigo."],
], size=11.5, spacing=5)
card(s, 0.5, 3.15, 4.3, 1.95, accent=TEAL)
text(s, 0.75, 3.2, 4.0, 0.3, "Lógica do teste exato", size=12, color=TEAL, bold=True)
text(s, 0.75, 3.52, 4.0, 1.55, [
    "Sob H₀, cada par discordante é “piorou” ou “melhorou” com chance ½ — como uma moeda honesta.",
    "Condicionando a n = b + c pares discordantes:",
], size=11, spacing=4)
picture(s, FIGS / "formula_binomial.png", 0.75, 4.55, w=3.9, h=0.32)
# fórmulas
rect(s, 5.1, 1.25, 4.4, 1.55, fill=NAVY, radius=0.06)
text(s, 5.3, 1.3, 4.0, 0.3, "P-valor exato bilateral", size=11.5, color=SAND, bold=True)
picture(s, FIGS / "formula_p_exato.png", 5.3, 1.6, w=4.0, h=0.6)
text(s, 5.3, 2.2, 4.0, 0.55, "Regra de cauda: dobrar a cauda menor (distribuição simétrica ⇒ igual a somar "
     "as probabilidades ≤ à do valor observado).", size=9.5, color=WHITE)
rect(s, 5.1, 2.95, 4.4, 1.25, fill=LIGHT, radius=0.06)
text(s, 5.3, 3.0, 4.0, 0.3, "Aproximação assintótica (outro procedimento)", size=11.5, color=NAVY, bold=True)
picture(s, FIGS / "formula_chi2.png", 5.3, 3.3, w=4.0, h=0.5)
text(s, 5.3, 3.77, 4.0, 0.4, "“− 1” = correção de continuidade (Edwards); sem ela: (b − c)²/(b + c).",
     size=9.5, color=GRAY)
text(s, 5.1, 4.35, 4.4, 0.75,
     [[("Estatística do exato: ", {"bold": True, "color": RED}),
       "min(b, c) — convenção do statsmodels. O p-valor vem da binomial, não da curva χ²."]], size=10.5)
notes(s, "Insistir: o teste exato e o qui-quadrado de McNemar são procedimentos diferentes; o qui-quadrado aproxima a binomial.")

# =============================================================== 8. Exemplo resolvido
s, n = new_slide()
content_chrome(s, "Fundamentação", "Exemplo resolvido: b = 2, c = 10", n)
steps = [
    ("1", "Pares discordantes", "n = b + c = 2 + 10 = 12"),
    ("2", "Distribuição sob H₀", "B ~ Binomial(12 ; 0,5)"),
    ("3", "Cauda menor: C(12,0) + C(12,1) + C(12,2) = 1 + 12 + 66", "P(B ≤ 2) = 79 / 4096 = 0,0193"),
    ("4", "Bilateral", "p = 2 × 0,0193 = 0,0386"),
    ("5", "Decisão", "0,0386 < 0,05 ⇒ rejeita H₀"),
]
for i, (k, h, d) in enumerate(steps):
    y = 1.28 + i * 0.66
    badge(s, 0.5, y + 0.05, 0.42, k, fill=RED if i < 4 else TEAL, size=12)
    text(s, 1.05, y, 3.6, 0.28, h, size=11, color=GRAY, bold=True)
    text(s, 1.05, y + 0.26, 3.7, 0.35, d, size=12.5, color=NAVY, bold=(i == 4), font=TITLE_FONT)
picture(s, FIGS / "binomial_b2_c10.png", 4.85, 1.25, w=4.7, h=2.6)
callout(s, 4.95, 4.05, 4.55, 1.0, "Leitura:",
        "se o treino não tivesse efeito, um desequilíbrio de 10 contra 2 (ou mais extremo) ocorreria em ~3,9 % das vezes.",
        size=11)
notes(s, "Faça a conta no quadro. C(12,0)=1, C(12,1)=12, C(12,2)=66; 2^12=4096.")

# =============================================================== 9. Interpretação
s, n = new_slide()
content_chrome(s, "Interpretação", "Significativo ou não? O desequilíbrio entre b e c decide", n)
picture(s, FIGS / "exemplo_sig.png", 0.45, 1.2, w=5.6, h=1.9)
picture(s, FIGS / "exemplo_nsig.png", 0.45, 3.2, w=5.6, h=1.9)
card(s, 6.25, 1.25, 3.25, 1.75, accent=TEAL)
text(s, 6.5, 1.3, 2.95, 1.7, [
    [("Significativo", {"bold": True, "color": TEAL})],
    "c = 10 × b = 2 (n = 12)",
    [("p = 0,039 < 0,05", {"bold": True})],
    "Mais alunos melhoraram do que pioraram.",
], size=11, spacing=3)
card(s, 6.25, 3.2, 3.25, 1.2, accent=MID_GRAY)
text(s, 6.5, 3.25, 2.95, 1.15, [
    [("Não significativo", {"bold": True, "color": GRAY})],
    "c = 9 × b = 5 (n = 14)",
    [("p = 0,424", {"bold": True}), " — compatível com acaso."],
], size=11, spacing=3)
rect(s, 6.25, 4.5, 3.25, 0.62, fill=NAVY, radius=0.08)
text(s, 6.4, 4.5, 3.0, 0.62, [[("Evidência ≠ efeito prático: ", {"bold": True, "color": SAND}),
                              ("relate também c − b em p.p. e a razão c/b.", {"color": WHITE})]],
     size=10, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Mesma ideia, dois resultados. Pares concordantes (a=20, d≈6-8) são idênticos; o que muda é b versus c.")

# =============================================================== 10. Exato x assintótico
s, n = new_slide()
content_chrome(s, "Interpretação", "Teste exato × aproximação qui-quadrado", n)
picture(s, FIGS / "exato_vs_assintotico.png", 0.45, 1.2, w=5.4, h=2.9)
table(s, 6.05, 1.35, 3.45, 1.5, [
    ["b = 1, c = 7", "estat.", "p"],
    ["Exato (binomial)", "min = 1", "0,070"],
    ["χ² sem correção", "4,50", "0,034"],
    ["χ² com correção", "3,13", "0,077"],
], col_widths=[1.45, 0.95, 1.05], size=10.5, highlight={(2, 2): RED, (1, 2): TEAL})
text(s, 6.05, 2.95, 3.45, 1.1,
     "Com só 8 pares discordantes, o χ² sem correção rejeitaria H₀; o exato não. As faixas laranja marcam essas divergências.",
     size=10.5, color=TEXT)
callout(s, 0.5, 4.25, 9.0, 0.82, "Regra prática:",
        "com poucos pares discordantes (b + c < 25, regra usual) use o exato — ele é sempre válido. "
        "Com dezenas de pares, os métodos convergem.", size=11.5)
notes(s, "O artigo declara 'McNemar's exact test' e imprime um X²; com 50 a 106 pares discordantes as conclusões coincidem.")

# =============================================================== 11. Bloco II
section_slide("Bloco II", "O estudo Safe Fall",
              ["Contexto e desenho quase experimental", "As cinco respostas motoras", "McNemar aplicado à Tabela 1"])

# =============================================================== 12. Artigo / contexto
s, n = new_slide()
content_chrome(s, "O artigo", "Ensinar crianças a cair para trás com segurança", n)
text(s, 0.5, 1.2, 5.0, 0.75,
     [[("Children’s Improvement of a Motor Response during Backward Falls through the Implementation of a Safe Fall Program",
        {"italic": True, "color": NAVY, "bold": True})],
      [("DelCastillo-Andrés, Toronjo-Hornillo, Rodríguez-López, Castañeda-Vázquez & Campos-Mesa · IJERPH, 2018",
        {"size": 9.5, "color": GRAY})]], size=11.5, spacing=3)
facts = [("122", "crianças"), ("10–12", "anos"), ("Sevilha", "escolas públicas"),
         ("5", "respostas motoras"), ("2", "momentos: pré e pós"), ("6", "semanas (2017)")]
for i, (big, small) in enumerate(facts):
    x, y = 0.5 + (i % 3) * 1.68, 2.15 + (i // 3) * 1.05
    card(s, x, y, 1.55, 0.92)
    text(s, x, y + 0.06, 1.55, 0.45, big, size=20, color=RED, bold=True, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    text(s, x, y + 0.52, 1.55, 0.35, small, size=10, color=GRAY, align=PP_ALIGN.CENTER)
text(s, 0.5, 4.3, 5.0, 0.8,
     [[("Motivação: ", {"bold": True, "color": RED}),
       "a OMS aponta quedas como 2ª causa de morte por lesão não intencional em crianças; quedas para trás, "
       "embora menos frequentes, causam as lesões mais graves."]], size=10.5)
picture(s, ASSETS / "artigo_fig1-000.png", 5.75, 1.25, w=3.75)
text(s, 5.75, 2.15, 3.75, 0.3, "Figura 1 do artigo — Safe Fall em aulas de Educação Física.",
     size=9, color=GRAY, italic=True)
card(s, 5.75, 2.55, 3.75, 1.2, accent=ORANGE)
text(s, 6.0, 2.6, 3.45, 1.15, [
    [("Desenho: ", {"bold": True, "color": NAVY}), "piloto exploratório, quase experimental, sem grupo controle."],
    [("Não é ", {"bold": True, "color": RED}), "um ensaio clínico randomizado."],
], size=10.5, spacing=4)
card(s, 5.75, 3.9, 3.75, 1.2, accent=TEAL)
text(s, 6.0, 3.95, 3.45, 1.15, [
    [("Desfecho: ", {"bold": True, "color": TEAL}), "resposta motora observada (correta/incorreta) numa queda para trás provocada."],
    [("Análise: ", {"bold": True, "color": NAVY}), "McNemar exato no SPSS 24, α = 0,05."],
], size=10.5, spacing=4)
source_note(s, "Fonte: " + ARTICLE)

# =============================================================== 13. Desenho / linha do tempo
s, n = new_slide()
content_chrome(s, "Metodologia", "Desenho do estudo: as mesmas crianças, antes e depois", n)
steps = [("Aula teórica", "1 h — quedas na infância", GRAY), ("Pré-teste", "INFOSECA", NAVY),
         ("Aula prática", "50 min de Safe Fall", RED), ("10 sessões", "10 min no aquecimento", RED),
         ("Pós-teste", "INFOSECA", TEAL)]
rect(s, 0.6, 1.83, 8.8, 0.05, fill=BORDER)
for i, (h, d, col) in enumerate(steps):
    x = 0.5 + i * 1.8
    badge(s, x + 0.62, 1.6, 0.5, str(i + 1), fill=col, size=13)
    text(s, x, 2.15, 1.75, 0.3, h, size=12, color=col, bold=True, align=PP_ALIGN.CENTER)
    text(s, x, 2.43, 1.75, 0.3, d, size=9.5, color=GRAY, align=PP_ALIGN.CENTER)
text(s, 0.5, 1.2, 9, 0.3, "24 de abril a 2 de junho de 2017 · aulas de Educação Física · tapete de espuma com sistema de absorção",
     size=10, color=GRAY, italic=True, align=PP_ALIGN.CENTER)
picture(s, ASSETS / "artigo_infoseca-000.png", 0.5, 2.95, w=2.6, h=2.1)
text(s, 0.5, 5.05, 2.6, 0.25, "Posição inicial do teste (Apêndice A do artigo)", size=8, color=GRAY, italic=True,
     align=PP_ALIGN.CENTER)
card(s, 3.3, 2.95, 3.0, 2.15, accent=TEAL)
text(s, 3.55, 3.0, 2.7, 2.1, [
    [("Coleta", {"bold": True, "color": TEAL})],
    "Amostragem por conveniência.",
    "Escala INFOSECA: 5 critérios, cada um sim/não.",
    "Concordância (Kappa) 0,75 a 0,98.",
    "Registro dicotômico ⇒ uma tabela 2×2 por critério.",
], size=10.5, spacing=3)
card(s, 6.5, 2.95, 3.0, 2.15, accent=ORANGE)
text(s, 6.75, 3.0, 2.7, 2.1, [
    [("Cuidados e limites", {"bold": True, "color": ORANGE})],
    "Sem grupo controle nem randomização.",
    "No pós-teste a queda é mais previsível (familiaridade).",
    "Avaliadores sabiam o momento da medida.",
    "Ambiente de laboratório, só queda para trás.",
], size=10.5, spacing=3)

# =============================================================== 14. Cinco respostas
s, n = new_slide()
content_chrome(s, "Variáveis", "As cinco respostas motoras avaliadas (INFOSECA)", n)
picture(s, FIGS / "esquema_respostas.png", 0.9, 1.12, w=8.2, h=1.82)
resp = [
    ("Flexão do pescoço", "Queixo em direção ao peito", "Proteger a cabeça do impacto", "κ = 0,93"),
    ("Não apoiar as mãos", "Mãos e cotovelos fora do chão", "Evitar lesões de punho e braço", "κ = 0,98"),
    ("Enrolamento", "Rolar sobre as costas arredondadas", "Distribuir a energia do impacto", "κ = 0,75"),
    ("Flexão do quadril", "Manter o agrupamento inicial", "Não elevar o centro de gravidade", "κ = 0,82"),
    ("Flexão dos joelhos", "Manter joelhos flexionados", "Idem; queda mais baixa e controlada", "κ = 0,84"),
]
for i, (h, desc, goal, kappa) in enumerate(resp):
    x = 0.5 + i * 1.82
    card(s, x, 3.0, 1.72, 2.1)
    badge(s, x + 0.1, 3.1, 0.36, str(i + 1), fill=TEAL, size=11)
    text(s, x + 0.5, 3.07, 1.2, 0.45, h, size=10.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.1, 3.58, 1.55, 1.5, [
        desc,
        [("Objetivo: ", {"bold": True, "color": TEAL}), goal],
        [("Correto = sim · incorreto = não", {"size": 8.5, "color": GRAY})],
        [(kappa, {"size": 8.5, "color": GRAY, "italic": True})],
    ], size=9.5, spacing=3)
source_note(s, "Esquema conceitual elaborado para fins didáticos a partir da descrição da escala INFOSECA (Apêndice A); não é instrução de execução sem supervisão.")

# =============================================================== 15. Por que McNemar
s, n = new_slide()
content_chrome(s, "McNemar no artigo", "Por que o teste de McNemar é adequado aqui?", n)
reasons = ["Mesmas 122 crianças", "Duas observações por criança", "Uma variável dicotômica por comportamento",
           "Interesse nas mudanças individuais", "Comparar proporções marginais pareadas"]
for i, r in enumerate(reasons):
    y = 1.3 + i * 0.6
    badge(s, 0.5, y, 0.38, "✓", fill=TEAL, size=13)
    text(s, 1.0, y - 0.02, 3.4, 0.42, r, size=12, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.5, 4.38, 3.9, 0.7, fill=RED, radius=0.1)
text(s, 0.5, 4.38, 3.9, 0.7, "⇒ McNemar, um teste por comportamento", size=13, color=WHITE, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
card(s, 4.75, 1.25, 4.75, 3.85, accent=RED)
text(s, 5.0, 1.3, 4.4, 0.3, "E se usássemos o χ² de independência?", size=12.5, color=RED, bold=True)
table(s, 5.0, 1.72, 4.3, 0.95, [
    ["Pescoço, tratado como 2 grupos", "Correto", "Incorreto"],
    ["“Grupo” pré", "28", "94"],
    ["“Grupo” pós", "110", "12"],
], col_widths=[2.1, 1.1, 1.1], size=10)
bullets(s, 5.0, 2.8, 4.35, 2.3, [
    "Conta 244 observações, mas são só 122 crianças: viola a independência.",
    "Ignora quem mudou: não distingue 84 melhoras + 2 pioras de 82 melhoras + 0 pioras.",
    "Testa outra pergunta (associação momento × resposta), com erro-padrão errado.",
    [("Resultado: χ² = 112,2 contra χ²", {}), ("McNemar", {"size": 8}), (" = 76,3 — números não comparáveis.", {})],
], size=10.5, spacing=5)
notes(s, "O qui-quadrado de independência só seria válido para grupos distintos de crianças.")

# =============================================================== 16. Resultados publicados
s, n = new_slide()
content_chrome(s, "Resultados publicados", "Mais crianças passaram a cair de forma protegida", n)
picture(s, FIGS / "pre_post_publicado.png", 0.4, 1.15, w=6.3, h=3.4)
card(s, 6.9, 1.25, 2.6, 2.05, accent=RED)
text(s, 7.12, 1.3, 2.33, 2.0, [
    [("Achados", {"bold": True, "color": RED})],
    "Ganhos de +39 a +87 p.p.",
    "Pós-teste: 87–95 % de respostas corretas.",
    "McNemar significativo nas cinco respostas.",
], size=10.5, spacing=4)
card(s, 6.9, 3.42, 2.6, 1.68, accent=NAVY)
text(s, 7.12, 3.47, 2.33, 1.62, [
    [("“p = 0,000” ", {"bold": True, "color": NAVY}), "na tabela"],
    "é arredondamento de 3 casas — uma probabilidade nunca é zero.",
    [("Relatar: p < 0,001", {"bold": True, "color": TEAL})],
], size=10.5, spacing=4)
callout(s, 0.5, 4.62, 6.2, 0.5, "Atenção:", "% recalculadas como contagem/122 (ver auditoria a seguir).", size=10.5)
source_note(s, "Dados: Tabela 1 de " + ARTICLE)

# =============================================================== 17. Auditoria Tabela 1
s, n = new_slide()
content_chrome(s, "Conferência", "Tabela 1 conferida: valores publicados × recalculados", n)
data = [["Comportamento", "Pré: n (% impressa)", "% = n/122", "Pós: n (% impressa)", "% = n/122", "X²", "p"],
        ["Flexão do pescoço", "28 (23,6)", "22,9", "110 (90,2)", "90,2", "76,291", "0,000"],
        ["Não apoiar as mãos", "1 (1,6)", "0,8", "107 (90,2)", "87,7", "104,009", "0,000"],
        ["Enrolamento corporal", "9 (8,1)", "7,4", "111 (91,1)", "91,0", "96,236", "0,000"],
        ["Flexão do quadril", "1 (1,6)", "0,8", "106 (87)", "86,9", "103,010", "0,000"],
        ["Flexão dos joelhos", "68 (56,1)", "55,7", "116 (95,1)", "95,1", "42,481", "0,000"]]
hl = {(1, 2): RED, (2, 2): RED, (3, 2): RED, (4, 2): RED, (5, 2): RED, (2, 4): RED, (3, 4): ORANGE}
table(s, 0.5, 1.25, 9.0, 2.15, data, col_widths=[1.85, 1.55, 1.05, 1.55, 1.05, 1.0, 0.95], size=10.5, highlight=hl)
items = [
    [("Pré-teste: ", {"bold": True, "color": RED}),
     "nenhuma % de “correto” bate com n/122 (ex.: 1 criança impressa como 1,6 %; o texto diz 0,8 %)."],
    [("Mãos, pós-teste: ", {"bold": True, "color": RED}),
     "107 impresso como 90,2 % — o correto é 87,7 %; repete os % da linha do pescoço (provável erro de cópia)."],
    [("Enrolamento, pós: ", {"bold": True, "color": ORANGE}), "91,1 % vs 91,0 % (diferença pequena)."],
    [("Coerente: ", {"bold": True, "color": TEAL}), "contagens somam 122 em todas as linhas; quadril e joelhos no pós batem."],
]
bullets(s, 0.5, 3.55, 9.0, 1.6, items, size=10.5, spacing=4)
source_note(s, "Valores impressos preservados sem correção; recálculo em safe_fall_statistics.data_validation.audit_table1.")

# =============================================================== 18. Do X² às tabelas 2x2
s, n = new_slide()
content_chrome(s, "McNemar no artigo", "As margens não bastam — mas o X² publicado revela b e c", n)
text(s, 0.5, 1.2, 4.4, 0.9, [
    [("Margens fixam só ", {}), ("c − b", {"bold": True, "color": NAVY}), (" = pós − pré.", {})],
    [("Pescoço: c − b = 110 − 28 = 82, mas b pode ir de 0 a 12.", {"color": GRAY, "size": 10.5})],
], size=11.5, spacing=3)
rect(s, 0.5, 2.05, 4.4, 1.05, fill=NAVY, radius=0.06)
text(s, 0.65, 2.08, 4.1, 0.3, "Se X² = McNemar com correção de continuidade:", size=10.5, color=SAND, bold=True)
picture(s, FIGS / "formula_inversao.png", 0.65, 2.4, w=4.1, h=0.62)
table(s, 0.5, 3.2, 4.4, 1.9, [
    ["Comportamento", "b + c", "b", "c", "p exato"],
    ["Pescoço", "86,000", "2", "84", "< 0,001"],
    ["Mãos", "106,000", "0", "106", "< 0,001"],
    ["Enrolamento", "106,000", "2", "104", "< 0,001"],
    ["Quadril", "105,000", "0", "105", "< 0,001"],
    ["Joelhos", "52,000", "2", "50", "< 0,001"],
], col_widths=[1.3, 0.85, 0.5, 0.6, 1.15], size=10, highlight={(r, 2): RED for r in range(1, 6)} | {(r, 3): TEAL for r in range(1, 6)})
picture(s, FIGS / "fluxo_pescoco_inferido.png", 5.1, 1.15, w=4.4, h=2.55)
card(s, 5.1, 3.8, 4.4, 1.3, accent=ORANGE)
text(s, 5.35, 3.83, 4.1, 1.25, [
    [("Teste da hipótese: ", {"bold": True, "color": ORANGE}),
     "b + c sai inteiro nas 5 linhas e o X² é reproduzido até a 3ª casa; sem correção, nenhuma linha fecha."],
    [("Tabelas INFERIDAS, ", {"bold": True, "color": RED}), "não publicadas. p exatos entre 10⁻³² e 10⁻¹²."],
], size=10, spacing=4)
source_note(s, "Inferência algébrica a partir da Tabela 1 (safe_fall_statistics.reconstruction); microdados não disponíveis.")
notes(s, "Ponto alto: o SPSS reporta o qui-quadrado corrigido para McNemar. Invertendo a fórmula recuperamos b+c.")

# =============================================================== 19. Limitações
s, n = new_slide()
content_chrome(s, "Leitura crítica", "Limitações: o que o estudo mostra — e o que não mostra", n)
lims = [
    ("Sem randomização nem grupo controle", "Maturação, aprendizagem com o teste e expectativa do avaliador não são separadas do efeito do programa."),
    ("Amostra por conveniência", "Escolas de Sevilha, 10–12 anos: generalização limitada a outras idades e contextos."),
    ("Familiaridade com o teste", "No pós-teste a queda é mais previsível — o próprio artigo reconhece."),
    ("Comportamento ≠ lesão", "O desfecho é a resposta motora em ambiente controlado; redução de lesões não foi medida."),
    ("Reprodutibilidade", "Sem microdados nem tabelas 2×2; porcentagens inconsistentes na Tabela 1."),
    ("Teste ≠ magnitude", "p < 0,001 indica mudança, não seu tamanho; reportar diferenças e intervalos."),
]
for i, (h, d) in enumerate(lims):
    x, y = 0.5 + (i % 2) * 4.55, 1.25 + (i // 2) * 1.3
    card(s, x, y, 4.45, 1.18, accent=[RED, ORANGE, ORANGE, RED, NAVY, TEAL][i])
    text(s, x + 0.25, y + 0.06, 4.1, 0.3, h, size=11.5, color=NAVY, bold=True)
    text(s, x + 0.25, y + 0.38, 4.1, 0.78, d, size=10, color=TEXT)
text(s, 0.5, 5.15, 9, 0.3, "A conclusão segura: houve mudança estatisticamente significativa na resposta motora observada após o programa.",
     size=10.5, color=RED, bold=True, italic=True)

# =============================================================== 20. Bloco III
section_slide("Bloco III", "Demonstração em Python",
              ["Notebook reprodutível", "Demonstração interativa", "Outro contexto: educação"])

# =============================================================== 21. Notebook
s, n = new_slide()
content_chrome(s, "Implementação", "Notebook 01_mcnemar_safe_fall.ipynb", n)
etapas = ["Dados", "Exploração", "Tabela 2×2", "Hipóteses", "Cálculo manual", "Bibliotecas",
          "Exato × χ²", "Visualização", "Interpretação", "Comparação"]
for i, e in enumerate(etapas):
    x, y = 0.5 + (i % 5) * 1.0, 1.3 + (i // 5) * 0.62
    rect(s, x, y, 0.92, 0.5, fill=[NAVY, TEAL][i // 5], radius=0.12)
    text(s, x, y, 0.92, 0.5, [[(f"{i + 2}. ", {"bold": True, "color": SAND}), (e, {"color": WHITE})]],
         size=8.5, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.5, 2.65, 4.85, 1.75, fill=NAVY, radius=0.04)
code = [
    "from statsmodels.stats.contingency_tables import mcnemar",
    "from scipy.stats import binomtest",
    "",
    "tab = [[15, 3], [13, 9]]          # [[a, b], [c, d]]",
    "res = mcnemar(tab, exact=True)    # p = 0,0213",
    "binomtest(3, 3 + 13, 0.5).pvalue  # p = 0,0213 ✓",
]
text(s, 0.65, 2.72, 4.6, 1.65, code, size=9.5, color=WHITE, font=MONO_FONT, spacing=1)
text(s, 0.5, 4.5, 4.85, 0.6, [[("Validação tripla: ", {"bold": True, "color": TEAL}),
                               "cálculo manual (frações exatas), scipy e statsmodels concordam em todos os casos."]],
     size=10.5)
card(s, 5.6, 1.25, 3.9, 3.85)
text(s, 5.8, 1.3, 3.6, 0.3, "src/safe_fall_statistics/", size=11.5, color=RED, bold=True, font=MONO_FONT)
mods = [("data_loader", "Tabela 1 publicada"), ("data_validation", "auditoria e pares/ausentes"),
        ("contingency_tables", "PairedTable a, b, c, d"), ("mcnemar_analysis", "exato, χ², interpretação"),
        ("reconstruction", "inferência b, c via X²"), ("synthetic_data", "exemplos SINTÉTICOS"),
        ("visualizations", "gráficos no padrão visual"), ("interactive_demo", "widget b × c"),
        ("slide_examples", "exemplos dos slides ajustáveis")]
for i, (m, d) in enumerate(mods):
    y = 1.66 + i * 0.32
    text(s, 5.8, y, 1.75, 0.32, m + ".py", size=9, color=NAVY, bold=True, font=MONO_FONT)
    text(s, 7.6, y, 1.85, 0.32, d, size=9.5, color=GRAY)
text(s, 5.8, 4.62, 3.6, 0.4, [[("40 testes automatizados", {"bold": True, "color": TEAL}), " (pytest)"]], size=10.5)

# =============================================================== 22. Demo interativa
s, n = new_slide()
content_chrome(s, "Demonstração", "Demonstração interativa: mova b e c", n)
for i, (lab, val, col) in enumerate([("c — melhoraram (I→C)", 13, TEAL), ("b — pioraram (C→I)", 3, RED)]):
    y = 1.3 + i * 0.42
    text(s, 0.5, y, 1.9, 0.3, lab, size=10, color=NAVY, bold=True)
    rect(s, 2.45, y + 0.12, 2.6, 0.06, fill=BORDER)
    rect(s, 2.45, y + 0.12, 2.6 * val / 40, 0.06, fill=col)
    badge(s, 2.45 + 2.6 * val / 40 - 0.09, y + 0.06, 0.18, "", fill=col)
    text(s, 5.15, y, 0.4, 0.3, str(val), size=10.5, color=col, bold=True)
picture(s, FIGS / "demo_b3_c13.png", 0.45, 2.15, w=6.2, h=2.3)
text(s, 0.5, 4.5, 6.1, 0.6, "Saída do widget (ipywidgets) para b = 3, c = 13: tabela, nº de pares discordantes, estatística, "
     "p exato, binomial sob H₀ e interpretação — tudo se atualiza ao mover os controles.", size=10, color=GRAY, italic=True)
card(s, 6.85, 1.25, 2.65, 3.85, accent=TEAL)
text(s, 7.07, 1.3, 2.4, 0.3, "Experimente no Colab", size=11.5, color=TEAL, bold=True)
picture(s, FIGS / "qr_colab.png", 7.47, 1.62, w=1.45)
text(s, 7.07, 3.1, 2.4, 0.4, [[("github.com/RodrigoSantosB/", {"size": 8.5}), ("mcnemar-safe-fall", {"size": 8.5, "bold": True})]],
     size=8.5, color=NAVY, align=PP_ALIGN.CENTER, font=MONO_FONT)
text(s, 7.07, 3.5, 2.4, 1.6, [
    [("b = c: ", {"bold": True}), "p = 1 — sem evidência."],
    [("b = 3, c = 13: ", {"bold": True}), "p = 0,021."],
    [("Mude a e d: ", {"bold": True, "color": RED}), "o p-valor não muda."],
], size=10, spacing=4)
source_note(s, "Dados SINTÉTICOS. Notebook: Etapa 9a (este widget) e Etapa 12 (abas com todos os exemplos dos slides, ajustáveis).")

# =============================================================== 23. Variação do p-valor
s, n = new_slide()
content_chrome(s, "Demonstração", "Como o desequilíbrio entre b e c move o p-valor", n)
picture(s, FIGS / "pvalor_vs_c.png", 0.4, 1.2, w=5.9, h=3.3)
text(s, 0.5, 4.55, 5.8, 0.55, "Com n = 20 pares discordantes fixos, p < 0,05 só quando c ≤ 5 ou c ≥ 15.",
     size=10.5, color=GRAY, italic=True)
card(s, 6.55, 1.25, 2.95, 3.85, accent=RED)
text(s, 6.78, 1.3, 2.7, 3.8, [
    [("O que governa o p-valor", {"bold": True, "color": RED})],
    [("Desequilíbrio ", {"bold": True}), "|c − b|: quanto maior, menor o p."],
    [("Quantidade ", {"bold": True}), "b + c: o mesmo 75 % de melhoras é mais convincente com 40 pares do que com 8."],
    [("Ignorados: ", {"bold": True}), "a e d — mesmo que sejam milhares."],
    [("Safe Fall: ", {"bold": True, "color": TEAL}), "84 contra 2 (pescoço) fica muito além da região crítica."],
], size=10.5, spacing=6)
source_note(s, "Curva calculada com safe_fall_statistics.mcnemar_analysis.exact_pvalue_manual (exemplo teórico).")

# =============================================================== 24. Educação
s, n = new_slide()
content_chrome(s, "Outro contexto", "Mesma estrutura em educação: acertou a questão?", n)
picture(s, FIGS / "tabela_educacao_sintetico.png", 0.4, 1.2, w=2.8, h=2.5)
picture(s, FIGS / "fluxo_educacao_sintetico.png", 3.25, 1.2, w=3.3, h=2.5)
text(s, 0.5, 3.75, 6.0, 0.55,
     [[("40 alunos ", {"bold": True}), "respondem à mesma questão antes e depois de uma aula de reforço: "
       "13 passaram a acertar, 3 passaram a errar ⇒ p exato = 0,021."]], size=10.5)
source_note(s, "Dados SINTÉTICOS (exemplo didático), gerados por safe_fall_statistics.synthetic_data.", y=4.35, w=6)
table(s, 6.75, 1.3, 2.75, 3.0, [
    ["", "Safe Fall", "Educação"],
    ["Indivíduos", "122 crianças", "40 alunos"],
    ["Momentos", "pré / pós", "pré / pós"],
    ["Categoria", "correto / incorreto", "acertou / errou"],
    ["b (pioraram)", "2", "3"],
    ["c (melhoraram)", "84", "13"],
    ["Teste", "McNemar exato", "McNemar exato"],
], col_widths=[0.95, 0.95, 0.85], size=9, highlight={(4, 1): RED, (4, 2): RED, (5, 1): TEAL, (5, 2): TEAL})
text(s, 6.75, 4.35, 2.75, 0.3, "Safe Fall: pescoço, b e c inferidos", size=8, color=MID_GRAY, italic=True)
callout(s, 0.5, 4.65, 9.0, 0.5, "Ideia-chave:",
        "fenômenos diferentes, mesma estrutura — dados pareados, resposta dicotômica, foco nos discordantes.", size=11)

# =============================================================== 25. Conclusões
s, n = new_slide()
content_chrome(s, "Conclusões", "Síntese", n)
concl = [
    ("Teste certo para a pergunta", "Pré e pós nas mesmas crianças com resposta sim/não: McNemar compara proporções pareadas olhando só para b e c.", TEAL),
    ("Exato é sempre válido", "Binomial(b + c; 0,5). A aproximação χ² serve para muitos pares, mas pode mudar a conclusão com poucos.", RED),
    ("Safe Fall: mudança robusta", "84–106 melhoras contra 0–2 pioras; p < 0,001 em qualquer método. Conclusão do artigo se sustenta.", NAVY),
    ("Leitura crítica", "Quase experimento sem controle; desfecho é comportamento, não lesão; Tabela 1 com % inconsistentes.", ORANGE),
]
for i, (h, d, col) in enumerate(concl):
    y = 1.25 + i * 0.97
    card(s, 0.5, y, 9.0, 0.85, accent=col)
    badge(s, 0.75, y + 0.2, 0.45, str(i + 1), fill=col, size=13)
    text(s, 1.4, y + 0.06, 7.9, 0.3, h, size=12.5, color=NAVY, bold=True)
    text(s, 1.4, y + 0.38, 7.9, 0.45, d, size=10.5, color=TEXT)

# =============================================================== 26. Referências
s, n = new_slide()
content_chrome(s, "Referências", "Principais referências", n)
refs = [
    [("DelCastillo-Andrés, Ó.; Toronjo-Hornillo, L.; Rodríguez-López, M.; Castañeda-Vázquez, C.; Campos-Mesa, M.C. ", {}),
     ("Children’s Improvement of a Motor Response during Backward Falls through the Implementation of a Safe Fall Program. ", {"italic": True}),
     ("Int. J. Environ. Res. Public Health 2018, 15, 2669. doi:10.3390/ijerph15122669.", {})],
    [("McNemar, Q. ", {}), ("Note on the sampling error of the difference between correlated proportions or percentages. ", {"italic": True}),
     ("Psychometrika 1947, 12, 153–157.", {})],
    [("Edwards, A.L. ", {}), ("Note on the “correction for continuity” in testing the significance of the difference between correlated proportions. ", {"italic": True}),
     ("Psychometrika 1948, 13, 185–187.", {})],
    [("Agresti, A. ", {}), ("Categorical Data Analysis, ", {"italic": True}), ("3rd ed. Wiley, 2013 (cap. 11 — dados pareados).", {})],
    [("Fagerland, M.W.; Lydersen, S.; Laake, P. ", {}),
     ("The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional. ", {"italic": True}),
     ("BMC Med. Res. Methodol. 2013, 13, 91.", {})],
    [("Seabold, S.; Perktold, J. ", {}), ("statsmodels: Econometric and statistical modeling with Python. ", {"italic": True}),
     ("Proc. 9th Python in Science Conf., 2010.  ·  Virtanen, P. et al. SciPy 1.0. Nat. Methods 2020, 17, 261–272.", {})],
]
bullets(s, 0.5, 1.25, 9.0, 3.9, refs, size=10.5, spacing=7)

# =============================================================== 27. Encerramento (template)
closing = clone_slide(prs, CLOSING_TPL)

# remove os slides de exemplo do template original
for old in template_slides:
    delete_slide(prs, old)

prs.save(OUTPUT)
print(f"{len(prs.slides)} slides -> {OUTPUT}")
