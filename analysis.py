import os
import pandas as pd


def main():
    file_names = os.listdir("data/")
    dfs = []
    for file_name in file_names:
        df = pd.read_json(f"data/{file_name}", lines=True)
        dfs.append(df)
    
    df = pd.concat(dfs)
    print(df)
    print(df["category"].value_counts().sort_values(ascending=False).to_string())

if __name__ == '__main__':
    main()
