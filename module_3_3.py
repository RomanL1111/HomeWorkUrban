# Первая часть

def print_params(a=1, b='строка', c=True):
    print(a, b, c)

print_params()
print_params(10)
print_params(10, 20)
print_params(10, 20, False)
print_params(b = 25)
print_params(c = [1, 2, 3])

# Вторая часть

values_list = [3.14, 'текст', False]
values_dict = {'a': 42, 'b': 'новая строка', 'c': 1.25}

print_params(*values_list)
print_params(**values_dict)

# Третья часть
values_list_2 = [54.32, 'Строка']
print_params(*values_list_2, 42)

