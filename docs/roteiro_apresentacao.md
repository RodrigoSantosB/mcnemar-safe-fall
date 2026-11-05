# Roteiro da apresentação (27 slides, ~25 min)

Arquivo: `slides/apresentacao_mcnemar_safe_fall.pptx` · gerado por `slides/build_slides.py` sobre `templates/template_cin_ufpe.pptx`.

| # | Título | Objetivo | Conteúdo | Recurso visual |
|---|---|---|---|---|
| 1 | O teste exato de McNemar | Abrir | Tema, artigo-base, autor | Capa vermelha CIn-UFPE com logos |
| 2 | Sumário | Orientar | 5 partes | Numeração grande do template |
| 3 | Bloco I — Fundamentação estatística | Transição | 3 tópicos | Divisória clonada do template |
| 4 | O treinamento mudou o comportamento? | Motivar | Exemplo escolar, pergunta de pesquisa | Fluxo observação → intervenção → nova observação; tabela de mudanças individuais |
| 5 | O que é o McNemar — e quando usá-lo | Definir | Pareado, dicotômico, não paramétrico; vs χ² de independência; exato vs assintótico | Fluxograma de decisão |
| 6 | Tabela 2×2 pareada | Estrutura | a, b, c, d; pós − pré = c − b | Matriz com b e c destacadas |
| 7 | Hipóteses e funcionamento | Formalizar | H₀/H₁, homogeneidade marginal, Binomial(b+c; 0,5), p exato, χ² assintótico | Fórmulas renderizadas |
| 8 | Exemplo resolvido b = 2, c = 10 | Calcular à mão | 5 passos até p = 0,0386 | Binomial sob H₀ com caudas |
| 9 | Significativo ou não? | Interpretar | p = 0,039 vs p = 0,424; evidência ≠ efeito | Duas matrizes + binomiais |
| 10 | Exato × qui-quadrado | Comparar métodos | b = 1, c = 7: 0,070 vs 0,034 vs 0,077 | Curva de p-valores + tabela |
| 11 | Bloco II — O estudo Safe Fall | Transição | 3 tópicos | Divisória do template |
| 12 | Ensinar crianças a cair com segurança | Contexto | 122 crianças, 10–12 anos, Sevilha, quase experimento | Cartões numéricos + Figura 1 do artigo |
| 13 | Desenho do estudo | Metodologia | Linha do tempo, INFOSECA, Kappa, cuidados | Timeline + foto do Apêndice A |
| 14 | As cinco respostas motoras | Variáveis | Descrição, objetivo, correto/incorreto, κ | Esquema corporal didático (vista lateral) |
| 15 | Por que McNemar é adequado? | Justificar | 5 condições; por que não χ² de independência (112,2 vs 76,3) | Checklist + tabela "como se fossem grupos" |
| 16 | Mais crianças passaram a cair protegidas | Resultados | +39 a +87 p.p.; p = 0,000 → p < 0,001 | Gráfico haltere pré/pós |
| 17 | Tabela 1 conferida | Rigor | Publicado × recalculado, divergências | Tabela com células sinalizadas |
| 18 | O X² publicado revela b e c | Aplicação do teste | Inversão do χ² corrigido; tabelas inferidas; p exatos | Fórmula + tabela + fluxo do pescoço |
| 19 | Limitações | Leitura crítica | Sem controle, conveniência, familiaridade, comportamento ≠ lesão, reprodutibilidade | 6 cartões |
| 20 | Bloco III — Demonstração em Python | Transição | 3 tópicos | Divisória do template |
| 21 | Notebook | Mostrar o código | 11 etapas, módulos, validação tripla, 40 testes | Pipeline + bloco de código |
| 22 | Demonstração interativa | Ao vivo | Controles b e c; casos para testar | Mock dos sliders + saída real do widget + QR code do Colab |
| 23 | Como b e c movem o p-valor | Intuição | |c − b| e b + c governam; a e d ignorados | p-valor exato vs c (n = 20) |
| 24 | Mesma estrutura em educação | Transferir | 40 alunos, b = 3, c = 13, p = 0,021 | Matriz + fluxo + tabela comparativa |
| 25 | Síntese | Fechar | 4 mensagens | Cartões numerados |
| 26 | Referências | Fontes | Artigo, McNemar 1947, Edwards 1948, Agresti, Fagerland, statsmodels/SciPy | Lista |
| 27 | Muito obrigado! | Encerrar | Contatos CIn | Slide de encerramento do template |

**Momento ao vivo (slide 22):** abrir `notebooks/01_mcnemar_safe_fall.ipynb`, Etapa 9a, e mover os controles:
b = c → p = 1; (7, 9) → p = 0,80; (3, 13) → p = 0,021; alterar a e d para mostrar que o p-valor não muda.
Se o widget falhar, rodar a célula seguinte (`render(b, c)`). A Etapa 12 tem abas para ajustar ao vivo os exemplos dos slides 8, 9, 10, 18, 22, 23 e 24.

Rótulos de dados usados nos slides: **publicado** (Tabela 1), **INFERIDO** (tabelas 2×2 do Safe Fall) e **SINTÉTICO** (educação, demonstração).
