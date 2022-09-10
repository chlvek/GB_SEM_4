#4 -Реализуйте RLE алгоритм:
# реализуйте модуль сжатия и восстановления данных.Входные и выходные данные хранятся в отдельных текстовых файлах

def compress(data):
    '''RLE compress.'''

    compressed = ''
    current_count = 0
    current_symbol = data[0]
    for s in data:
        if s != current_symbol:
            if current_count > 1:
                compressed += f'{current_count}{current_symbol}'
            else:
                compressed += current_symbol
            current_symbol = s
            current_count = 1
        else:
            current_count += 1

    if current_count > 1:
        compressed += f'{current_count}{current_symbol}'
    else:
        compressed += current_symbol
    return compressed


if __name__ == "__main__":

    with open('original_file_path.txt', 'r') as file:
        data = file.read()

    print(f'Initial data:\n{data}')

    compressed = compress(data)

    print(f'Compressed data:\n{compressed}')

    with open('compressed_file_path.txt', 'w') as file:
        file.write(compressed)