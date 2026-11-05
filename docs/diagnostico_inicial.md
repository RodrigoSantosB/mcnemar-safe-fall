# Diagnóstico inicial

## 1. Auditoria do repositório (estado encontrado)

| Item | Situação |
|---|---|
| Artigo | `ijerph-15-02669.pdf` (9 p., versão MDPI com camada de texto duplicada) → movido para `references/` |
| Template de slides | **Nenhum `.pptx` no repositório.** Havia apenas `ML_PROJ_MLP.pdf`, um deck exportado do Google Slides com a identidade CIn-UFPE → movido para `templates/referencia_visual_ML_PROJ_MLP.pdf` |
| Dados | Nenhum arquivo de dados ou microdados |
| Código / notebooks | Nenhum |
| Figuras do artigo | Figura 1 (fotos da aplicação) e imagem do Apêndice A (posição inicial) → extraídas para `slides/assets/` |

**Decisão sobre o template.** O arquivo oficial `Apresentação Padrão CIn-UFPE.pptx` (encontrado em `~/Downloads`, mesma
identidade visual do PDF de referência, mantido apenas localmente e fora do Git) foi copiado para `templates/template_cin_ufpe.pptx` e é aberto pelo gerador como
base: master, layouts, proporção 16:9 (10 × 5,625 in), paleta (#DB1E2F, #AF0421), divisória de seção e slide de
encerramento são clonados do próprio arquivo. A moldura dos slides de conteúdo (rótulo de seção cinza, título vermelho em
Cambria, logo CIn no canto superior direito, número da página, cartões, caixa escura de destaque) reproduz a referência
visual do repositório; as cores foram amostradas em pixels do PDF.

## 2. Resumo do artigo

DelCastillo-Andrés *et al.* (2018), *IJERPH* 15:2669 — avaliam se o programa **Safe Fall** melhora a resposta motora de
escolares numa **queda para trás**.

* **Desenho:** piloto exploratório, **quase experimental**, pré/pós, **sem grupo controle**, amostragem por conveniência.
* **Amostra:** 122 crianças de 10–12 anos (44/54/24), 5º e 6º anos de escolas públicas de Sevilha, 2016/17.
* **Intervenção:** aula teórica (1 h) → pré-teste → aula prática (50 min) → 10 sessões de 10 min no aquecimento → pós-teste
  (24/04 a 02/06/2017).
* **Instrumento:** escala observacional ad hoc **INFOSECA** — 5 critérios dicotômicos (pescoço, mãos, tronco, quadril,
  joelhos), Kappa 0,75–0,98.
* **Análise:** McNemar exato (SPSS 24), α = 0,05.
* **Resultado:** mudança significativa nas 5 respostas; > 85 % corretas no pós-teste.
* **Limitações reconhecidas:** sem controle, contexto de laboratório, só quedas para trás; redução de lesões **não** testada.

## 3. Conferência da Tabela 1

* Contagens somam 122 em todas as linhas (coerentes).
* **Porcentagens do pré-teste não correspondem a n/122** em nenhuma linha (ex.: 28 → 23,6 % impresso, 22,95 % real;
  1 → 1,6 % impresso, 0,82 % real — o texto do artigo diz 0,8 %).
* **Mãos, pós-teste:** 107 impresso como 90,2 % (real 87,7 %) e 15 como 9,8 % (real 12,3 %) — idênticos à linha do pescoço,
  provável erro de cópia, repetido no texto.
* **Enrolamento, pós:** 91,1 % impresso, 90,98 % real.
* `p = 0.000` é arredondamento → relatar **p < 0,001**.
* Outros detalhes menores: 50,4 %/49,6 % de meninos/meninas não correspondem a inteiros de 122; 52,8/47,2 % para 64/58
  (real 52,5/47,5 %).

## 4. Disponibilidade de dados e consequência para a análise

O artigo **não** publica `a, b, c, d` nem microdados. As margens fixam apenas `c − b`. Porém o **X²** impresso coincide,
nas cinco linhas, com o McNemar **com correção de continuidade**: `b + c = (|c − b| − 1)² / X²` sai exatamente inteiro
(86, 106, 106, 105, 52) e o X² é reproduzido na 3ª casa — o que não ocorre sem correção. Daí as tabelas **inferidas**:

| Comportamento | a | b | c | d | p exato |
|---|---:|---:|---:|---:|---|
| Pescoço | 26 | 2 | 84 | 10 | 9,7·10⁻²³ |
| Mãos | 1 | 0 | 106 | 15 | 2,5·10⁻³² |
| Enrolamento | 7 | 2 | 104 | 9 | 1,4·10⁻²⁸ |
| Quadril | 1 | 0 | 105 | 16 | 4,9·10⁻³² |
| Joelhos | 66 | 2 | 50 | 4 | 6,1·10⁻¹³ |

Essas tabelas são sempre rotuladas **INFERIDO**. Os exemplos de educação e a demonstração interativa usam dados
**SINTÉTICOS**. Assim, o projeto cobre a Análise A (publicado), a Análise B (sintético) e, adicionalmente, a inferência.
