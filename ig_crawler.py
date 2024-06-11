import instaloader
import emoji
import csv

# 建立 Instaloader 物件
L = instaloader.Instaloader()

username = '' # 登入IG帳戶
password = '' # 登入IG帳戶
target_user = '' # 設定目標用戶

data_limit = 10 # 設定資料數量上限
comment_limit = 20 # 設定每篇貼文的留言數量上限

L.login(username, password)
profile = instaloader.Profile.from_username(L.context, target_user)

# 計數器
data_count = 0
comment_count = 0

csv_data = []

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:

    for post in profile.get_posts():
        
        emoji_sentences = [line.strip() for line in post.caption.splitlines() if any(emoji.is_emoji(char) for char in line)]
        
        for sentence in emoji_sentences:
            text = ''.join(char for char in sentence if not emoji.is_emoji(char))
            # 每行的不同表情符號
            emojis = list(set(char for char in sentence if emoji.is_emoji(char)))
            # 表情符號的種類數
            emoji_count = len(emojis)
            # 把每個表情符號和對應的文本一起存入 CSV 
            for emoji_char in emojis:
                csv_data.append([text, emoji_char])
                data_count += 1
                if data_count >= data_limit:
                    break

            if data_count >= data_limit:
                break
        
        if data_count >= data_limit:
            break
            
        emoji_sentences = [line.strip() for comment in post.get_comments() for line in comment.text.splitlines() if any(emoji.is_emoji(char) for char in line)]

        comment_count = 0
        for sentence in emoji_sentences:
            text = ''.join(char for char in sentence if not emoji.is_emoji(char))
            # 每行的不同表情符號
            emojis = list(set(char for char in sentence if emoji.is_emoji(char)))
            # 表情符號的種類數
            emoji_count = len(emojis)
            # 把每個表情符號和對應的文本一起存入 CSV 
            for emoji_char in emojis:
                csv_data.append([text, emoji_char])
                data_count += 1
                if data_count >= data_limit or comment_count >= comment_limit:
                    break

            if data_count >= data_limit or comment_count >= comment_limit:
                break
            
        if data_count >= data_limit:
            break
    
    writer = csv.writer(csvfile)
    # 寫入標題
    writer.writerow(['Text', 'Emoji'])
    # 寫入數據
    writer.writerows(csv_data)

# 顯示前十筆
print("前十筆資料：")
for row in csv_data[:10]:
    print(row)
