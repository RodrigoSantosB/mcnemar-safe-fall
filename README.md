# Teste exato de McNemar — programa Safe Fall

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RodrigoSantosB/mcnemar-safe-fall/blob/main/notebooks/01_mcnemar_safe_fall.ipynb)

Apresentação acadêmica, notebook e pacote Python sobre o **teste exato de McNemar**, aplicado ao estudo
DelCastillo-Andrés *et al.* (2018), *Children's Improvement of a Motor Response during Backward Falls through the
Implementation of a Safe Fall Program*, IJERPH 15:2669, [doi:10.3390/ijerph15122669](https://doi.org/10.3390/ijerph15122669).

## Entregáveis

| Arquivo | Conteúdo |
|---|---|
| `slides/apresentacao_mcnemar_safe_fall.pptx` | Apresentação editável (32 slides) construída sobre o template oficial CIn-UFPE; o Bloco I segue o roteiro "Teste de McNemar" (o slide 29 tem QR code para o Colab) |
| `notebooks/01_mcnemar_safe_fall.ipynb` | Notebook didático em 11 etapas, com demonstração interativa (já executado) |
| `src/safe_fall_statistics/` | Módulos Python usados pelo notebook e pelos slides |
| `data/table1_published.csv` | Tabela 1 do artigo, transcrita sem correções (ver `data/README.md`) |
| `docs/diagnostico_inicial.md` | Auditoria do repositório, resumo do artigo e conferência da Tabela 1 |
| `docs/roteiro_apresentacao.md` | Objetivo, conteúdo e recurso visual de cada slide |
| `results/figures/` | Figuras geradas (PNG) |

## Google Colab

Clique no botão **Abrir no Colab** acima e use *Ambiente de execução → Executar tudo*. A primeira célula de código
clona este repositório em `/content/mcnemar-safe-fall`, adiciona `src/` ao caminho e ativa os widgets do Colab.
Não há nada para instalar: numpy, pandas, scipy, statsmodels, matplotlib, plotly e ipywidgets já vêm no Colab.

### Exemplos dos slides ajustáveis

A **Etapa 12** do notebook abre abas com os exemplos da apresentação, nos mesmos valores iniciais:

| Aba | Slide | Controles |
|---|---|---|
| variantes | 10 | b, c — p-valor das versões clássica, Edwards, exata e mid-p |
| Ilustração #1 | 15 | a, b, c, d da monitoria — χ², valor crítico 3,841, p-valor e conclusão |
| Ilustração #2 | 17 | a, b, c, d da campanha — P(X = i) linha a linha e p exato |
| Safe Fall | 25 | comportamento e b (começa na tabela inferida; outros b mantêm as margens publicadas) |
| demonstração | 29 | a, b, c, d (começa na campanha) |

Fora do notebook:

```python
from safe_fall_statistics.slide_examples import slide_examples_widget
slide_examples_widget()
```

## Como executar localmente

```bash
pip install -e ".[dev]"
```

```bash
python -m pytest
```

```bash
jupyter lab notebooks/01_mcnemar_safe_fall.ipynb
```

Regenerar figuras e slides:

```bash
python slides/make_figures.py && python slides/build_slides.py
```

Reexecutar o notebook de ponta a ponta sem abrir o Jupyter:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_mcnemar_safe_fall.ipynb
```

A demonstração interativa (Etapa 9a) usa **ipywidgets**: rode-a no Jupyter Lab/Notebook ou no VS Code com o kernel ativo.
Uma versão estática (`render(b, c)`) vem logo em seguida, para apresentações sem kernel.

## Estrutura

```text
├── data/                 Tabela 1 publicada + README dos dados
├── docs/                 diagnóstico e roteiro
├── notebooks/            01_mcnemar_safe_fall.ipynb
├── references/           artigo (PDF)
├── results/figures/      figuras geradas
├── slides/               build_slides.py, pptx_helpers.py, make_figures.py, assets/, .pptx final
├── src/safe_fall_statistics/
│   ├── data_loader.py         leitura da Tabela 1
│   ├── data_validation.py     auditoria da Tabela 1; validação de dados pareados/ausentes
│   ├── contingency_tables.py  PairedTable (a, b, c, d)
│   ├── mcnemar_analysis.py    p exato manual, scipy, statsmodels; mid-p; χ²; interpretação
│   ├── reconstruction.py      inferência de b e c a partir do X² publicado
│   ├── synthetic_data.py      ilustrações SINTÉTICAS do roteiro
│   ├── visualizations.py      gráficos na paleta do template
│   ├── interactive_demo.py    widget b × c
│   └── slide_examples.py      exemplos dos slides com controles
├── templates/            template oficial CIn-UFPE (.pptx); a referência visual em PDF fica só local
└── tests/                44 testes (pytest)
```

## Três tipos de dado — nunca misturados

* **PUBLICADO**: valores da Tabela 1, preservados mesmo onde são inconsistentes (as divergências são sinalizadas por
  `audit_table1`).
* **INFERIDO**: tabelas 2×2 do Safe Fall. O artigo publica só as margens, que fixam `c − b` mas não `b + c`. O X²
  impresso coincide exatamente com o McNemar com correção de continuidade, `(|c−b|−1)²/(b+c)`, o que identifica `b`
  e `c` (inteiros exatos nas 5 linhas; sem correção nenhuma linha fecha). É uma inferência, não um dado original.
* **SINTÉTICO**: as ilustrações do roteiro — monitoria (45, 10, 30, 15) e campanha (42, 3, 12, 43) — e a demonstração interativa.

## Template

O repositório trazia apenas um PDF do deck com a identidade CIn-UFPE. O `.pptx` oficial (`Apresentação Padrão CIn-UFPE`)
foi incorporado em `templates/template_cin_ufpe.pptx` e é aberto por `build_slides.py`: master, layouts, proporção,
divisórias e encerramento vêm do arquivo; os slides de conteúdo seguem a referência visual do PDF.
Fontes do template: Cambria (títulos) e Calibri (texto). Sem elas instaladas, o LibreOffice usa Caladea/Carlito, que têm
as mesmas métricas.
