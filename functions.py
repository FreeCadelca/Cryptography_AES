from GaluaField import IntM, GaluaItem, GaluaField, create_intm_list

Byte_conversions = dict()
irreducible_sub = create_intm_list([1, 0, 0, 0, 1, 1, 0, 1, 1], 2)
irreducible_mix = create_intm_list([1, 0, 0, 0, 1, 1, 0, 1, 1], 2)


def create_byte_conversions():
    for i in range(256):
        if i == 0:
            Byte_conversions[i] = 0
            continue
        bits = f"{i:08b}"
        galua_el = GaluaItem(2, 8, create_intm_list([int(i) for i in bits], 2))
        inv_galua_item = galua_el.inv(irreducible_sub)
        new_value = int(''.join(str(i.value) for i in inv_galua_item), 2)
        Byte_conversions[i] = new_value


def cyclic_shift_left(a: list, k: int):
    return [a[(k + i) % len(a)] for i in range(len(a))]


def rot_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        b[i] = cyclic_shift_left(a[i], i)
    return b


def sub_bytes(a: list[list]):
    if len(Byte_conversions.keys()) == 0:
        create_byte_conversions()
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = Byte_conversions[a[i][j]]


def byte_to_galua(n: int):
    return GaluaItem(2, 8, create_intm_list([int(i) for i in f"{n:08b}"], 2))


def mix_columns(a: list[list]):
    for j in range(len(a[0])):
        [a0j, a1j, a2j, a3j] = [a[i][j] for i in range(len(a))]
        a[0][j] = (byte_to_galua(a0j).multiply(GaluaItem(2, 8, [IntM(2, 8)]), irreducible_mix) +
                   byte_to_galua(a1j).multiply(GaluaItem(2, 8, [IntM(3, 8)]), irreducible_mix) +
                   byte_to_galua(a2j) +
                   byte_to_galua(a3j))
        a[1][j] = (byte_to_galua(a0j) +
                   byte_to_galua(a1j).multiply(GaluaItem(2, 8, [IntM(2, 8)]), irreducible_mix) +
                   byte_to_galua(a2j).multiply(GaluaItem(2, 8, [IntM(3, 8)]), irreducible_mix) +
                   byte_to_galua(a3j))
        a[2][j] = (byte_to_galua(a0j) +
                   byte_to_galua(a1j) +
                   byte_to_galua(a2j).multiply(GaluaItem(2, 8, [IntM(2, 8)]), irreducible_mix) +
                   byte_to_galua(a3j).multiply(GaluaItem(2, 8, [IntM(3, 8)]), irreducible_mix))
        a[3][j] = (byte_to_galua(a0j).multiply(GaluaItem(2, 8, [IntM(3, 8)]), irreducible_mix) +
                   byte_to_galua(a1j) +
                   byte_to_galua(a2j) +
                   byte_to_galua(a3j).multiply(GaluaItem(2, 8, [IntM(2, 8)]), irreducible_mix))
    return a


def add_round_key(a: list[list], round_key: list[list]):
    for i in range(len(a)):
        for j in range(len(a)):
            a[i][j] = a[i][j] ^ round_key[i][j]
    return a


def generate_round_keys(base_key: list[list]):
    round_keys = [base_key]
    for k in range(1, 11):
        new_round_key = [[0 for _ in range(4)] for _ in range(4)]
        new_round_key[0] = cyclic_shift_left(round_keys[k - 1][3], 1)
        new_round_key[0] = [Byte_conversions[j] for j in new_round_key[0]]
        new_round_key[0][0] ^= 2^k
        new_round_key[0] = [new_round_key[0][j] ^ round_keys[k - 1][0][j] for j in range(len(new_round_key[0]))]
        for i in range(1, 4):
            new_round_key[i] = [new_round_key[i][j] ^ round_keys[k - 1][i][j] for j in range(len(new_round_key[i]))]
            new_round_key[i] = [new_round_key[i][j] ^ new_round_key[i - 1][j] for j in range(len(new_round_key[i]))]
        round_keys.append(new_round_key)
    return round_keys

