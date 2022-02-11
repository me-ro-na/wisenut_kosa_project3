import pandas as pd

def get_jobs():
    df = pd.read_csv('datasets/seaborn-data/titanic.csv')
    df2 = df.copy()
    df2.drop([''])

    df.drop(['deck', 'embarked', 'embark_town'], axis=1, inplace=True)
    dic = dict()
    return dic