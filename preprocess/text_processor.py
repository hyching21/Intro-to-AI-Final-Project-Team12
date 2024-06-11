import jieba
import re
import pandas as pd

# 1. remove user names
def remove_name(text):
    if not isinstance(text, str):
        return ''
    name=re.compile(r'@\S+\s*')
    return name.sub(r'',text)

# 2. cut the words
jieba.set_dictionary('dict.txt.big.txt')
def cut_word(text):
    words = list(jieba.cut(text))
    return words

# 3. remove stopwords & punctuations
def get_stopwords(file):
    stopword_list = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            stopword_list.append(line)
    return stopword_list

def remove_stopwords(sentence, stopwords):
    return [word for word in sentence if word not in stopwords and word.strip()]

# 4. remove non-chinese words
def keep_chinese_list(text_list):
    cleaned_text_list = []
    for text in text_list:
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)  # 匹配中文字符
        cleaned_text = ''.join(chinese_text)
        if cleaned_text:  # 檢查字是否是空的
            cleaned_text_list.append(cleaned_text)
    return cleaned_text_list


stopwords = get_stopwords('stopwords.txt')
def text_processing(text):
    text = remove_name(text)
    text = cut_word(text) 
    text = remove_stopwords(text, stopwords)
    processed_text = keep_chinese_list(text)
    return processed_text

df = pd.read_csv('combined_data.csv')
df['Text'] = df['Text'].apply(text_processing)
df = df[df['Text'].apply(lambda x: len(x) > 0)]
df.to_csv('preprocessed_data.csv', index=False)