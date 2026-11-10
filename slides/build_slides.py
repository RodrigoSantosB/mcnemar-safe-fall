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
notes(s, "Apresentação em três blocos: o teste de McNemar (roteiro e duas ilustrações), sua aplicação no estudo Safe Fall "
         "e uma demonstração prática em Python (notebook 01_mcnemar_safe_fall.ipynb).")

# =============================================================== 2. Sumário
s, n = new_slide()
text(s, 0.6, 0.3, 5, 0.6, "Sumário", size=26, color=RED, bold=True, font=TITLE_FONT)
picture(s, ASSETS / "logo_cin.png", 8.62, 0.22, w=1.05)
items = [
    ("Bloco I — O teste de McNemar", "Problemática, definição, origem, pressupostos, formalização e variantes."),
    ("Ilustrações", "#1 McNemar clássico (monitoria) e #2 McNemar exato (campanha)."),
    ("Bloco II — O estudo Safe Fall", "122 crianças, cinco respostas motoras, Tabela 1 e limitações."),
    ("Bloco III — Python", "Notebook reprodutível e demonstração interativa no Colab."),
    ("Síntese e referências", "O que levar desta apresentação."),
]
for i, (h, d) in enumerate(items):
    col, row = (0, i) if i < 3 else (1, i - 3)
    x, y = 0.6 + col * 4.6, 1.3 + row * 1.25
    text(s, x, y, 0.75, 0.6, f"{i + 1:02d}", size=26, color=RED, bold=True, font=TITLE_FONT)
    text(s, x + 0.85, y + 0.02, 3.5, 0.3, h, size=13.5, color=NAVY, bold=True)
    text(s, x + 0.85, y + 0.34, 3.5, 0.6, d, size=10.5, color=GRAY)
text(s, 9.3, 5.25, 0.45, 0.25, str(n), size=10, color=MID_GRAY, align=PP_ALIGN.RIGHT)

# =============================================================== 3. Bloco I
section_slide("Bloco I", "O teste de McNemar",
              ["Problemática, definição e pressupostos", "Formalização e variantes", "Ilustrações resolvidas"])

# =============================================================== 4. Problemática
s, n = new_slide()
content_chrome(s, "0. Problemática", "A campanha mudou a intenção de compra?", n)
flow = [("Antes", "compraria?"), ("Campanha", "publicitária"), ("Depois", "compraria?")]
for i, (h, d) in enumerate(flow):
    chevron(s, 0.5 + i * 1.62, 1.35, 1.75, 0.62, h, fill=[GRAY, RED, TEAL][i], size=11, first=(i == 0))
    text(s, 0.5 + i * 1.62, 2.0, 1.75, 0.3, d, size=10, color=GRAY, italic=True, align=PP_ALIGN.CENTER)
bullets(s, 0.5, 2.5, 4.9, 1.7, [
    "Uma empresa quer avaliar se uma campanha publicitária mudou a intenção de compra dos consumidores.",
    "Pergunta às mesmas pessoas, antes e depois da campanha, se comprariam determinado produto.",
    "Depois da coleta, a proporção de pessoas com intenção de compra aumentou.",
], size=12, spacing=7)
callout(s, 0.5, 4.3, 4.9, 0.8, "A pergunta:",
        "esse aumento é estatisticamente significativo ou pode ser só variação aleatória?", size=12)
card(s, 5.75, 1.3, 3.75, 3.8, accent=RED)
text(s, 6.0, 1.4, 3.4, 0.3, "Mesmas pessoas, duas medidas", size=12, color=RED, bold=True)
rows = [["Consumidor", "Antes", "Depois"],
        ["1", "compraria", "compraria"], ["2", "não", "compraria"], ["3", "compraria", "não"],
        ["4", "não", "não"], ["…", "…", "…"]]
table(s, 6.0, 1.8, 3.3, 2.1, rows, col_widths=[1.1, 1.1, 1.1], size=10.5,
      highlight={(2, 2): TEAL, (3, 2): RED})
text(s, 6.0, 4.05, 3.35, 1.0, [[("É para investigar situações como essa que usamos o ", {}),
                                ("teste de McNemar.", {"bold": True, "color": RED})]], size=11.5)
notes(s, "Problemática do roteiro. A Ilustração #2, adiante, resolve exatamente este caso com números.")

