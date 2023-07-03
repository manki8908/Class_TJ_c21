#
# 챗봇에서 사용하는 사전 파일 생성
#
from tensorflow.keras import preprocessing
import pickle

import sys
sys.path.insert(0, '../../')
from utils.Preprocess import Preprocess

# 말뭉치 데이터 읽어오기, 데이터 그대로 3차원으로 가져옴
def read_corpus_data(filename):
    with open(filename, 'r', encoding='utf8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]
    return data

# CNN 절차 예)
# 1. 음절단위 분류  2. 토크나이저 핏 3. 토크나이저에서 시퀀스 추출  4. 3을 패딩
# 여기서는 토크나이저 핏만 함

# 말뭉치 데이터 가져오기
corpus_data = read_corpus_data('./corpus.txt')
#print(corpus_data[0:5])


# 망뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
#p = Preprocess(word2index_dic='chatbot_dict.bin',
#               userdic = '../../utils/user_dic.tsv')

p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c[1])   # 단어 분류
    for k in pos:
        dict.append(k[0])
    # keywords = p.get_keywords(pos, without_tag=True)
    # for k in keywords:
    #     dict.append(k)

#print(dict[0:50])

# 사전에 사용될 word2index 생성
# 사전의 첫번 째 인덱스에는 OOV 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index
print("word_index--------", word_index)

# 사전 파일 생성
f = open("chatbot_dict.bin", "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()
