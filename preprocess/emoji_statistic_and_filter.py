import pandas as pd
import matplotlib.pyplot as plt
import re

file_path = 'preprocessed_data.csv'
df = pd.read_csv(file_path)
num = 40

# 提取所有表情符號
all_emojis = []
for text in df['Emoji']:
    if isinstance(text, str):  # 確保處理的是字串
        all_emojis.extend(list(text))

##find top 20

emoji_counts = pd.Series(all_emojis).value_counts()


top_20_emojis = emoji_counts.head(num)

## mapping 用的csv
emoji_df = pd.DataFrame({'Index': range(1, num+1), 'Emoji': top_20_emojis.index})
top_20_txt_file_path = '40_mapping_emojis.txt'
with open(top_20_txt_file_path, 'w', encoding='utf-8') as file:
    for index, row in emoji_df.iterrows():
        file.write(f"{row['Index']-1} {row['Emoji']}\n")

##畫圖top 20
# 創建包含前 20 个表情符號&count的 DataFrame
top_20_emojis_df = top_20_emojis.reset_index()
top_20_emojis_df.columns = ['Emoji', 'Count']
top_20_emojis_df['Index'] = range(0, num)


##top 20 count
# 總計數
total_count_top_20 = top_20_emojis_df['Count'].sum()

print("Top 20 Emojis with their Counts:")
print(top_20_emojis_df)
print("\nTotal Count of Top 20 Emojis:", total_count_top_20)

# 存成csv
top_20_counts_csv_file_path = 'top_40_emojis_with_counts.csv'
top_20_emojis_df.to_csv(top_20_counts_csv_file_path, index=False)
print(f"Top 20 emojis with their counts saved to {top_20_counts_csv_file_path}")

##刪除不用的data
# 獲取前20個項目
column_name = df.columns[1]
top_categories = df[column_name].value_counts().nlargest(num).index

# 過濾出只包含前 20 個類別資料，存成新的 CSV 
filtered_df = df[df[column_name].isin(top_categories)]
#filtered_csv_file_path = 'filtered_file.csv'
#filtered_df.to_csv(filtered_csv_file_path, index=False)
#print(f"Filtered CSV file saved to {filtered_csv_file_path}")

##processed data map to index
# 只保留CSV檔案中屬於這前20種資料的記錄
filtered_df = df[df[column_name].isin(top_20_emojis.index)]

# 將這些資料換成0到19
category_to_index = {category: i for i, category in enumerate(emoji_df['Emoji'])}
filtered_df.loc[:, column_name] = filtered_df[column_name].map(category_to_index)

filtered_df = filtered_df.rename(columns={column_name: 'Index'})

# 將結果存回CSV檔案
filtered_df.to_csv('40_mapped_data.csv', index=False)




