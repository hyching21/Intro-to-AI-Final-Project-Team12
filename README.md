# NYCU AI Final Project Team12 
## Topic : Exploring Text-Emoji Correspondence
## Overview (including I/O)
In the rapidly evolving digital communication landscape, emojis have become an integral part of how we convey emotions, reactions, and context in text-based conversations. In our work, we intend to train a Chinese text-to-emoji prediction system and analyze different performance of our model using different numbers of classes and models.
## Prerequisite (environment, requirement.txt)
## Main Approach (including hyperparameters)
我們使用雙向長短期記憶網絡（BLSTM）來預測中文文本中的表情符號。BLSTM是一種先進的循環神經網絡（RNN），能夠在正向和反向兩個方向上處理輸入序列，從而捕捉到文本的上下文，這對於理解文本的語義非常重要。
以下是我們的訓練流程:
### 1. Data Preprocessing
#### a. Preprocessing
##### remove user names
Example :
Input : @jaychou 蘋果肉桂waffle一份竟然$204！
Output : 蘋果肉桂waffle一份竟然$204！
##### cut the words
使用jieba的繁體字典庫dict.txt.big，進行繁體中文分詞及處理。
##### remove stopwords & punctuations
標點符號和停用詞（例如「的」、「了」、「在」 等）在文本分析中通常是無用的，因此需要被移除。我們可以從一個預先定義的停用詞檔案stopwords.txt中讀取停用詞。
##### remove non-chinese words
Example :
Input : 蘋果肉桂waffle一份竟然$204！
Output : 蘋果肉桂一份竟然$204！
#### b. Over-sampling Data
由於每個emoji的數據量不相符，我們利用RandomOverSampler解決數據不平衡問題，這樣可以確保模型在訓練過程中不會偏向數據量較多的表情符號。
#### c. Tokenize
利用tokenizer將dataset中的單詞以詞頻排序後編號，再將每個文本都轉化成以編號表示的序列。這樣的處理可以使模型更有效地理解文本中的詞語。
#### d. Padding
為了確保每個文本的長度一致，我們對文本進行填充或截斷，使所有文本的長度相同。
### 2. Model Architecture
#### a. 嵌入層
將input轉換為固定大小的密集向量。這些向量可以捕捉詞語之間的語義關係，為後續的BLSTM層提供有效的特徵表示。
#### b. BLSTM層
利用兩個BLSTM層捕捉上下文。
#### c. 全連接層
將BLSTM輸出映射到所需的輸出大小，即表情符號的機率分布。其中activation function為Softmax，確保輸出的機率總合為1，以便最終的表情符號預測。
### 3. Training Process
#### a. Loss function
利用Categorical Cross-Entropy來測量預測準確性。
#### b. Optimizer
利用Adam optimizer進行高效的梯度下降。Adam是一種自適應學習率的優化方法，能夠在訓練過程中自動調整學習率，從而加快收斂速度和提高模型性能。
#### c. Batch Training
利用batch training優化權重，其中batch size為64、epoch為15，並使用early stopping。
### 4. Prediction
#### a. Preprocessing
如1.所述，對新輸入的文本進行處理。
#### b. Model Inference
將已預處理的input文本傳入BLSTM模型。
#### c. Output
從Softmax輸出中選擇一率最高的emoji。
### 5. UI
我們利用flask開發了一個網站，串接上述的模型，使用者可以輸入一段文字，網站將以換行做為每句話的分隔，為每句話加入適當的表情符號。
## Results
### 1. 翻譯Baseline的dataset，測試中文是否能成功
我們先採用baseline所使用的twiter datasets，取3000筆進行train，並利用google sheet的”=GOOGLETRANSLATE(A2,"en","zh-TW")“ 函式將原先英文的資料翻譯成中文。
#### LSTM 訓練結果，accuracy為0.9252
#### BLSTM 訓練結果，accuracy為0.9357
#### 20種emojis的數據（precision, recall, f1-score, and total accuracy）
#### 手動輸入一些測資，跑出的對應表情符號也確實有正確符合語意。
### 2. 初步爬蟲測試 (發現太多留言重複會影響結果，像是綠色愛心、台灣加油)
經過翻譯樣本測試後，我們確定中文版本是可執行的。而我們發現翻譯的樣本常會有翻譯錯誤的現象，不符合中文語法，且對應的20種emoji也並不符合我們想要的真實數據，因此我們決定選用更貼近中文使用表情符號狀況的Instagram貼文及留言當作dataset。
利用python套件"instaloader”進行爬蟲，將該帳號前10篇貼文的內容與留言全部擷取。結果可以達到約7成的accuracy，但我們發現選取全部留言的dataset，會使得有太多重複的內容，例如"台灣加油"配上綠色愛心，而這會影響到最終的預測結果。
### 3. 第一次採用的dataset (某些帳號的資料筆數較多，像是賴清德、周杰倫)
根據上面的測試確定爬蟲及其擷取的資料有一定的可行性。我們接著蒐集更多樣化的Instagram帳號資料，並且限制了每次爬取貼文的留言數量，避免過多重複資料。
#### LSTM，accuracy為0.7028
#### BLSTM，accuracy為0.7263
#### 每個emoji各自的precision、recall和f1-score

經過訓練後，我們發現BLSTM會有較高的accuracy，因此在最後版本我們以BLSTM的方法去訓練model。
但我們發現，因為部分帳號經過篩選是否有emoji的資料後，所保留的資料集數較多，導致我們訓練資料的來源會不平均，因此最終我們改以在爬蟲時就篩選出包含emoji的資料，讓每個帳號的資料數量是固定一樣的。
### 4. 最後採用的dataset
最後的dataset是固定每個帳號所爬到含有emoji的資料數量。我們分別篩選出前20、30及40個常用的emoji的那些數據資料，並訓練了能夠predict出20、30和40的emoji的model。
#### a. top 20 emojis
##### 訓練結果，accuracy為0.8039
##### 每個emoji各自的precision、recall和f1-score
#### b. top 30 emojis
##### 訓練結果，accuracy為0.8322
##### 每個emoji各自的precision、recall和f1-score
#### c. top 40 emojis
##### 訓練結果，accuracy為0.8438
##### 每個emoji各自的precision、recall和f1-score

