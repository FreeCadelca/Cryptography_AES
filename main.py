from functions import *

with open("plaintext.txt", "rb") as file:
    data = [i for i in file.read()]

# создание блоков
if len(data) % 16 != 0:
    data += [32] * (16 - len(data) % 16)
blocks = []
for i in range(0, len(data), 16):
    blocks.append(
        [data[i + j * 4:i + (j + 1) * 4] for j in range(4)]
    )

# создание блока ключа
with open("key", "rb") as file:
    key = [i for i in file.read()]
print(key)
if len(key) > 16:
    for i in range(16, len(key)):
        key[i % 16] ^= key[i]
    key = key[:16]
print(key)
if len(key) < 16:
    key += [0] * (16 - len(key))
key_block = [key[j * 4:(j + 1) * 4] for j in range(4)]
print(key_block)

# создание раундовых ключей
round_keys = generate_round_keys(key_block)
for i in round_keys:
    print(i)

# шифрование каждого блока
encrypted_blocks = []
for block in blocks:
    new_block = block.copy()
    for cur_round in range(11):
        new_block = sub_bytes(new_block)
        new_block = rot_bytes(new_block)
        new_block = mix_columns(new_block)
        new_block = add_round_key(new_block, round_keys[cur_round])
    new_block = sub_bytes(new_block)
    new_block = rot_bytes(new_block)
    new_block = add_round_key(new_block, round_keys[-1])
    encrypted_blocks.append(new_block)

# перевод блоков обратно в текст
data_enc = []
for block in encrypted_blocks:
    for i in range(len(block)):
        for j in range(len(block[i])):
            data_enc.append(block[i][j])

# запись в файл
with open("ciphertext.txt", "wb") as f:
    f.write(bytes(data_enc))

# расшифрование -----------------------------------------------------------------

with open("ciphertext.txt", "rb") as file:
    data = [i for i in file.read()]

# создание блоков
if len(data) % 16 != 0:
    data += [32] * (16 - len(data) % 16)
blocks = []
for i in range(0, len(data), 16):
    blocks.append(
        [data[i + j * 4:i + (j + 1) * 4] for j in range(4)]
    )

# создание блока ключа
with open("key", "rb") as file:
    key = [i for i in file.read()]
print(key)
if len(key) > 16:
    for i in range(16, len(key)):
        key[i % 16] ^= key[i]
    key = key[:16]
print(key)
if len(key) < 16:
    key += [0] * (16 - len(key))
key_block = [key[j * 4:(j + 1) * 4] for j in range(4)]
print(key_block)

# создание раундовых ключей
round_keys = generate_round_keys(key_block)
for i in round_keys:
    print(i)

# расшифрование каждого блока
decrypted_blocks = []
for block in blocks:
    new_block = block.copy()
    new_block = add_round_key(new_block, round_keys[-1])
    new_block = inv_sub_bytes(new_block)
    new_block = inv_rot_bytes(new_block)
    for cur_round in range(10, -1, -1):
        new_block = add_round_key(new_block, round_keys[cur_round])
        new_block = inv_mix_columns(new_block)
        new_block = inv_sub_bytes(new_block)
        new_block = inv_rot_bytes(new_block)
    # new_block = inv_sub_bytes(new_block)
    # new_block = inv_rot_bytes(new_block)
    # new_block = add_round_key(new_block, round_keys[0])
    decrypted_blocks.append(new_block)

# перевод блоков обратно в текст
data_dec = []
for block in decrypted_blocks:
    for i in range(len(block)):
        for j in range(len(block[i])):
            data_dec.append(block[i][j])

# запись в файл
with open("plaintext_after_decode.txt", "wb") as f:
    f.write(bytes(data_dec))
