import os
import pandas as pd

DF = pd.read_csv(rf"{os.path.abspath('jobabot/static/csvs/charts.csv')}")

def get_data_chart1():
    df2 = DF[["대분류", "bq12_1", "bq12_2", "bq12_3", "bq12_4", "bq12_5"]]

    # 설문 답 중 9 => 해당사항 없음으로, 0점 처리
    for i in range(1, 6):
        df2.loc[df2.index[df2[f"bq12_{i}"] == 9], f"bq12_{i}"] = 0

    result = df2.groupby(df2['대분류'], as_index=False).mean()
    result["sum"] = result.sum(axis=1)
    sorted_result = result.sort_values(by=['sum'], ascending=False)
    return sorted_result

def get_data_chart2():
    df2 = DF[["job", "bq30_1"]]
    df2['bq30_1'] = pd.to_numeric(df2['bq30_1'], errors='coerce')
    result = df2.groupby(df2['job']).mean().sort_values(by=['bq30_1'], ascending=False).head(5).reset_index('job')

    return result

def get_data_chart3():
    df2 = DF[["대분류", "bq3"]]

    result = df2.groupby(df2['대분류'], as_index=False).mean()
    sorted_result = result.sort_values(by=['bq3'], ascending=False)

    return sorted_result

def get_data_chart4():
    df2 = DF[["job", "bq19"]]
    result = df2.groupby(df2['job']).mean().sort_values(by=['bq19'], ascending=False).head(5).reset_index('job')

    return result

def get_data_chart5():
    df = pd.read_csv(rf"{os.path.abspath('jobabot/static/csvs/chart5.csv')}", encoding="utf-8-sig")

    models = df.columns[2:5].tolist()
    xticks = df.iloc[:5,1].tolist()
    data = {"loss_people":df.iloc[:5,-3].tolist(),
            "loss_percent":df.iloc[:5,-2].tolist(),
    		"get_people":df.iloc[:5,-1].tolist(),
            "xticks": xticks,
            "models": models}
    return data