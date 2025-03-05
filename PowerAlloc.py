def ComputingDist(A, B, lng_A, lng_B, D) -> list:
    # заполнение матрицы D
    for i in range(lng_A): 
        D[i][0] = i # удаление всех символов из A
        for j in range(lng_B): # вставка всех символов из B
            D[0][j] = j
            if i > 0 and j > 0:
                if A[i - 1] == B[j - 1]:
                    D[i][j] = D[i - 1][j - 1]
                else:
                    D[i][j] = min(D[i - 1][j] + 1,
                                  D[i][j - 1] + 1,
                                  D[i - 1][j - 1] + 1,
                    )

    return D

def main(): 
    A = input("Введите строку А: ")
    B = input("Введите строку B: ")

    lng_A = len(A) + 1
    lng_B = len(B) + 1

    # простор для вычислений
    D = [[0 for _ in range(lng_B)] for _ in range(lng_A)]


    result = ComputingDist(A, B, lng_A, lng_B, D)

    # корректный вывод матрицы
    for row in result:
        for elem in row:
            print(str(elem).ljust(3), end=" ")
        print()

    print()
    
    print(f"Расстояние Левенштейна между \"{A}\" \"{B}\": {result[lng_A - 1][lng_B - 1]} ")

main()