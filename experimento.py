import random
import time
import matplotlib.pyplot as plt


def insercao(lista):
    arr = lista[:]  
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr



def quicksort_pura(lista):
    if len(lista) <= 1:
        return lista

    pivo = random.choice(lista)
    menores = []
    iguais = []
    maiores = []

    for x in lista:
        if x < pivo:
            menores.append(x)
        elif x == pivo:
            iguais.append(x)
        else:
            maiores.append(x)

    return quicksort_pura(menores) + iguais + quicksort_pura(maiores)



def quicksort_hibrida(lista, corte):
    
    if len(lista) <= 1:
        return lista

   
    if len(lista) < corte:
        return insercao(lista)

    pivo = random.choice(lista)
    menores = []
    iguais = []
    maiores = []

    for x in lista:
        if x < pivo:
            menores.append(x)
        elif x == pivo:
            iguais.append(x)
        else:
            maiores.append(x)

    return (
        quicksort_hibrida(menores, corte)
        + iguais
        + quicksort_hibrida(maiores, corte)
    )



def executar_experimento():
    N = 20_000
    REPETICOES = 5  
    cortes = [1, 5, 10, 16, 20, 32, 50, 100, 200]

    random.seed(42)
   
    listas_base = [
        [random.randint(1, 100_000) for _ in range(N)]
        for _ in range(REPETICOES)
    ]
    gabarito = sorted(listas_base[0])

   
    tempos_pura = []
    for i in range(REPETICOES):
        entrada = listas_base[i][:]
        inicio = time.perf_counter()
        resultado = quicksort_pura(entrada)
        fim = time.perf_counter()
        if i == 0:
            assert resultado == gabarito, "Erro na ordenação QuickSort Pura!"
        tempos_pura.append((fim - inicio) * 1000)  

    tempo_medio_pura = sum(tempos_pura) / REPETICOES

   
    tempos_hibrida = {}
    for corte in cortes:
        tempos_corte = []
        for i in range(REPETICOES):
            entrada = listas_base[i][:]
            inicio = time.perf_counter()
            resultado = quicksort_hibrida(entrada, corte)
            fim = time.perf_counter()
            if i == 0:
                assert (
                    resultado == gabarito
                ), f"Erro na ordenação com corte={corte}!"
            tempos_corte.append((fim - inicio) * 1000)  

        tempos_hibrida[corte] = sum(tempos_corte) / REPETICOES

    
    print(f"Tempo médio QuickSort Pura: {tempo_medio_pura:.2f} ms\n")
    print("| Método / Corte | Tempo Médio (ms) | Diferença vs. Rápida Pura |")
    print("| :--- | :---: | :---: |")
    print(f"| **QuickSort Pura** | **{tempo_medio_pura:.2f}** | **0,0% (referência)** |")
    for corte in cortes:
        t = tempos_hibrida[corte]
        diff = ((t - tempo_medio_pura) / tempo_medio_pura) * 100
        sinal = "+" if diff > 0 else ""
        print(f"| Corte = {corte} | {t:.2f} | {sinal}{diff:.1f}% |")

   
    plt.figure(figsize=(10, 6))
    valores_y = [tempos_hibrida[c] for c in cortes]

    plt.plot(cortes, valores_y, marker="o", linewidth=2, label="QuickSort Híbrida (Rápida + Inserção)")
    plt.axhline(
        y=tempo_medio_pura,
        color="r",
        linestyle="--",
        linewidth=1.5,
        label=f"QuickSort Pura ({tempo_medio_pura:.2f} ms)",
    )

    melhor_corte = min(tempos_hibrida, key=tempos_hibrida.get)
    melhor_tempo = tempos_hibrida[melhor_corte]
    plt.annotate(
        f"Melhor ponto: corte={melhor_corte}\n({melhor_tempo:.2f} ms)",
        xy=(melhor_corte, melhor_tempo),
        xytext=(melhor_corte + 15, melhor_tempo - 3),
        arrowprops=dict(arrowstyle="->", color="green"),
        fontsize=10,
        fontweight="bold",
        color="green",
    )

    plt.title("Tempo de Execução vs. Ponto de Corte (20.000 elementos)", fontsize=13)
    plt.xlabel("    Tamanho do Corte (elementos)", fontsize=11)
    plt.ylabel("Tempo Médio de Execução (ms)", fontsize=11)
    plt.xticks(cortes)
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_corte.png", dpi=150)
    print("\nGráfico salvo com sucesso em 'grafico_corte.png'!")


if __name__ == "__main__":
    executar_experimento()