# =============================================================== 5. O teste de McNemar?
s, n = new_slide()
content_chrome(s, "1. Definição", "O que é o teste de McNemar?", n)
card(s, 0.5, 1.25, 5.0, 2.55, accent=RED)
text(s, 0.75, 1.32, 4.65, 2.45, [
    [("Teste não paramétrico ", {"bold": True, "color": RED}),
     "para dados categóricos nominais ", ("pareados", {"bold": True}), "."],
    "Há duas medições relacionadas, e cada uma tem duas categorias mutuamente exclusivas "
    "(sim/não, positivo/negativo, sucesso/fracasso).",
    [("Testa ", {}), ("se as duas medições têm a mesma proporção marginal", {"bold": True, "color": NAVY}),
     ", isto é, se houve mudança estatisticamente significativa entre a primeira e a segunda medida após "
     "uma intervenção."],
], size=12, spacing=7)
text(s, 5.85, 1.25, 3.6, 0.35, "Exemplos", size=13, color=TEAL, bold=True)
exs = [("Diagnóstico", "Dois testes diagnósticos aplicados às mesmas pessoas."),
       ("Opinião", "Antes e depois de uma campanha de conscientização."),
       ("Sintoma", "Presença/ausência antes e depois de um tratamento.")]
for i, (h, d) in enumerate(exs):
    y = 1.7 + i * 1.05
    badge(s, 5.85, y + 0.08, 0.45, str(i + 1), fill=[RED, TEAL, ORANGE][i], size=13)
    text(s, 6.45, y, 3.05, 0.3, h, size=12, color=NAVY, bold=True)
    text(s, 6.45, y + 0.3, 3.05, 0.65, d, size=10.5, color=TEXT)
rect(s, 0.5, 4.0, 5.0, 1.1, fill=NAVY, radius=0.06)
text(s, 0.7, 4.0, 4.6, 1.1, [[("Pareado ", {"bold": True, "color": SAND}),
                             ("= as duas medidas vêm do mesmo indivíduo (ou de pares emparelhados), "
                              "por isso não são independentes.", {"color": WHITE})]],
     size=11.5, anchor=MSO_ANCHOR.MIDDLE)

# =============================================================== 6. Origem e pressupostos
s, n = new_slide()
content_chrome(s, "2–3. Origem e pressupostos", "Quem criou o teste e o que ele exige", n)
card(s, 0.5, 1.25, 4.3, 3.85, accent=NAVY)
text(s, 0.75, 1.32, 4.0, 0.35, "Quinn McNemar, 1947", size=14, color=NAVY, bold=True, font=TITLE_FONT)
text(s, 0.75, 1.72, 4.0, 3.3, [
    "Psicólogo e estatístico.",
    [("Artigo: ", {"bold": True}),
     ("“Note on the sampling error of the difference between correlated proportions or percentages”", {"italic": True}),
     " (Psychometrika)."],
    [("Objetivo original: ", {"bold": True, "color": RED}),
     "fórmulas para avaliar a significância da diferença entre proporções correlacionadas, isto é, "
     "obtidas dos mesmos indivíduos ou de pares relacionados."],
], size=11.5, spacing=8)
text(s, 5.1, 1.25, 4.4, 0.35, "Pressupostos", size=14, color=RED, bold=True, font=TITLE_FONT)
pres = [("✓", TEAL, "Amostra aleatória ou representativa."),
        ("✓", TEAL, "Dados dependentes (pareados), categóricos, binários e dicotômicos: só duas categorias, "
                    "mutuamente exclusivas."),
        ("✗", GRAY, "Não exige normalidade dos dados nem homogeneidade das variâncias.")]
for i, (mk, col, d) in enumerate(pres):
    y = 1.75 + i * 1.1
    badge(s, 5.1, y + 0.05, 0.42, mk, fill=col, size=13)
    text(s, 5.7, y, 3.8, 1.0, d, size=12, color=TEXT)

# =============================================================== 7. Ideia central + organização
s, n = new_slide()
content_chrome(s, "4. Formalização", "Ideia central e organização dos dados", n)
text(s, 0.5, 1.2, 9.0, 0.6, [[("Ideia central: ", {"bold": True, "color": RED}),
     "verificar se a proporção marginal de respostas positivas mudou de forma significativa entre duas medidas "
     "nos mesmos indivíduos (ou em pares emparelhados), para uma variável dicotômica."]], size=11.5)
table(s, 0.5, 1.95, 4.9, 1.7, [
    ["", "Medida 2: +", "Medida 2: −", "Total"],
    ["Medida 1: +", "a", "b", "a + b"],
    ["Medida 1: −", "c", "d", "c + d"],
    ["Total", "a + c", "b + d", "N"],
], col_widths=[1.3, 1.2, 1.2, 1.2], size=12, highlight={(1, 2): RED, (2, 1): TEAL})
text(s, 0.5, 3.75, 4.9, 0.6, "Cada par cai em exatamente uma de quatro combinações: (+,+), (+,−), (−,+) ou (−,−); "
     "a + b + c + d = N.", size=10.5, color=GRAY, italic=True)
