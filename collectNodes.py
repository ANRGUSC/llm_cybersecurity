import csv


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
        features = next(reader)
        for i, row in enumerate(reader):
            chunk.append(row[1:-1])
            if row[-1] == "1":
                attacked_nodes.append(row[1])
            if (i + 1) % chunk_size == 0:
                if len(attacked_nodes) == 0:
                    attacked_nodes.append('-')
                data.append(chunk)
                attacked.append(attacked_nodes)
                attacked_nodes = []
                chunk = []
    if chunk:
        data.append(chunk)
    print(attacked)
    return data, attacked


def formatting(newFile):
    """
    This function write 50 nodes data in one row of csv file, as well as which nodes are under attack.
    :param newFile:
    """
    with open(newFile, 'w') as file:
        for i in range(0, len(data)):
            for row in data[i]:
                file.write(' '.join(row) + ';')
            file.write(',')
            for row in attacked[i]:
                file.write(' ' + ''.join(row))
            file.write('\n')


# Read from data set, and save data of each 50 nodes in one time stamp in one list

original_file = 'train_data/1.4_8h.csv'
node_size = 50
data, attacked = read_csv(original_file, node_size)
new_file = "train_data/train_1.4_8h.csv"
formatting(new_file)
