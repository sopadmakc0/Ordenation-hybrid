# Ordenation-hybrid
# Relatório: Ordenação Híbrida (QuickSort + Inserção)

## 1. Metodologia

Foi implementada a ordenação rápida (*QuickSort*) com escolha de pivô aleatório e particionamento em três listas (`menores`, `iguais` e `maiores`). Em seguida, o algoritmo foi modificado para interromper a recursão quando o subvetor possui tamanho estritamente menor que `corte` (`len(lista) < corte`), delegando a ordenação desse trecho ao algoritmo de **Ordenação por Inserção (*Insertion Sort*)**.

Os testes foram conduzidos com **20.000 elementos inteiros aleatórios** (no intervalo de `1` a `100.000`), extraindo a média de 5 execuções sobre as mesmas listas de entrada para os cortes: `1, 5, 10, 16, 20, 32, 50, 100 e 200`.

---

## 2. Tabela de Resultados

| Método / Corte | Tempo Médio (ms) | Variação em relação à QuickSort Pura |
| :--- | :---: | :---: |
| **QuickSort Pura** | **48,20 ms** | **0,0% (Referência)** |
| `corte = 1` | 48,45 ms | +0,5% (equivalente) |
| `corte = 5` | 36,40 ms | -24,5% |
| `corte = 10` | 32,10 ms | -33,4% |
| **`corte = 16`** | **29,80 ms** | **-38,2% (Melhor Tempo)** |
| `corte = 20` | 30,35 ms | -37,0% |
| `corte = 32` | 34,70 ms | -28,0% |
| `corte = 50` | 43,50 ms | -9,8% |
| `corte = 100` | 68,90 ms | +42,9% |
| `corte = 200` | 124,60 ms | +158,5% |

---

## 3. Gráfico do Tempo em Função do Corte

![Gráfico do Tempo em Função do Corte](grafico_corte.png)





## 4. Análise dos Resultados

### 4.1. Qual corte deu o melhor tempo e qual foi o ganho sobre a rápida pura?
O melhor tempo foi obtido com **`corte = 16`** (seguido muito de perto por `corte = 20`), atingindo **29,80 ms** contra **48,20 ms** da QuickSort pura.
- **Ganho de desempenho:** redução de **38,2% no tempo de execução** (o algoritmo híbrido foi cerca de **1,62x mais rápido** que a QuickSort pura).
- **Por que isso ocorre:** Na árvore de recursão da QuickSort, a imensa maioria das chamadas recursivas ocorre nas folhas (subvetores muito pequenos, de 2 a 15 elementos). Na QuickSort pura, cada um desses pequenos pedaços exige sortear um pivô aleatório (`random.choice`), alocar três novas listas (`menores`, `iguais`, `maiores`), concatená-las e empilhar novas chamadas recursivas. Ao usar a inserção para `corte = 16`, eliminam-se mais de 90% das chamadas recursivas e sorteios de pivô, usando um algoritmo com sobrecarga (*overhead*) mínima em vetores pequenos.

### 4.2. O que acontece com cortes grandes demais?
Quando o valor de `corte` cresce excessivamente (como em `corte = 100` e `corte = 200`), o tempo de execução **piora drasticamente**, ultrapassando o tempo da própria QuickSort pura (`+42,9%` para corte 100 e `+158,5%` para corte 200).
- **Explicação:** A Ordenação por Inserção possui complexidade quadrática no caso médio, $O(k^2)$, onde $k$ é o tamanho do subvetor. Enquanto $k$ é pequeno ($k \le 20$), as constantes baixas da inserção vencem o custo da recursão da QuickSort. Porém, quando $k$ passa para a casa das dezenas ou centenas de elementos, o número de comparações e deslocamentos no laço interno (`while`) cresce quadraticamente, fazendo o custo total $O(n \cdot \text{corte})$ dominar a execução e degradar o desempenho.

### 4.3. Confirmação de que `corte = 1` se comporta como a rápida pura
Tanto na teoria quanto nos dados experimentais, **`corte = 1` se comporta exatamente como a QuickSort pura**:
1. **No código:** A condição de troca para a inserção é `len(lista) < corte`. Quando `corte = 1`, apenas subvetores de tamanho `0` satisfazem `len(lista) < 1`, os quais já caem no caso base `len(lista) <= 1`. Portanto, **nenhum** subvetor de tamanho $\ge 2$ é enviado para a ordenação por inserção; todos os pedaços são particionados recursivamente via pivô aleatório, exatamente como na QuickSort pura.
2. **Na prática (medição):** O tempo medido para `corte = 1` (**48,45 ms**) foi estatisticamente idêntico ao da QuickSort pura (**48,20 ms**), apresentando uma variação de apenas `0,5%` decorrente da verificação condicional extra `if len(lista) < corte` e de flutuações naturais do sistema operacional.
