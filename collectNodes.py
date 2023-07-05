import csv
import pandas as pd


def read_csv(filename, chunk_size):
    """
    This function will read data from csv, and this csv is pre-processed by panda, which filtered with constraints
    and only shows the columns "TIME", "NODES", "PACKET", "PACKET_30_MIN", and "ATTACKED". We also sort this data by
    'TIME', and this is implemented by Excel, instead of panda.
    :param filename: file name of data set to be processed
    :param chunk_size: node size
    :return: data: node packet, packet_30_min; attacked: which nodes are attacked
    """

    data = []
    attacked = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        chunk = []
        attacked_nodes = []
        next(reader)
        for i, row in enumerate(reader):

            chunk.append(row[3:-1])

            attacked_nodes.append(row[-1])
            if (i + 1) % chunk_size == 0:
                data.append(row[2])
                data.append(chunk)
                attacked.append(attacked_nodes)
                attacked_nodes = []
                chunk = []
    if chunk:
        data.append(chunk)
    # print(attacked)
    return data, attacked


def formatting(newFile):
    """
    This function write 50 nodes data in one row of csv file, as well as which nodes are under attack.
    :param newFile:
    """
    with open(newFile, 'w') as file:
        for i in range(0, int(len(data)/2)):
            dataString = ''
            for row in data[2*i+1]:
                dataString += ' '.join(row) + ';'
                # file.write(' '.join(row) + ';')
            # file.write(',')
            # for row in attacked[i]:
            for j in range(len(attacked[i])):
                file.write(data[2 * i] + " ;")
                file.write(dataString)
                file.write(' ' + str(j))
                file.write(',')
                file.write(attacked[i][j])
                file.write('\n')


def first(original, newFile, new_size):
    group_size = 50

    with open(original, 'r') as file:
        reader = csv.reader(file)
        # skip the first row
        rows = list(reader)

    # Extract the first 5 rows by group and build a new list of rows
    features = rows[0]
    new_rows = [features]
    for i in range(1, len(rows), group_size):
        group = rows[i:i + group_size]
        new_group = group[:new_size]
        new_rows.extend(new_group)

    # Write to new CSV file
    with open(newFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_rows)


def de_duplicate(newFile):
    df = pd.read_csv(newFile)
    df = df.drop_duplicates()
    df.to_csv(newFile, index=False)


if __name__ == '__main__':
    original_file = 'test_data/1.14_8h_0.5.csv'
    new_file = "test_data/test_1.14_8h_0.5_5.csv"
    node_size = 5
    first(original_file, new_file, node_size)
    data, attacked = read_csv(original_file, node_size)
    # format_file = "test_data/test_1.14_8h_0.5_1hour.csv"
    formatting(new_file)
    de_duplicate(new_file)
