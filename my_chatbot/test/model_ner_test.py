import sys
sys.path.insert(0, "../")

from utils.Preprocess import Preprocess
from model.ner.NerModel import NerModel

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict3.bin',
               userdic='../utils/user_dic1.tsv')


ner = NerModel(model_name='../model/ner/ner_model2.h5', proprocess=p)


#query = '오늘 오전 13시 2분에 탕수육 주문 하고 싶어요'
query1 = "오늘 오전 13시 2분에 탕수육 주문 하고 싶어요"
query2 = "오늘 오전 13시 2분에 우라늄회 주문 하고 싶어요"
query3 = "오늘 오전 13시 2분에 우럭회 주문 하고 싶어요"
query4 = "오늘 오전 13시 2분에 짜장면 주문 하고 싶어요"
query5 = "오늘 오전 13시 2분에 우라회 주문 하고 싶어요"
query6 = "오늘 오전 13시 2분에 촐랭이밥 주문 하고 싶어요" 

query = "오늘 오전 13시 2분에 싱싱회 주문 하고 싶어요" 

#query_list = [query1, query2, query3, query4, query5, query6]
query_list = [query]

for i in query_list:
    predicts = ner.predict(i)
    tags = ner.predict_tags(i)
    print(predicts)
    print(tags)

# sen = p.pos(query5)
# print(sen)