card(s, 5.7, 1.95, 3.8, 1.25, accent=GRAY)
text(s, 5.95, 2.0, 3.5, 1.2, [[("Concordantes: a e d", {"bold": True, "color": NAVY})],
                              "as duas medidas coincidem."], size=11.5, spacing=4)
card(s, 5.7, 3.35, 3.8, 1.25, accent=RED)
text(s, 5.95, 3.4, 3.5, 1.2, [[("Discordantes: ", {"bold": True, "color": RED}),
                              ("b", {"bold": True, "color": RED}), (" e ", {"bold": True, "color": RED}),
                              ("c", {"bold": True, "color": TEAL})],
                              "as duas medidas diferem."], size=11.5, spacing=4)
callout(s, 0.5, 4.45, 9.0, 0.65, "Variável:",
        "dicotômica (positivo/negativo) observada em N pares: mesmo indivíduo antes/depois, ou caso e controle.",
        size=11)

# =============================================================== 8. Hipóteses
s, n = new_slide()
content_chrome(s, "4.3 Hipóteses", "Formulação das hipóteses", n)
table(s, 0.5, 1.25, 4.1, 1.45, [
    ["", "Medida 2: +", "Medida 2: −", "Total"],
    ["Medida 1: +", "π₁₁", "π₁₀", "π₁₊"],
    ["Medida 1: −", "π₀₁", "π₀₀", "π₀₊"],
    ["Total", "π₊₁", "π₊₀", "1"],
], col_widths=[1.1, 1.0, 1.0, 1.0], size=11.5, highlight={(1, 2): RED, (2, 1): TEAL})
text(s, 0.5, 2.75, 4.1, 0.5, "1 = positivo, 0 = negativo; o 1º índice é a medida 1, o 2º a medida 2.",
     size=9.5, color=GRAY, italic=True)
text(s, 0.5, 3.15, 4.1, 0.3, "Estimadores", size=11.5, color=TEAL, bold=True)
picture(s, FIGS / "f_estimadores.png", 0.5, 3.45, w=4.1, h=0.55)
picture(s, FIGS / "f_marginais.png", 0.5, 4.1, w=4.1, h=0.35)
picture(s, FIGS / "f_marginais_amostra.png", 0.5, 4.55, w=3.3, h=0.55)
card(s, 4.9, 1.25, 4.6, 1.15, accent=NAVY)
text(s, 5.15, 1.3, 4.3, 0.3, "Proporções marginais", size=11.5, color=NAVY, bold=True)
picture(s, FIGS / "f_h_marginais.png", 5.15, 1.7, w=4.2, h=0.45)
text(s, 4.9, 2.55, 4.6, 0.3, "Reescrevendo e cancelando o termo comum π₁₁:", size=11, color=GRAY)
picture(s, FIGS / "f_h_cancela.png", 5.15, 2.9, w=3.0, h=0.32)
rect(s, 4.9, 3.35, 4.6, 0.75, fill=NAVY, radius=0.06)
picture(s, FIGS / "f_h_discordantes_branco.png", 5.05, 3.45, w=4.3, h=0.55)
text(s, 4.9, 4.2, 4.6, 0.95, [[("O teste usa só b e c ", {"bold": True, "color": RED}),
     "(π₁₀ e π₀₁ são estimados por b/N e c/N). Sob H₀ esperamos b ≈ c; a e d não contribuem para a diferença "
     "entre as marginais."]], size=10.5)

# =============================================================== 9. Estatística do teste
s, n = new_slide()
content_chrome(s, "4.4 Estatística do teste", "Dos pares discordantes à estatística χ²", n)
text(s, 0.5, 1.2, 4.4, 0.85, [
    "Condicionamos no total de discordantes n = b + c.",
    "B conta quantos dos n discordantes são do tipo (+, −); a chance de um discordante ser desse tipo é:",
], size=11, spacing=3)
picture(s, FIGS / "f_p_direcao.png", 0.5, 2.1, w=4.3, h=0.55)
text(s, 0.5, 2.75, 4.4, 0.3, "Sob H₀, condicionando em n:", size=11, color=GRAY)
picture(s, FIGS / "f_b_binomial.png", 0.5, 3.05, w=4.3, h=0.55)
callout(s, 0.5, 3.85, 4.4, 1.25, "n suficientemente grande",
        "(regra usual: n ≥ 25): a binomial é bem aproximada pela normal.", size=11)
text(s, 5.15, 1.2, 4.35, 0.3, "Padronizando B no valor observado b:", size=11, color=GRAY)
picture(s, FIGS / "f_z.png", 5.15, 1.55, w=4.35, h=1.05)
text(s, 5.15, 2.75, 4.35, 0.6, "O quadrado de uma normal padrão tem distribuição qui-quadrado com 1 grau de liberdade:",
     size=11, color=TEXT)
