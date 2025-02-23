class IntM:
    def __init__(self, v: int, m: int):
        self.modulus = m
        self.value = v

    def __add__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value + other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value + other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value - other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value - other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value * other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value * other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __floordiv__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            v = self.value
            while v % other.value != 0:
                v += self.modulus
            return IntM(v // other.value, self.modulus)
        elif isinstance(other, int):
            v = self.value
            while v % other != 0:
                v += self.modulus
            return IntM(v // other, self.modulus)
        else:
            raise ValueError

    def __gt__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            raise ValueError

    def __lt__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            raise ValueError

    def __ge__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            raise ValueError

    def __le__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            raise ValueError

    def __eq__(self, other):
        if isinstance(other, IntM):
            return self.modulus == other.modulus and self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            raise ValueError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f'{self.value}m{self.modulus}'


def create_intm_list(lst: list, modulus: int):
    return [IntM(i, modulus) for i in lst]


def trimListWithZeros(lst: list):
    max_pow = 0
    for i in range(len(lst) - 1, -1, -1):
        if lst[i].value != 0:
            max_pow = len(lst) - 1 - i
    lst = lst[len(lst) - 1 - max_pow:]
    return lst


class GaluaItem:
    def __init__(self, p, n, coefs: list):
        self.coefficients = coefs
        self.p = p
        self.n = n

    def copy(self):
        return GaluaItem(self.p, self.n, coefs=self.coefficients.copy())

    def __copy__(self):
        return self.copy()

    def __len__(self):
        return self.n + 1

    def __add__(self, other):
        if len(self.coefficients) >= len(other.coefficients):
            newGaluaItem = self.copy()
            for i in range(len(other.coefficients)):
                newGaluaItem.coefficients[len(newGaluaItem.coefficients) - 1 - i] += \
                    (other.coefficients)[len(other.coefficients) - 1 - i]
        else:
            newGaluaItem = other.copy()
            for i in range(len(self.coefficients)):
                newGaluaItem.coefficients[len(newGaluaItem.coefficients) - 1 - i] += (
                    self.coefficients)[len(self.coefficients) - 1 - i]
        return newGaluaItem

    def __sub__(self, other):
        newGaluaItem = self.copy()
        for i in range(min(len(newGaluaItem.coefficients), len(other.coefficients))):
            newGaluaItem.coefficients[i] -= other.coefficients[i]
        return newGaluaItem

    # перемножение многочленов методом фонтанчика
    def fontain(self, other):
        self.coefficients = trimListWithZeros(self.coefficients)
        other.coefficients = trimListWithZeros(other.coefficients)

        max_pow = len(self.coefficients) + len(other.coefficients) - 2
        pre_res = [IntM(0, self.p) for i in range(max_pow + 1)]
        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                power_i = len(self.coefficients) - 1 - i
                power_j = len(other.coefficients) - 1 - j
                pre_res[max_pow - (power_i + power_j)] += self.coefficients[i] * other.coefficients[j]
        return trimListWithZeros(pre_res)

    # def __get_big_degrees__(irreducible, max_pow):

    def multiply(self, other, irreducible: list[IntM]):
        def __get_big_degrees__(irreducible) -> dict:
            BigDegrees = dict()
            # выражаем наибольшую степень из неприводимого многочлена
            BigDegrees[len(irreducible) - 1] = \
                [irreducible[i] * -1 // irreducible[0] for i in range(1, len(irreducible))]
            BigDegrees[len(irreducible) - 1] = trimListWithZeros(BigDegrees[len(irreducible) - 1])
            for new_degree in range(len(irreducible), len(irreducible) * 2 - 3):
                lastDegreeInGaluaItem = GaluaItem(
                    BigDegrees[new_degree - 1][0].modulus,
                    len(irreducible) - 1,
                    BigDegrees[new_degree - 1].copy()
                )
                singleXInGaluaItem = GaluaItem(
                    BigDegrees[new_degree - 1][0].modulus,
                    len(irreducible) - 1,
                    create_intm_list([1, 0], BigDegrees[new_degree - 1][0].modulus)
                )
                BigDegrees[new_degree] = lastDegreeInGaluaItem.fontain(singleXInGaluaItem)
                if len(BigDegrees[new_degree]) == len(irreducible):
                    multedPoly = GaluaItem(self.p, self.n, BigDegrees[len(BigDegrees[new_degree]) - 1]).fontain(
                        GaluaItem(self.p, self.n, [BigDegrees[new_degree][0]])
                    )
                    for indexInAddPoly in range(len(multedPoly)):
                        BigDegrees[new_degree][len(BigDegrees[new_degree]) - 1 - indexInAddPoly] += multedPoly[
                            len(multedPoly) - 1 - indexInAddPoly]
                    BigDegrees[new_degree][0].value = 0
                    BigDegrees[new_degree] = trimListWithZeros(BigDegrees[new_degree])
            # for key, item in BigDegrees.items():
            #     print(f'x^{key}:', *item)
            return BigDegrees

        bigDegreesDict = __get_big_degrees__(irreducible)

        # Выполняем умножение методом фонтанчика
        pre_res = self.fontain(other)

        # Подставляем в высокие степени многочлена, используя наш словарь,
        # в котором мы выражали все такие "большие" степени
        for i in range(0, len(pre_res) - self.n):
            multedPoly = GaluaItem(self.p, self.n, bigDegreesDict[len(pre_res) - 1 - i]).fontain(
                GaluaItem(self.p, self.n, [pre_res[i]])
            )
            for indexInAddPoly in range(len(multedPoly)):
                pre_res[len(pre_res) - 1 - indexInAddPoly] += multedPoly[len(multedPoly) - 1 - indexInAddPoly]
            pre_res[i].value = 0
        pre_res = trimListWithZeros(pre_res)
        return GaluaItem(self.p, self.n, pre_res)

    def inv(self, irreducible):
        temp_res = self.copy()
        temp_res.coefficients = trimListWithZeros(temp_res.coefficients)
        while (len(temp_res.multiply(self, irreducible).coefficients) != 1 or
               temp_res.multiply(self, irreducible).coefficients[0].value != 1):
            temp_res = temp_res.multiply(self, irreducible)
        return temp_res

    def division(self, other, irreducible):
        return self.multiply(other.inv(irreducible), irreducible)

    def divmod(self, other):
        dividend = self.coefficients.copy()
        divisor = other.coefficients.copy()
        divisor = trimListWithZeros(divisor)

        result_degree = len(dividend) - len(divisor)  # Степень результата
        if result_degree < 0:
            return GaluaItem(self.p, self.n, [IntM(0, self.p)]), self
        result = [IntM(0, self.p) for _ in range(result_degree + 1)]

        # Деление методом старших коэффициентов
        while len(dividend) >= len(divisor):
            lead_coeff_dividend = dividend[0]
            lead_coeff_divisor = divisor[0]
            lead_term = lead_coeff_dividend // lead_coeff_divisor  # Делим старшие коэффициенты
            result[len(dividend) - len(divisor)] = lead_term

            for i in range(len(divisor)):
                dividend[i] -= divisor[i] * lead_term
            dividend = trimListWithZeros(dividend)

        result = result[::-1]
        result = trimListWithZeros(result)

        # Возвращаем частное и остаток
        return GaluaItem(self.p, self.n, result), GaluaItem(self.p, self.n, dividend)

    def __hash__(self):
        return hash(f'{self.p}{self.n}{''.join(str(i.value) for i in self.coefficients)}')

    def __eq__(self, other):
        if self.n != other.n or self.p != other.p:
            return False
        if len(self.coefficients) != len(other.coefficients):
            return False
        for i in range(len(other.coefficients)):
            if self.coefficients[i] != other.coefficients[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        self.coefficients = trimListWithZeros(self.coefficients)
        other.coefficients = trimListWithZeros(other.coefficients)
        if len(self.coefficients) > len(other.coefficients):
            return True
        elif len(self.coefficients) < len(other.coefficients):
            return False
        else:
            for i in range(len(self.coefficients)):
                if self.coefficients[i] == other.coefficients[i]:
                    continue
                else:
                    return self.coefficients[i] > other.coefficients[i]
        return True

    def degree(self):
        return len(trimListWithZeros(self.coefficients)) - 1


def find_irreducible(p: int, n: int, count: int = 1) -> list[list[IntM]]:
    def rec(pos=n) -> list:
        simple_values = [[j] for j in range(p)]

        if pos <= 0:
            return simple_values

        new_values = []
        for i in range(len(simple_values)):
            for adjacent in rec(pos=pos - 1):
                new_values.append(simple_values[i] + adjacent)
        return new_values

    items = rec()
    items_galua = [GaluaItem(p, n, create_intm_list(item, p)) for item in items]
    potential_irreducibles = [i for i in items_galua if i.coefficients[0] != 0]
    irreducibles = []

    for potential_irreducible in potential_irreducibles:
        is_irreducible = True
        for i in items_galua:
            if i >= potential_irreducible or i.degree() == 0 or i.degree() == potential_irreducible.degree():
                continue
            c, ost = potential_irreducible.divmod(i)
            if len(ost.coefficients) == 1 and ost.coefficients[0].value == 0:
                is_irreducible = False
                break
        if is_irreducible:
            irreducibles.append(potential_irreducible.coefficients)
            if len(irreducibles) == count:
                return irreducibles
    return irreducibles


class GaluaField:
    def __init__(self, p, n, irreducible):
        self.p = p
        self.n = n
        self.irreducible = irreducible

    def find_elements(self):
        def rec(pos=self.n - 1) -> list:
            # Делаем "простые элементы", состоящие из одного компонента - последнего (0, 1, 2, 3, 4, ... (p-1))
            simple_values = [[j] for j in range(self.p)]

            # если это последняя позиция (самая последняя компонента), то возвращаем список простых элементов поля
            if pos <= 0:
                return simple_values

            # иначе рекурсивно прибавляем к простым элементам следующие такие же списки
            new_values = []
            for i in range(len(simple_values)):
                for adjacent in rec(pos=pos - 1):
                    new_values.append(simple_values[i] + adjacent)
            return new_values

        # запускаем рекурсию и записываем результат в items
        items = rec()

        items_galua = [GaluaItem(self.p, self.n, create_intm_list(item, self.p)) for item in items]
        return items_galua

    def display(self):
        items = self.find_elements()

        # собираем форматированную строку для вывода
        s = ""
        for item in items:
            # флаг, обозначающий, вывелся ли первый ненулевой элемент, чтобы знать, когда выводить " + "
            fl = 0
            for i in range(len(item.coefficients)):
                if item.coefficients[i].value != 0:
                    if fl == 0:
                        fl = 1
                    else:
                        s += ' + '
                    if self.n - i - 1 == 0:
                        s += f'{item.coefficients[i].value}'
                    elif self.n - i - 1 == 1:
                        s += f'{item.coefficients[i].value}x'
                    else:
                        s += f'{item.coefficients[i].value}x{self.n - i - 1}'
            if fl == 0:
                s += '0'
            s += ';\n'
        print(s)

    def find_orders(self):
        items = self.find_elements()
        items = items[1:]
        orders = dict()
        for item in items:
            current_order = 1
            temp_res = item.copy()
            temp_res.coefficients = trimListWithZeros(temp_res.coefficients)
            while len(temp_res.coefficients) != 1 or temp_res.coefficients[0].value != 1:
                temp_res = temp_res.multiply(item, self.irreducible)
                current_order += 1
            orders[item] = current_order
        return orders

    def find_forming_elements(self):
        orders = self.find_orders()
        forming_elements = []
        for item in orders.keys():
            if orders[item] == self.p ** self.n - 1:
                forming_elements.append(item)
        return forming_elements

    def decompose_by_forming_element(self, forming: GaluaItem):
        temp_res = forming.copy()
        print(*temp_res.coefficients)
        while len(temp_res.coefficients) != 1 or temp_res.coefficients[0].value != 1:
            temp_res = temp_res.multiply(forming, self.irreducible)
            print(*temp_res.coefficients)


# # Пример неприводимого многочлена x^4 + x^3 + 1
# irreducible = create_intm_list([1, 1, 0, 0, 1], 2)
# gf = GaluaField(4, 4, irreducible)
# # orders = gf.find_orders()
# # for i in orders.keys():
# #     print(*i.coefficients, " - ", orders[i])
# # fe = gf.find_forming_elements()
# # for i in fe:
# #     print(*i.coefficients)
# # print()
# # gf.decompose_by_forming_element(fe[2])
#
# a = GaluaItem(gf.p, gf.n, create_intm_list([3, 2, 0, 1], gf.p))
# b = GaluaItem(gf.p, gf.n, create_intm_list([0, 1, 0, 1], gf.p))
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток

# irreducible = create_intm_list([1, 1, 0, 0, 1], 2)
# gf = GaluaField(4, 4, irreducible)
# a = GaluaItem(gf.p, gf.n, create_intm_list([3, 2, 0, 1], gf.p))
# b = GaluaItem(gf.p, gf.n, create_intm_list([0, 1, 0, 1], gf.p))
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток
#
# irreducible = create_intm_list([1, 0, 0, 1, 1], 2)  # x^4 + x + 1
# gf = GaluaField(2, 4, irreducible)
# a = GaluaItem(gf.p, gf.n, create_intm_list([3, 1, 2, 1, 0, 1, 1], gf.p))  # 3x^6 + x^5 + 2x^4 + x^3 + x + 1
# b = GaluaItem(gf.p, gf.n, create_intm_list([1, 0, 1, 1], gf.p))  # x^3 + x + 1
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток
#
# irreducible = create_intm_list([1, 0, 2, 1], 3)  # x^3 + 2x + 1
# gf = GaluaField(3, 3, irreducible)
# a = GaluaItem(gf.p, gf.n, create_intm_list([2, 1, 1, 0, 2, 2], gf.p))  # 2x^5 + x^4 + x^3 + 2x + 2
# b = GaluaItem(gf.p, gf.n, create_intm_list([1, 2, 1], gf.p))  # x^2 + 2x + 1
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток
#
# irreducible = create_intm_list([1, 0, 1, 3], 7)  # x^3 + x + 3
# gf = GaluaField(7, 3, irreducible)
# a = GaluaItem(gf.p, gf.n, create_intm_list([6, 3, 1, 1, 0, 5, 2], gf.p))  # 6x^6 + 3x^5 + x^4 + x^3 + 5x + 2
# b = GaluaItem(gf.p, gf.n, create_intm_list([1, 4, 6], gf.p))  # x^2 + 4x + 6
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток


# p, n = 3, 4
# a = GaluaItem(p, n, create_intm_list([2, 0, 0, 2, 1], p))  # x^4 + 1
# b = GaluaItem(p, n, create_intm_list([1, 0, 0, 1, 2], p))  # x
# c, ost = a.divmod(b)
# print("Частное:", *c.coefficients)  # Ожидаемое частное
# print("Остаток:", *ost.coefficients)  # Ожидаемый остаток
# for i in find_irreducible(3, 4, count=10000):
#     print(*i)

# p, n = 11, 2
# a = GaluaItem(p, n, create_intm_list([0, 2], p))  # x^4 + 1
# b = GaluaItem(p, n, create_intm_list([1], p))  # x
# gf = GaluaField(p, n, find_irreducible(11, 2)[0])
# b_inv = b.inv(gf.irreducible)
# c = a.multiply(b_inv, gf.irreducible)
# print("Частное:", *b_inv.coefficients)
# print("Остаток:", *c.coefficients)