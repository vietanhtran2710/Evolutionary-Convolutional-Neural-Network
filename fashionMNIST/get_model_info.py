LEARNING_RATE_DICT = {
    0: 1 * 10 ** (-5), 1: 5 * 10 ** (-5),
    2: 1 * 10 ** (-4), 3: 5 * 10 ** (-4),
    4: 1 * 10 ** (-3), 5: 5 * 10 ** (-3),
    6: 1 * 10 ** (-2), 7: 5 * 10 ** (-2),
}

DENSE_TYPE_DICT = {
    0: "recurrent", 1: "feed-forward"
}

REGULARIZATION_DICT = {
    0: "l1", 1: "l2", 2: "l1l2", 3: None
}

ACTIVATION_DICT = {
    0: "relu",
    1: "linear"
}

# GENE = [
#     '110110110001111100010001111011011111100110010110110100111110101011111', # 0 - 1
#     '110010111001100110010001111011011110001010010110110100111110101011111', # 2 - 2
#     '110110110001111100010001111011011111100011110110110000001110101011111', # 3 - 3
#     '110010110101100010011111111001011100101100011110110100111101101011111', # 4 - 4
#     '110010110001100011011111100100111111101000011110110000111110101011111', # 5 - 5
#     '110010111001100110010111110100110110001000011110100000111110101011111', # 6 - 6
#     '110010110101100110011111100111011111100100110110110000111100000011111', # 9 - 7
#     '110010111001100111110111110100110110100011110110111000001100000100110', # 11 - 8
#     '110010111001100111010111110100110110100011110110111000001100101011111', # 12 - 9
#     '110010110001100011011110110011011100101100011110110100111110101011111', # 13 - 10
# ]

GENE = [
    ['1100100010001101101110010100110111100001101011111101011100101101011', 0.8374000191688538],
    ['1100111111011000011100100001000110000100111011110111000101010100100', 0.8360000252723694],
    ['1001010001000111001100100001000110111001101011011111000101010101100', 0.8360000252723694],
    ['0000100010001101101110010100110101000001011101110001111110110111100', 0.8339999914169312],
    ['1100100010001100111101101001000110111000111001011111001001111111100', 0.833899974822998],
    ['1001000010000111001000110101111111010001110001111001111100100111011', 0.8324000239372253],
    ['0000011101000010001000011101110000010001011101110001001110111111100', 0.8317000269889832],
    ['1001010001000111001100100001000010000100111101101101000100110101100', 0.8309000134468079],
    ['1001010001000111001000110100111111111000111011111011110100100111100', 0.8307999968528748],
    ['1100101001100100100000011110000110111001111001011111001001101101100', 0.8307999968528748],

]

def binary_to_decimal(bits):
    return int("".join(map(str, bits)), 2)

def get_batch_size(gene):
    return [25, 50, 100, 15][binary_to_decimal(gene[:2])]

def get_convol_layers_num(gene):
    return 1 + binary_to_decimal(gene[2:4])

def get_kernels_num(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[4 + i * 10: 4 + i * 10 + 3]
        result.append(2 ** (binary_to_decimal(binary) + 1))
    return result

def get_kernel_sizes(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[7 + i * 10: 7 + i * 10 + 3]
        result.append(2 + binary_to_decimal(binary))
    return result

def get_pooling(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[10 + i * 10: 10 + i * 10 + 3]
        result.append(1 + binary_to_decimal(binary))
    return result

def get_convol_activation(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[13 + i * 10: 13 + i * 10 + 1]
        result.append(ACTIVATION_DICT[binary_to_decimal(binary)])
    return result

def get_dense_layers_num(gene):
    return 1 + binary_to_decimal([gene[44]])

def get_dense_type(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[45 + i * 8: 45 + i * 8 + 1]
        result.append(DENSE_TYPE_DICT[binary_to_decimal(binary)])
    return result

def get_neurons_num(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[46 + i * 8: 46 + i * 8 + 3]
        result.append(2 ** (binary_to_decimal(binary) + 3))
    return result

def get_dense_activation(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[49 + i * 8: 49 + i * 8 + 1]
        result.append(ACTIVATION_DICT[binary_to_decimal(binary)])
    return result

def get_regularization(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[50 + i * 8: 50 + i * 8 + 2]
        result.append(binary_to_decimal(binary))
    return result

def get_dropout(gene, layers_num):
    result = []
    for i in range(layers_num):
        binary = gene[52 + i * 8: 52 + i * 8 + 1]
        result.append(binary_to_decimal(binary) / 2)
    return result

def get_optimizer(gene):
    binary = gene[61: 64]
    return binary_to_decimal(binary)

def get_learning_rate(gene):
    binary = gene[64: 67]
    return LEARNING_RATE_DICT[binary_to_decimal(binary)]

def get_components(gene):
    dct = {}

    dct["b"] = get_batch_size(gene)

    # Convolutional layers
    dct["nc"] = get_convol_layers_num(gene)
    dct["ck"] = get_kernels_num(gene, dct["nc"])
    dct["cs"] = get_kernel_sizes(gene, dct["nc"])
    dct["cp"] = get_pooling(gene, dct["nc"])
    dct["ca"] = get_convol_activation(gene, dct["nc"])

    # Dense layers
    dct["nd"] = get_dense_layers_num(gene)
    dct["dt"] = get_dense_type(gene, dct["nd"])
    dct["dn"] = get_neurons_num(gene, dct["nd"])
    dct["da"] = get_dense_activation(gene, dct["nd"])
    dct["dd"] = get_dropout(gene, dct["nd"])
    dct["dr"] = get_regularization(gene, dct["nd"])

    # Learning parameters
    dct["n"] = get_learning_rate(gene)
    dct["f"] = get_optimizer(gene)

    return dct

s = set()
a = []
for index, gene in enumerate(GENE):
    des = ""
    dct = get_components(gene[0])
    for item in dct.values():
        des += str(item) + "-"
    if des not in s:
        print(gene, index)
        a.append(des)
        s.add(des)
print(len(a), len(s))
for item in a:
    print(item)