rect(s, 5.15, 3.45, 4.35, 1.1, fill=NAVY, radius=0.06)
picture(s, FIGS / "f_chi2_branco.png", 5.3, 3.55, w=2.6, h=0.9)
text(s, 7.9, 3.45, 1.5, 1.1, "1 gl", size=16, color=SAND, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=TITLE_FONT)
text(s, 5.15, 4.65, 4.35, 0.45, "Estatística do teste de McNemar (versão clássica).", size=10.5, color=RED, bold=True)

# =============================================================== 10. Variantes
s, n = new_slide()
content_chrome(s, "Variantes", "Quatro versões do teste", n)
text(s, 0.5, 1.15, 9.0, 0.4, "A aproximação qui-quadrado depende de haver pares discordantes suficientes; "
     "as variantes cobrem os demais cenários.", size=11, color=GRAY)
heads = ["Versão", "Estatística", "Quando usar"]
xs, ws = [0.5, 2.6, 5.75], [2.0, 3.05, 3.75]
for x, w_, h in zip(xs, ws, heads):
    rect(s, x, 1.6, w_, 0.36, fill=NAVY)
    text(s, x + 0.1, 1.6, w_ - 0.2, 0.36, h, size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
variants = [
    ("Clássica (assintótica)", "f_v_classica.png", "b + c ≥ 25 · χ² com 1 gl", TEAL),
    ("Com correção de continuidade (Edwards, 1948)", "f_v_edwards.png",
     "b + c ≥ 25, para corrigir a binomial discreta × χ² contínua. Mais conservadora; é a do R (mcnemar.test).", NAVY),
    ("Exata (binomial)", "f_v_exata.png",
     "b + c < 25. X ~ Bin(n; 0,5), k = min(b, c), n = b + c. Sem aproximação, mas conservadora.", RED),
    ("Mid-p exata", "f_v_midp.png",
     "b + c < 25, quando se quer um teste menos conservador e com mais poder que o exato.", ORANGE),
]
for i, (name, fig, when, col) in enumerate(variants):
    y = 1.98 + i * 0.68
    rect(s, 0.5, y, 9.0, 0.66, fill=LIGHT if i % 2 == 0 else WHITE)
    rect(s, 0.5, y, 0.07, 0.66, fill=col)
    text(s, 0.65, y, 1.9, 0.66, name, size=10.5, color=col, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    fh = 0.54 if "exata" not in fig and "midp" not in fig else 0.27
    picture(s, FIGS / fig, 2.7, y + (0.66 - fh) / 2, w=2.85, h=fh)
    text(s, 5.85, y, 3.6, 0.66, when, size=9.5, color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.5, 4.72, 9.0, 0.5, "Na prática:",
        "com muitos discordantes, as quatro dão resultados muito próximos; com poucos, prefira a exata ou a mid-p. "
        "Informe sempre a versão usada.", size=10.5)
notes(s, "A fórmula exata p = 2·P(X ≤ k) é limitada a 1 quando b = c (o código usa min(1, ·)).")

# =============================================================== 11. A variante exata
s, n = new_slide()
content_chrome(s, "4.1 A variante exata", "Por que a distribuição binomial?", n)
card(s, 0.5, 1.25, 4.3, 1.45, accent=NAVY)
text(s, 0.75, 1.3, 4.0, 1.4, [
    [("Alternativa ao assintótico ", {"bold": True, "color": NAVY}), "quando há poucos discordantes (regra geral: n < 25)."],
    [("Clássico: ", {"bold": True}), "aproximação pela qui-quadrado."],
    [("Exato: ", {"bold": True, "color": RED}), "usa diretamente a distribuição binomial."],
], size=11, spacing=4)
text(s, 0.5, 2.85, 4.3, 0.3, "O teste só olha para quem mudou de resposta:", size=11, color=GRAY)
chevron(s, 0.5, 3.2, 2.1, 0.55, "+ → −   (b)", fill=RED, size=12, first=True)
chevron(s, 2.6, 3.2, 2.1, 0.55, "− → +   (c)", fill=TEAL, size=12, first=True)
text(s, 0.5, 3.9, 4.3, 1.2, [
    [("Logo: ", {"bold": True}), "X ~ Bin(n; 0,5), com n = b + c."],
    "O número de tentativas é o total de pares discordantes.",
], size=11.5, spacing=4)
text(s, 5.1, 1.25, 4.4, 0.3, "A lógica de um experimento binomial", size=12, color=TEAL, bold=True)
bullets(s, 5.1, 1.6, 4.4, 2.1, [
    "Existem duas possibilidades (positivo e negativo).",
    "Cada observação tem uma probabilidade de ocorrência.",
    "Sob H₀, essa probabilidade é 0,5 para cada direção.",
    "Os pares são considerados independentes entre si.",
], size=11, spacing=5)
callout(s, 5.1, 3.8, 4.4, 1.3, "Atenção:",
        "o 0,5 não significa que metade da população é positiva. Significa que, entre os discordantes, "
        "as duas direções de mudança são igualmente prováveis sob H₀.", size=10.5)

# =============================================================== 12. Fórmula binomial
s, n = new_slide()
content_chrome(s, "4.1 A variante exata", "A fórmula binomial no McNemar exato", n)
text(s, 0.5, 1.2, 4.4, 0.3, "Função de probabilidade binomial", size=11.5, color=TEAL, bold=True)
picture(s, FIGS / "f_pmf.png", 0.5, 1.55, w=4.0, h=0.6)
table(s, 0.5, 2.35, 4.4, 1.9, [
    ["Símbolo", "Significado no McNemar"],
    ["n", "Total de pares discordantes: b + c"],
    ["k", "Discordantes em uma direção: k = min(b, c)"],
    ["p", "Prob. de mudança nessa direção (0,5 sob H₀)"],
    ["q", "Prob. da direção contrária (0,5 sob H₀)"],
], col_widths=[0.8, 3.6], size=10.5)
text(s, 5.2, 1.2, 4.3, 0.3, "Sob H₀ (p = q = 0,5):", size=11.5, color=TEAL, bold=True)
picture(s, FIGS / "f_pmf05.png", 5.2, 1.55, w=4.3, h=0.6)
rect(s, 5.2, 2.4, 4.3, 1.15, fill=NAVY, radius=0.06)
text(s, 5.35, 2.43, 4.0, 0.3, "P-valor exato bilateral", size=11, color=SAND, bold=True)
picture(s, FIGS / "f_pvalor_branco.png", 5.35, 2.75, w=4.0, h=0.72)
callout(s, 5.2, 3.75, 4.3, 0.9, "Origem:", "esta é a origem matemática do teste exato de McNemar.", size=11)
notes(s, "Somamos a cauda até k = min(b, c) e dobramos, porque a binomial com p = 0,5 é simétrica.")

# =============================================================== 13. Limites
s, n = new_slide()
content_chrome(s, "Limites", "Quando não usar o McNemar", n)
text(s, 0.5, 1.25, 9.0, 0.5, "Se o estudo tiver amostras independentes, mais de duas medições ou mais de duas "
     "categorias, use outro teste:", size=12, color=TEXT)
lims = [("Grupos independentes", "Qui-quadrado ou teste de Fisher", NAVY),
        ("Mais de duas medições", "Q de Cochran", TEAL),
        ("Mais de duas categorias", "Teste de Bowker", ORANGE)]
for i, (sit, test, col) in enumerate(lims):
    x = 0.5 + i * 3.05
    card(s, x, 2.0, 2.85, 2.2, accent=col)
    text(s, x + 0.25, 2.1, 2.5, 0.3, "Situação", size=10, color=GRAY)
    text(s, x + 0.25, 2.38, 2.5, 0.65, sit, size=14, color=NAVY, bold=True)
    arrow(s, x + 0.25, 3.12, 0.35, 0.2, fill=col)
    text(s, x + 0.7, 3.0, 2.0, 0.3, "Sugestão", size=10, color=GRAY)
    text(s, x + 0.25, 3.4, 2.5, 0.7, test, size=13.5, color=col, bold=True)
rect(s, 0.5, 4.45, 9.0, 0.65, fill=RED, radius=0.1)
text(s, 0.5, 4.45, 9.0, 0.65, "McNemar: mesmos indivíduos · duas medições · duas categorias",
     size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# =============================================================== 14–15. Ilustração #1
s, n = new_slide()
content_chrome(s, "Ilustração #1 — McNemar clássico", "Uma monitoria melhorou o desempenho?", n)
text(s, 0.5, 1.2, 4.5, 0.9, "Um professor aplicou uma avaliação antes e outra depois de uma monitoria de Estatística "
     "aos mesmos 100 alunos. α = 5 %.", size=11.5)
table(s, 0.5, 2.15, 4.5, 1.35, [
    ["", "Depois: aprovado", "Depois: reprovado"],
    ["Antes: aprovado", "45", "10"],
    ["Antes: reprovado", "30", "15"],
], col_widths=[1.5, 1.5, 1.5], size=12, highlight={(1, 2): RED, (2, 1): TEAL})
text(s, 0.5, 3.6, 4.5, 0.3, "SINTÉTICO — exemplo didático do roteiro", size=9, color=MID_GRAY, italic=True)
text(s, 5.3, 1.2, 4.2, 0.3, "Etapa 1 — Identificando os valores", size=12, color=RED, bold=True)
bullets(s, 5.3, 1.55, 4.2, 2.0, [
    [("a = 45 ", {"bold": True}), "aprovados nas duas avaliações"],
    [("b = 10 ", {"bold": True, "color": RED}), "aprovados antes, reprovados depois"],
    [("c = 30 ", {"bold": True, "color": TEAL}), "reprovados antes, aprovados depois"],
    [("d = 15 ", {"bold": True}), "reprovados nas duas avaliações"],
    [("n = b + c = 40 ", {"bold": True, "color": NAVY}), "alunos que mudaram de resultado"],
], size=11, spacing=4)
card(s, 0.5, 3.95, 9.0, 1.15, accent=NAVY)
text(s, 0.75, 4.0, 8.6, 0.3, "Etapa 2 — Formulando as hipóteses", size=12, color=NAVY, bold=True)
text(s, 0.75, 4.32, 8.6, 0.75, [
    [("H₀: π₁₊ = π₊₁ ", {"bold": True}), "— não há diferença nas proporções marginais de aprovados após a monitoria"],
    [("H₁: π₁₊ ≠ π₊₁ ", {"bold": True}), "— há diferença nas proporções marginais de aprovados após a monitoria"],
], size=11, spacing=2)

s, n = new_slide()
content_chrome(s, "Ilustração #1 — McNemar clássico", "Etapa 3: aplicando o McNemar clássico", n)
steps = [("3.1", "Estatística do teste", "f_ex1_chi2.png"),
         ("3.2", "Valor crítico (α = 0,05; gl = 1)", "f_ex1_crit.png")]
for i, (k, h, fig) in enumerate(steps):
    y = 1.25 + i * 1.0
    badge(s, 0.5, y + 0.05, 0.45, k, fill=RED, size=10)
    text(s, 1.1, y, 3.6, 0.3, h, size=11, color=GRAY, bold=True)
    picture(s, FIGS / fig, 1.1, y + 0.32, w=3.5, h=0.6 if "chi2" in fig else 0.45)
badge(s, 0.5, 3.3, 0.45, "3.3", fill=RED, size=10)
text(s, 1.1, 3.25, 3.7, 0.3, "P-valor (recurso computacional)", size=11, color=GRAY, bold=True)
text(s, 1.1, 3.55, 3.7, 0.35, "p-valor = 0,001565", size=15, color=NAVY, bold=True, font=TITLE_FONT)
text(s, 1.1, 3.9, 3.7, 0.4, "A tabela qui-quadrado dá valores críticos, não o p-valor exato.", size=9.5,
     color=GRAY, italic=True)
picture(s, FIGS / "chi2_monitoria.png", 4.95, 1.2, w=4.55, h=2.6)
rect(s, 0.5, 4.35, 9.0, 0.78, fill=NAVY, radius=0.06)
text(s, 0.7, 4.35, 8.6, 0.78, [[("3.4 Conclusão: ", {"bold": True, "color": SAND}),
     ("3,841 < 10 e 0,001565 < 0,05 ⇒ rejeita-se H₀. Aprovados passaram de 55 % para 75 %: "
      "a monitoria foi associada a um aumento na aprovação.", {"color": WHITE})]],
     size=11.5, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Proporções: antes (a+b)/N = 55/100; depois (a+c)/N = 75/100. "
         "O roteiro escreve 'houveram mudanças'; na fala, use 'houve mudança'.")

# =============================================================== 16–17. Ilustração #2
s, n = new_slide()
content_chrome(s, "Ilustração #2 — McNemar exato", "A campanha mudou a intenção de compra?", n)
text(s, 0.5, 1.2, 4.5, 0.9, "Uma empresa entrevistou 100 consumidores antes e depois de uma campanha publicitária. "
     "α = 5 %.", size=11.5)
table(s, 0.5, 2.15, 4.5, 1.35, [
    ["", "Depois: compraria", "Depois: não compraria"],
    ["Antes: compraria", "42", "3"],
    ["Antes: não compraria", "12", "43"],
], col_widths=[1.5, 1.5, 1.5], size=11.5, highlight={(1, 2): RED, (2, 1): TEAL})
text(s, 0.5, 3.6, 4.5, 0.3, "SINTÉTICO — exemplo didático do roteiro", size=9, color=MID_GRAY, italic=True)
text(s, 5.3, 1.2, 4.2, 0.3, "Etapa 1 — Identificando os valores", size=12, color=RED, bold=True)
bullets(s, 5.3, 1.55, 4.2, 2.0, [
    [("a = 42 ", {"bold": True}), "comprariam independente da campanha"],
    [("b = 3 ", {"bold": True, "color": RED}), "comprariam, passaram a não comprar"],
    [("c = 12 ", {"bold": True, "color": TEAL}), "não comprariam, passaram a comprar"],
    [("d = 43 ", {"bold": True}), "não comprariam independente da campanha"],
    [("n = b + c = 15 ", {"bold": True, "color": NAVY}), "mudaram de opinião (n < 25 ⇒ exato)"],
], size=11, spacing=4)
card(s, 0.5, 3.95, 9.0, 1.15, accent=NAVY)
text(s, 0.75, 4.0, 8.6, 0.3, "Etapa 2 — Formulando as hipóteses", size=12, color=NAVY, bold=True)
text(s, 0.75, 4.32, 8.6, 0.75, [
    [("H₀: π₁₊ = π₊₁ ", {"bold": True}), "— não há diferença nas proporções de quem compraria antes e depois da publicidade"],
    [("H₁: π₁₊ ≠ π₊₁ ", {"bold": True}), "— há diferença nas proporções de quem compraria antes e depois da publicidade"],
], size=11, spacing=2)

s, n = new_slide()
content_chrome(s, "Ilustração #2 — McNemar exato", "Etapa 3: calculando o p-valor exato", n)
picture(s, FIGS / "f_ex2_p.png", 0.5, 1.2, w=4.4, h=0.75)
text(s, 0.5, 1.95, 4.4, 0.3, "onde n = 15 e k = 3:", size=10.5, color=GRAY)
probs = [["i", "P(X = i) = C(15, i) · 0,5ⁱ · 0,5¹⁵⁻ⁱ"],
         ["0", "3,052 · 10⁻⁵"], ["1", "4,578 · 10⁻⁴"], ["2", "3,204 · 10⁻³"], ["3", "1,389 · 10⁻²"],
         ["P(X ≤ 3)", "0,0175"], ["2 · P(X ≤ 3)", "0,03516"]]
table(s, 0.5, 2.3, 4.4, 2.0, probs, col_widths=[1.2, 3.2], size=10.5, highlight={(6, 1): RED})
picture(s, FIGS / "binomial_b3_c12.png", 5.1, 1.2, w=4.4, h=3.05)
rect(s, 0.5, 4.4, 9.0, 0.75, fill=NAVY, radius=0.06)
text(s, 0.7, 4.4, 8.6, 0.75, [[("Conclusão: ", {"bold": True, "color": SAND}),
     ("0,03516 < 0,05 ⇒ rejeita-se H₀. A intenção de compra passou de 45 % para 54 %: "
      "a campanha foi associada a um aumento na intenção de compra.", {"color": WHITE})]],
     size=11.5, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "P(X ≤ 3) = 576/32768 = 0,017578 (o roteiro trunca para 0,0175); 2 × 0,017578 = 0,03516. "
         "Antes: (42+3)/100 = 45 %; depois: (42+12)/100 = 54 %. "
         "As áreas vermelhas do gráfico são as duas caudas somadas no p-valor.")

# =============================================================== 18. Bloco II
section_slide("Bloco II", "O estudo Safe Fall",
              ["Contexto e desenho quase experimental", "As cinco respostas motoras", "McNemar aplicado à Tabela 1"])

# =============================================================== 19. Artigo / contexto
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

# =============================================================== 20. Desenho / linha do tempo
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

# =============================================================== 21. Cinco respostas
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

# =============================================================== 22. Por que McNemar
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

# =============================================================== 23. Resultados publicados
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

# =============================================================== 24. Auditoria Tabela 1
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

# =============================================================== 25. Do X² às tabelas 2x2
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

# =============================================================== 26. Limitações
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

# =============================================================== 27. Bloco III
section_slide("Bloco III", "Demonstração em Python",
              ["Notebook reprodutível", "As ilustrações no Python", "Demonstração interativa no Colab"])

# =============================================================== 28. Notebook
s, n = new_slide()
content_chrome(s, "Implementação", "Notebook 01_mcnemar_safe_fall.ipynb", n)
etapas = ["Dados", "Exploração", "Fundamentos", "Ilustração #1", "Ilustração #2", "Versões",
          "Safe Fall", "Demonstração", "Exemplos", "Conclusões"]
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
    "tab = [[42, 3], [12, 43]]         # Ilustração #2",
    "res = mcnemar(tab, exact=True)    # p = 0,03516",
    "binomtest(3, 3 + 12, 0.5).pvalue  # p = 0,03516 ✓",
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
        ("visualizations", "figuras dos slides"), ("plotly_charts", "gráficos interativos"), ("interactive_demo", "widget b × c"),
        ("slide_examples", "exemplos dos slides ajustáveis")]
for i, (m, d) in enumerate(mods):
    y = 1.64 + i * 0.29
    text(s, 5.8, y, 1.75, 0.32, m + ".py", size=9, color=NAVY, bold=True, font=MONO_FONT)
    text(s, 7.6, y, 1.85, 0.32, d, size=9.5, color=GRAY)
text(s, 5.8, 4.62, 3.6, 0.4, [[("45 testes automatizados", {"bold": True, "color": TEAL}), " (pytest)"]], size=10.5)

# =============================================================== 29. Demo interativa
s, n = new_slide()
content_chrome(s, "Demonstração", "Demonstração interativa: mova b e c", n)
for i, (lab, val, col) in enumerate([("c — (−, +)", 12, TEAL), ("b — (+, −)", 3, RED)]):
    y = 1.3 + i * 0.42
    text(s, 0.5, y, 1.9, 0.3, lab, size=10, color=NAVY, bold=True)
    rect(s, 2.45, y + 0.12, 2.6, 0.06, fill=BORDER)
    rect(s, 2.45, y + 0.12, 2.6 * val / 40, 0.06, fill=col)
    badge(s, 2.45 + 2.6 * val / 40 - 0.09, y + 0.06, 0.18, "", fill=col)
    text(s, 5.15, y, 0.4, 0.3, str(val), size=10.5, color=col, bold=True)
picture(s, FIGS / "demo_b3_c12.png", 0.45, 2.15, w=6.2, h=2.3)
text(s, 0.5, 4.5, 6.1, 0.6, "Saída do widget (ipywidgets) na Ilustração #2 (b = 3, c = 12): tabela, nº de pares discordantes, estatística, "
     "p exato, binomial sob H₀ e interpretação — tudo se atualiza ao mover os controles.", size=10, color=GRAY, italic=True)
card(s, 6.85, 1.25, 2.65, 3.85, accent=TEAL)
text(s, 7.07, 1.3, 2.4, 0.3, "Experimente no Colab", size=11.5, color=TEAL, bold=True)
picture(s, FIGS / "qr_colab.png", 7.47, 1.62, w=1.45)
text(s, 7.07, 3.1, 2.4, 0.4, [[("github.com/RodrigoSantosB/", {"size": 8.5}), ("mcnemar-safe-fall", {"size": 8.5, "bold": True})]],
     size=8.5, color=NAVY, align=PP_ALIGN.CENTER, font=MONO_FONT)
text(s, 7.07, 3.5, 2.4, 1.6, [
    [("b = c: ", {"bold": True}), "p = 1 — sem evidência."],
    [("b = 3, c = 12: ", {"bold": True}), "p = 0,035."],
    [("Mude a e d: ", {"bold": True, "color": RED}), "o p-valor não muda."],
], size=10, spacing=4)
source_note(s, "Dados SINTÉTICOS. Notebook: seção 9 (este widget) e seção 10 (abas com as ilustrações, as variantes e o Safe Fall, ajustáveis).")

# =============================================================== 30. Conclusões
s, n = new_slide()
content_chrome(s, "Conclusões", "Síntese", n)
concl = [
    ("Pareado, dicotômico, só b e c", "McNemar testa H₀: π₁₊ = π₊₁ ⇔ π₁₀ = π₀₁ — a mudança marginal depende só dos pares discordantes.", TEAL),
    ("Escolha e informe a versão", "b + c ≥ 25: χ² clássico ou com correção de Edwards. b + c < 25: exato (Bin(n; 0,5)) ou mid-p.", RED),
    ("Safe Fall: mudança robusta", "84–106 melhoras contra 0–2 pioras; p < 0,001 em qualquer método. Conclusão do artigo se sustenta.", NAVY),
    ("Leitura crítica", "Quase experimento sem controle; desfecho é comportamento, não lesão; Tabela 1 com % inconsistentes.", ORANGE),
]
for i, (h, d, col) in enumerate(concl):
    y = 1.25 + i * 0.97
    card(s, 0.5, y, 9.0, 0.85, accent=col)
    badge(s, 0.75, y + 0.2, 0.45, str(i + 1), fill=col, size=13)
    text(s, 1.4, y + 0.06, 7.9, 0.3, h, size=12.5, color=NAVY, bold=True)
    text(s, 1.4, y + 0.38, 7.9, 0.45, d, size=10.5, color=TEXT)

# =============================================================== 31. Referências
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

# =============================================================== 32. Encerramento (template)
closing = clone_slide(prs, CLOSING_TPL)

# remove os slides de exemplo do template original
for old in template_slides:
    delete_slide(prs, old)

prs.save(OUTPUT)
print(f"{len(prs.slides)} slides -> {OUTPUT}")
