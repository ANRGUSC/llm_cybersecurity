import pandas as pd


def filterData(filePath, startDate, endDate):
    df = pd.read_parquet(filePath)
    print(df.columns)
    duration = 28800
    parameter = [0, 0.5, 1]
    attack_ratio = 0.5
    # filter data by constraints
    filter_df = df[
        (df['TIME'] >= startDate) & (df['TIME'] < endDate) & (df['ATTACK_DURATION'] == duration) &
        df['ATTACK_PARAMETER'].isin(parameter) & (df['ATTACK_RATIO'] == attack_ratio)]
    # sorted by time
    columns_to_includes = ['TIME', 'NODE', 'PACKET', 'ATTACKED', 'PACKET_30_MIN']
    filter_df[columns_to_includes].to_csv("./train_data/1.4_8h.csv", index=False)


if __name__ == '__main__':
    PATH = "./train_data/train_data.parquet"
    start_date = '2021/1/4'
    end_date = '2021/1/5'

    filterData(PATH, start_date, end_date)

# selected_df = filter_df[columns_to_includes]
# selected_df.reindex(columns=['TIME', 'NODE', 'PACKET', 'PACKET_30_MIN', 'ATTACKED']).to_csv("./train_data/1.4_8h.csv", index=False)

# df.to_csv('./validation_data/validation_data.csv', index=False)
