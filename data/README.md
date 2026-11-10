# Dados

## `table1_published.csv` — dados publicados (fonte primária)

Transcrição literal da **Tabela 1** de DelCastillo-Andrés et al. (2018),
*Int. J. Environ. Res. Public Health* 15, 2669 (doi:10.3390/ijerph15122669, CC BY 4.0).

| Coluna | Significado |
|---|---|
| `pre_correct_n`, `pre_incorrect_n` | Nº de crianças que executaram a resposta corretamente/incorretamente no pré-teste |
| `post_correct_n`, `post_incorrect_n` | Idem, no pós-teste |
| `*_pct_reported` | Porcentagem **como impressa** no artigo (não recalculada) |
| `chi2_reported` | Coluna "X²" da tabela |
| `p_reported` | Coluna "p" (impressa como `0.000`, ou seja, p < 0,001) |

N = 122 crianças em todas as linhas. Os valores **não foram corrigidos**: as divergências
entre contagens e porcentagens são detectadas por `safe_fall_statistics.data_validation.audit_table1`.

O artigo **não** publica as frequências conjuntas pré×pós (`a`, `b`, `c`, `d`) nem microdados individuais.

## Dados derivados e sintéticos

* As tabelas 2×2 do Safe Fall usadas no notebook são **inferidas** por
  `safe_fall_statistics.reconstruction` a partir das margens + X² publicado,
  sob a hipótese (verificável) de que o X² é o qui-quadrado de McNemar com correção de continuidade.
  Não são dados originais.
* As ilustrações do roteiro (monitoria e campanha) e a demonstração interativa usam dados **sintéticos**
  (`safe_fall_statistics.synthetic_data`), gerados com semente fixa e marcados como tal.
