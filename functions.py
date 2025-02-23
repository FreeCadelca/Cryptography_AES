from GaluaField import IntM, GaluaItem, GaluaField, create_intm_list

Byte_conversions = dict()
irreducible = create_intm_list([1, 0, 0, 0, 1, 1, 0, 1, 1], 2)


def cyclic_shift_left(a: list, k: int):
    return [a[(k + i) % len(a)] for i in range(len(a))]


def rot_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        b[i] = cyclic_shift_left(a[i], i)
    return b


def sub_bytes(a: list[list]):
    if len(Byte_conversions.keys()) == 0:
        for i in range(256):
            if i == 0:
                Byte_conversions[i] = 0
                continue
            bits = f"{i:08b}"
            galua_el = GaluaItem(2, 8, create_intm_list([int(i) for i in bits], 2))
            inv_galua_item = galua_el.inv(irreducible)
            new_value = int(''.join(str(i.value) for i in inv_galua_item), 2)
            Byte_conversions[i] = new_value
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = Byte_conversions[a[i][j]]
