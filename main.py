import math

class UncertainNumber:
    def __init__(self, value, uncertainty):
        self.value = float(value)
        self.unc = abs(float(uncertainty))  # абсолютная погрешность всегда положительная

    def __repr__(self):
        return f"{self.value:.10g} ± {self.unc:.10g}"

    def add(self, other):
        z = self.value + other.value
        dz = self.unc + other.unc
        return UncertainNumber(z, dz)

    def sub(self, other):
        z = self.value - other.value
        dz = self.unc + other.unc
        return UncertainNumber(z, dz)

    def mul(self, other):
        z = self.value * other.value
        dz = abs(self.value * other.unc) + abs(other.value * self.unc)
        return UncertainNumber(z, dz)

    def div(self, other):
        if other.value == 0:
            raise ValueError("Деление на ноль")
        z = self.value / other.value
        rel_x = self.unc / abs(self.value) if self.value != 0 else float('inf')
        rel_y = other.unc / abs(other.value)
        dz = abs(z) * (rel_x + rel_y)
        return UncertainNumber(z, dz)

    def pow(self, n):
        """Возведение в степень n (n — точное число без погрешности)"""
        if self.value == 0 and n <= 0:
            raise ValueError("Недопустимая степень")
        z = self.value ** n
        if self.value == 0:
            dz = 0
        else:
            rel_err = abs(n) * (self.unc / abs(self.value))
            dz = abs(z) * rel_err
        return UncertainNumber(z, dz)

    def root(self, k):
        """Извлечение корня k-й степени (k — точное целое число)"""
        if self.value < 0 and k % 2 == 0:
            raise ValueError("Чётный корень из отрицательного числа")
        if k == 0:
            raise ValueError("Корень нулевой степени недопустим")
        n = 1.0 / k
        return self.pow(n)

def read_uncertain():
    while True:
        try:
            s = input("Введите число и абсолютную погрешность (через пробел, например: 10.5 0.1): ")
            val, unc = map(float, s.split())
            return UncertainNumber(val, unc)
        except:
            print("Неверный формат. Попробуйте снова.")

print("Простой калькулятор с учётом погрешностей")
print("Доступные операции: +, -, *, /, ^ (степень), root (корень)")
print("Для степени и корня второе число — точный показатель (целое, без погрешности)")
print("Введите 'exit' для выхода\n")

numbers = []  # храним введённые числа

while True:
    print("\nТекущие числа:")
    for i, num in enumerate(numbers):
        print(f"{i}: {num}")
    
    if len(numbers) < 2:
        action = input("\nВведите 'add' для добавления нового числа или 'exit': ").strip().lower()
        if action == 'exit':
            break
        elif action == 'add':
            num = read_uncertain()
            numbers.append(num)
        else:
            print("Сначала добавьте хотя бы два числа.")
        continue

    op = input("\nВведите операцию (например, 0 + 1, или 0 ^ 3, или 0 root 2): ").strip()
    if op == 'exit':
        break

    try:
        parts = op.split()
        if len(parts) != 3:
            raise ValueError
        i = int(parts[0])
        operation = parts[1]
        j = int(parts[2]) if operation not in ('^', 'root') else float(parts[2])

        if i >= len(numbers) or (operation not in ('^', 'root') and j >= len(numbers)):
            raise IndexError

        a = numbers[i]
        if operation in ('^', 'root'):
            if operation == '^':
                result = a.pow(j)
            else:
                result = a.root(j)
        else:
            b = numbers[j]
            if operation == '+':
                result = a.add(b)
            elif operation == '-':
                result = a.sub(b)
            elif operation == '*':
                result = a.mul(b)
            elif operation == '/':
                result = a.div(b)
            else:
                raise ValueError("Неизвестная операция")

        print(f"Результат: {result}")
        # Можно добавить результат в список
        add_res = input("Добавить результат в список? (y/n): ").strip().lower()
        if add_res == 'y':
            numbers.append(result)

    except Exception as e:
        print(f"Ошибка: {e}. Попробуйте снова.")