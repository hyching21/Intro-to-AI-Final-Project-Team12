# NYCU AI Final Project Team12 
In the rapidly evolving digital communication landscape, emojis have become an integral part of how we convey emotions, reactions, and context in text-based conversations. In our work, we intend to train a Chinese text-to-emoji prediction system and analyze different performance of our model using different numbers of classes and models.
## Topic : Exploring Text-Emoji Correspondence
## Overview (including I/O)
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
