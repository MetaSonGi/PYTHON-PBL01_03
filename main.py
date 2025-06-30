# main.py

def read_inventory_file(filename):
    """
    Reads the inventory CSV file and prints its contents.

    :param filename: str - CSV file path
    :return: list of lists
    """
    inventory_data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
            inventory_data.append(header)
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == len(header):
                    inventory_data.append(parts)
    except FileNotFoundError:
        print('Error: File not found.')
    except IOError:
        print('Error: Could not read the file.')

    return inventory_data

def safe_float(value):
    """
    Converts value to float, returns 0.0 if conversion fails.
    """
    try:
        return float(value)
    except ValueError:
        return 0.0

def sort_by_flammability(data):
    """
    Sorts the inventory list by flammability index in descending order.

    :param data: list of lists
    :return: sorted list of lists
    """
    header = data[0]
    rows = data[1:]

    sorted_rows = sorted(
        rows,
        key=lambda x: safe_float(x[2]),
        reverse=True
    )
    return [header] + sorted_rows


def filter_dangerous_materials(data, threshold=0.7):
    """
    Filters materials with flammability index >= threshold.

    :param data: list of lists
    :param threshold: float
    :return: list of lists
    """
    header = data[0]
    rows = data[1:]

    filtered = [row for row in rows if safe_float(row[2]) >= threshold]

    return [header] + filtered


def save_to_csv(data, filename):
    """
    Saves list of lists to a CSV file.

    :param data: list of lists
    :param filename: str - output CSV file path
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for row in data:
                line = ','.join(row)
                file.write(line + '\n')
        print(f'File saved: {filename}')
    except IOError:
        print('Error: Could not write to the file.')


def print_table(data):
    """
    Prints the list of lists in a table-like format.

    :param data: list of lists
    """
    for row in data:
        print('\t'.join(row))


def main():
    inventory_file = r'C:\Users\52649\Documents\GitHub\python_codyseey\Step01\01\PYTHON-PBL01_03\Mars_Base_Inventory_List.csv'
    danger_file = r'C:\Users\52649\Documents\GitHub\python_codyseey\Step01\01\PYTHON-PBL01_03\Mars_Base_Inventory_danger.csv'

    # CSV 읽기
    data = read_inventory_file(inventory_file)

    if not data:
        print('No data found in the file.')
        return

    print('=== Original Inventory ===')
    print_table(data)

    # 인화성 지수 기준 정렬
    sorted_data = sort_by_flammability(data)
    print('\n=== Sorted Inventory (by flammability) ===')
    print_table(sorted_data)

    # 인화성 지수 0.7 이상 추출
    dangerous_data = filter_dangerous_materials(sorted_data, threshold=0.7)
    print('\n=== Dangerous Materials (flammability >= 0.7) ===')
    print_table(dangerous_data)

    # CSV 저장
    save_to_csv(dangerous_data, danger_file)


if __name__ == '__main__':
    main()
