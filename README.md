# NYCU AI Final Project Team12 
In the rapidly evolving digital communication landscape, emojis have become an integral part of how we convey emotions, reactions, and context in text-based conversations. In our work, we intend to train a Chinese text-to-emoji prediction system and analyze different performance of our model using different numbers of classes and models.
## Topic : Exploring Text-Emoji Correspondence
## Overview (including I/O)
## Prerequisite (environment, requirement.txt)
## Main Approach (including hyperparameters)
我們使用雙向長短期記憶網絡（BLSTM）來預測中文文本中的表情符號。BLSTM是一種先進的循環神經網絡（RNN），能夠在正向和反向兩個方向上處理輸入序列，從而捕捉到文本的上下文，這對於理解文本的語義非常重要。
以下是我們的訓練流程:
### 1. Data Preprocessing
#### remove user names
Example :
Input : @jaychou 蘋果肉桂waffle一份竟然$204！
Output : 蘋果肉桂waffle一份竟然$204！
#### cut the words
使用jieba的繁體字典庫dict.txt.big，進行繁體中文分詞及處理。
#### remove stopwords & punctuations
標點符號和停用詞（例如「的」、「了」、「在」 等）在文本分析中通常是無用的，因此需要被移除。我們可以從一個預先定義的停用詞檔案stopwords.txt中讀取停用詞。
#### remove non-chinese words
Example :
Input : 蘋果肉桂waffle一份竟然$204！
Output : 蘋果肉桂一份竟然$204！
## Results
