from GaluaField import IntM, GaluaItem, create_intm_list
from BytesConversionDict import *

irreducible_sub = create_intm_list([1, 0, 0, 0, 1, 1, 0, 1, 1], 2)
irreducible_mix = create_intm_list([1, 0, 0, 0, 1, 1, 0, 1, 1], 2)


def create_byte_conversions():
    for i in range(256):
        if i == 0:
            Byte_conversions[i] = 0
            continue
        bits = f"{i:08b}"
        galua_el = GaluaItem(2, 8, create_intm_list([int(k) for k in bits], 2))
        print("cur galua item:", *galua_el.coefficients)
        inv_galua_item = galua_el.inv(irreducible_sub)
        new_value = int(''.join(str(k.value) for k in inv_galua_item.coefficients), 2)
        Byte_conversions[i] = new_value


def cyclic_shift_left(a: list, k: int):
    return [a[(k + i) % len(a)] for i in range(len(a))]


def rot_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        b[i] = cyclic_shift_left(a[i], i)
    return b


def inv_rot_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        b[i] = cyclic_shift_left(a[i], -i)
    return b


def sub_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        for j in range(len(b[i])):
            b[i][j] = Byte_conversions[b[i][j]]
    return b


def inv_sub_bytes(a: list[list]):
    b = a.copy()
    for i in range(len(b)):
        for j in range(len(b[i])):
            b[i][j] = InvByte_conversions[b[i][j]]
    return b


def byte_to_galua(n: int):
    return GaluaItem(2, 8, create_intm_list([int(i) for i in f"{n:08b}"], 2))


def galua_to_byte(item: GaluaItem):
    return int(''.join([str(i.value) for i in item.coefficients]), 2)


def mix_columns(b: list[list]):
    a = b.copy()
    for j in range(len(a[0])):
        [a0j, a1j, a2j, a3j] = [a[i][j] for i in range(len(a))]
        a[0][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x02), irreducible_mix) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x03), irreducible_mix) +
                                byte_to_galua(a2j) +
                                byte_to_galua(a3j))
        a[1][j] = galua_to_byte(byte_to_galua(a0j) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x02), irreducible_mix) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x03), irreducible_mix) +
                                byte_to_galua(a3j))
        a[2][j] = galua_to_byte(byte_to_galua(a0j) +
                                byte_to_galua(a1j) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x02), irreducible_mix) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x03), irreducible_mix))
        a[3][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x03), irreducible_mix) +
                                byte_to_galua(a1j) +
                                byte_to_galua(a2j) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x02), irreducible_mix))
    return a


def inv_mix_columns(a: list[list]):
    for j in range(len(a[0])):
        [a0j, a1j, a2j, a3j] = [a[i][j] for i in range(len(a))]
        a[0][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x0E), irreducible_mix) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x0B), irreducible_mix) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x0D), irreducible_mix) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x09), irreducible_mix))
        a[1][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x09), irreducible_mix) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x0E), irreducible_mix) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x0B), irreducible_mix) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x0D), irreducible_mix))
        a[2][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x0D), irreducible_mix) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x09), irreducible_mix) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x0E), irreducible_mix) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x0B), irreducible_mix))
        a[3][j] = galua_to_byte(byte_to_galua(a0j).multiply(byte_to_galua(0x0B), irreducible_mix) +
                                byte_to_galua(a1j).multiply(byte_to_galua(0x0D), irreducible_mix) +
                                byte_to_galua(a2j).multiply(byte_to_galua(0x09), irreducible_mix) +
                                byte_to_galua(a3j).multiply(byte_to_galua(0x0E), irreducible_mix))
    return a


def add_round_key(b: list[list], round_key: list[list]):
    a = b.copy()
    for i in range(len(a)):
        for j in range(len(a)):
            a[i][j] = a[i][j] ^ round_key[i][j]
    return a


def generate_round_keys(base_key: list[list]):
    round_keys = [base_key]
    for k in range(1, 12):
        new_round_key = [[0 for _ in range(4)] for _ in range(4)]
        new_round_key[0] = cyclic_shift_left(round_keys[k - 1][3], 1)
        new_round_key[0] = [Byte_conversions[j] for j in new_round_key[0]]
        if k == 9:
            new_round_key[0][0] ^= 0x1B
        elif k == 10:
            new_round_key[0][0] ^= 0x36
        elif k == 11:
            new_round_key[0][0] ^= 0x6C
        else:
            new_round_key[0][0] ^= 2 ** (k - 1)
        new_round_key[0] = [new_round_key[0][j] ^ round_keys[k - 1][0][j] for j in range(len(new_round_key[0]))]
        for i in range(1, 4):
            new_round_key[i] = [new_round_key[i][j] ^ round_keys[k - 1][i][j] for j in range(len(new_round_key[i]))]
            new_round_key[i] = [new_round_key[i][j] ^ new_round_key[i - 1][j] for j in range(len(new_round_key[i]))]
        round_keys.append(new_round_key)
    return round_keys

# key = [[0x00, 0x01, 0x02, 0x03],
#        [0x04, 0x05, 0x06, 0x07],
#        [0x08, 0x09, 0x0A, 0x0B],
#        [0x0C, 0x0D, 0x0E, 0x0F]]

# keys = generate_round_keys(key)
# for key_i in keys:
#     print("------------------------")
#     for i in key_i:
#         for j in i:
#             print(j, end="\t")
#         print()
#     print("------------------------")
