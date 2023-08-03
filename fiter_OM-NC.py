import pandas as pd
import random

def filter():
    # 加载Parquet文件到DataFrame
    path = "validation_data/validation_data.parquet"
    df = pd.read_parquet(path)
    start_date = '2021/1/10'
    end_date = '2021/1/11'
    # 根据条件过滤数据
    grouped = df.groupby(df["ATTACK_PARAMETER"])
    Ks = [0, 0.1, 0.3, 0.5, 0.7, 1]
    for k in Ks:
        df_filtered = df[
            (df["ATTACK_PARAMETER"] > k - 0.001) & (df["ATTACK_PARAMETER"] < k + 0.001)
            & (df["TIME"] >= start_date) & (df["TIME"] < end_date)
            & (df["ATTACK_DURATION"] == 28800)
            & (df["ATTACK_RATIO"] == 0.5)
            ]

        # 定义一个函数，用于将多列数据合并成一个字符串，用空格分隔
        def combine_columns(row):
            def format_value(val):
                return int(val) if val == 0.0 else val

            return " ".join([str(format_value(row[col])) for col in
                             ['NODE', 'PACKET', 'PACKET_30_MIN', 'PACKET_1_HOUR', 'PACKET_2_HOUR', 'PACKET_4_HOUR']])

        # 创建一个新的DataFrame，其中包含合并后的字符串和"ATTACKED"列的数据
        result_df = pd.DataFrame({
            "prompt": df_filtered.apply(combine_columns, axis=1),
            "completion": df_filtered["ATTACKED"].apply(int)
        })
        type = path.split("_")[0]
        result_df.to_csv(type + str(k) + ".csv", index=False)


def choose(type:str):
    parameters = [0, 0.1, 0.3, 0.5, 0.7, 1]
    for k in parameters:
        path = type + str(k) + '_prepared.jsonl'
        new_path = type + str(k) + '.jsonl'
        with open(path, 'r') as f:
            lines = f.readlines()
        randomlines = random.sample(lines, 500)

        with open(new_path, 'w') as file:
            file.writelines(randomlines)


if __name__ == '__main__':
    types = ['test']
    for type in types:
        choose(type)
# # 将每个"ATTACK_PARAMETER"分组保存为单独的CSV文件
# grouped = result_df.groupby(df_filtered["ATTACK_PARAMETER"])
# print(grouped)
# for group_name, group_data in grouped:
#     print(group_name)
#     group_data.to_csv(f"output_file_{group_name}.csv", index=False)