def optimal_way(costs_matrix, sum_costs,n , k):
    sum_costs[0][0] = costs_matrix[0][0] 
    
    for i in range(1, n):
        sum_costs[i][0] = sum_costs[i-1][0] + costs_matrix[i][0]
    for j in range(1, k):
        sum_costs[0][j] = sum_costs[0][j-1] + costs_matrix[0][j]


    for i in range(1, n):
        for j in range(1,k):
            sum_costs[i][j] = max(sum_costs[i-1][j], 
                                    sum_costs[i][j-1]) + costs_matrix[i][j]

            
    return sum_costs


def main():

    n,k = int(input("Кол-во строк: ")), int(input("Кол-во столбцов: "))

    sum_costs = [[0]* k for _ in range(n)] # матрица сумм
    
    
    costs_matrix = [[0]*k for _ in range(n)] # матрица цен
    print("Введите элементы матрицы цен (nxk): ")
    for i in range(n):
        costs_matrix[i] = [int(num) for num in input().split()]

    print()

    print("Вы ввели:")
    for row in costs_matrix:
        # Преобразуем каждый элемент в строку и выравниваем по левому краю
        formatted_row = [str(element).ljust(3) for element in row]
        # Объединяем элементы строки в одну строку и выводим
        print(" ".join(formatted_row))
    

    res = optimal_way(costs_matrix, sum_costs, n, k)

    print(f"Итого сумма при оптимальном пути: {res[n-1][k-1]}")
main()
