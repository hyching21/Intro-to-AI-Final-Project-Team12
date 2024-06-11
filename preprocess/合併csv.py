from google.colab import drive
drive.mount('/content/drive')

import os
import glob
import pandas as pd

shared_folder_path = '/content/drive/My Drive/AI_final/crawl_output' 

if not os.path.exists(shared_folder_path):
    raise ValueError(f"資料夾路徑不存在: {shared_folder_path}")

csv_files = glob.glob(os.path.join(shared_folder_path, '*.csv'))

if not csv_files:
    raise ValueError("在指定的資料夾中未找到任何 CSV 文件")

df_list = [pd.read_csv(file) for file in csv_files]

combined_df = pd.concat(df_list, ignore_index=True)

print(combined_df.head())

output_path = '/content/drive/My Drive/AI_final/combined_data.csv'
combined_df.to_csv(output_path, index=False)
print(f"合併後的 CSV 已保存至: {output_path}")