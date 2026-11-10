# Roteiro da apresentação (32 slides, ~30 min)

Arquivo: `slides/apresentacao_mcnemar_safe_fall.pptx` · gerado por `slides/build_slides.py` sobre `templates/template_cin_ufpe.pptx`.

O Bloco I (slides 3–17) segue o documento-roteiro "Teste de McNemar": problemática, definição, origem, pressupostos,
formalização, variantes, variante exata, limites e as Ilustrações #1 (monitoria, clássico) e #2 (campanha, exato).
Os slides antigos que repetiam essa teoria (hipóteses, exemplo b = 2/c = 10, significativo × não, p-valor × c e o
exemplo de educação 3/13) foram removidos.

| # | Título | Objetivo | Conteúdo | Recurso visual |
|---|---|---|---|---|
| 1 | O teste exato de McNemar | Abrir | Tema, artigo-base, autor | Capa vermelha CIn-UFPE com logos |
| 2 | Sumário | Orientar | 5 partes | Numeração grande do template |
| 3 | Bloco I — O teste de McNemar | Transição | 3 tópicos | Divisória clonada do template |
| 4 | A campanha mudou a intenção de compra? | Motivar (roteiro §0) | Mesmas pessoas antes/depois; aumento é significativo ou acaso? | Fluxo antes → campanha → depois; tabela de consumidores |
| 5 | O que é o teste de McNemar? | Definir (§1) | Não paramétrico, nominal pareado, 2 categorias; mesma proporção marginal; 3 exemplos | Cartão de definição + exemplos numerados |
| 6 | Quem criou o teste e o que ele exige | Origem e pressupostos (§2–3) | McNemar 1947, Psychometrika; amostra representativa, dados pareados dicotômicos, sem normalidade | Dois cartões com marcadores ✓/✗ |
| 7 | Ideia central e organização dos dados | Formalizar (§4.1–4.2) | Tabela Medida 1 × Medida 2 com margens; concordantes a, d; discordantes b, c | Tabela nativa com b e c destacadas |
| 8 | Formulação das hipóteses | Hipóteses (§4.3) | Tabela de π, estimadores, H₀: π₁₊ = π₊₁ ⇒ π₁₀ = π₀₁ | Fórmulas renderizadas |
| 9 | Dos pares discordantes à estatística χ² | Estatística (§3.4) | B ~ Bin(n; 0,5), μ = n/2, σ² = n/4, z = (b−c)/√(b+c), χ² com 1 gl, n ≥ 25 | Derivação em fórmulas |
| 10 | Quatro versões do teste | Variantes | Clássica, Edwards, exata, mid-p e quando usar cada uma | Tabela com fórmulas |
| 11 | Por que a distribuição binomial? | Variante exata (§4.1) | Clássico × exato; experimento binomial; aviso sobre o 0,5 | Cartões + chevrons + − / − + |
| 12 | A fórmula binomial no McNemar exato | Fórmula | P(X = k), tabela de símbolos, p = 2·Σ P(X = i) | Fórmulas + tabela |
| 13 | Quando não usar o McNemar | Limites | Independentes → χ²/Fisher; > 2 medições → Q de Cochran; > 2 categorias → Bowker | Três cartões |
| 14 | Uma monitoria melhorou o desempenho? | Ilustração #1 (Etapas 1–2) | 45/10/30/15, n = 40, hipóteses | Tabela + lista de valores |
| 15 | Etapa 3: aplicando o McNemar clássico | Ilustração #1 (Etapa 3) | χ² = 10, crítico 3,841, p = 0,001565, 55 % → 75 % | Fórmulas + curva χ²₁ com região crítica |
| 16 | A campanha mudou a intenção de compra? | Ilustração #2 (Etapas 1–2) | 42/3/12/43, n = 15, hipóteses | Tabela + lista de valores |
| 17 | Etapa 3: calculando o p-valor exato | Ilustração #2 (Etapa 3) | P(X = 0…3), P(X ≤ 3) = 0,0175, p = 0,03516, 45 % → 54 % | Tabela de probabilidades + Binomial(15; 0,5) |
| 18 | Bloco II — O estudo Safe Fall | Transição | 3 tópicos | Divisória do template |
| 19 | Ensinar crianças a cair com segurança | Contexto | 122 crianças, 10–12 anos, Sevilha, quase experimento | Cartões numéricos + Figura 1 do artigo |
| 20 | Desenho do estudo | Metodologia | Linha do tempo, INFOSECA, Kappa, cuidados | Timeline + foto do Apêndice A |
| 21 | As cinco respostas motoras | Variáveis | Descrição, objetivo, correto/incorreto, κ | Esquema corporal didático |
| 22 | Por que McNemar é adequado? | Justificar | 5 condições; por que não χ² de independência | Checklist + tabela "como se fossem grupos" |
| 23 | Mais crianças passaram a cair protegidas | Resultados | +39 a +87 p.p.; p = 0,000 → p < 0,001 | Gráfico haltere pré/pós |
| 24 | Tabela 1 conferida | Rigor | Publicado × recalculado, divergências | Tabela com células sinalizadas |
| 25 | O X² publicado revela b e c | Aplicação | Inversão do χ² corrigido (Edwards); tabelas inferidas | Fórmula + tabela + fluxo do pescoço |
| 26 | Limitações | Leitura crítica | Sem controle, conveniência, familiaridade, comportamento ≠ lesão | 6 cartões |
| 27 | Bloco III — Demonstração em Python | Transição | 3 tópicos | Divisória do template |
| 28 | Notebook | Mostrar o código | Etapas, módulos, validação tripla, 44 testes; snippet da Ilustração #2 | Pipeline + bloco de código |
| 29 | Demonstração interativa | Ao vivo | Controles b e c, começando na campanha | Mock dos sliders + saída do widget + QR code do Colab |
| 30 | Síntese | Fechar | 4 mensagens | Cartões numerados |
| 31 | Referências | Fontes | Artigo, McNemar 1947, Edwards 1948, Agresti, Fagerland, statsmodels/SciPy | Lista |
| 32 | Muito obrigado! | Encerrar | Contatos CIn | Slide de encerramento do template |

**Notas do apresentador sobre o roteiro:** P(X ≤ 3) = 576/32768 = 0,017578 (o roteiro trunca para 0,0175);
"houveram mudanças" deve ser dito "houve mudança"; p = 2·P(X ≤ k) é limitado a 1 quando b = c.

**Momento ao vivo (slide 29):** abrir `notebooks/01_mcnemar_safe_fall.ipynb`, Etapa 9a, que começa na Ilustração #2
(b = 3, c = 12 → p = 0,035). Mover para b = c → p = 1; alterar a e d para mostrar que o p-valor não muda.
Se o widget falhar, rodar a célula seguinte (`render(b, c)`). A Etapa 12 tem abas para ajustar ao vivo os slides
10 (variantes), 15 (Ilustração #1), 17 (Ilustração #2), 25 (Safe Fall) e 29 (demonstração).

Rótulos de dados usados nos slides: **publicado** (Tabela 1), **INFERIDO** (tabelas 2×2 do Safe Fall) e **SINTÉTICO**
(ilustrações do roteiro, demonstração).
