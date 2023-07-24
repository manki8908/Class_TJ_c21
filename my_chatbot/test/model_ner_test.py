import sys
sys.path.insert(0, "../")

from utils.Preprocess import Preprocess
from model.ner.NerModel import NerModel

#p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict3.bin',
#               userdic='../utils/user_dic1.tsv')
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict3.bin',
               userdic='../utils/mtn_user_dict.tsv')


ner = NerModel(model_name='../model/ner/ner_model2.h5', proprocess=p)


query = "오늘 오전 13시 2분에 싱싱회 주문 하고 싶어요" 
#query = "매봉산 산들길 찾아줘"
#query = "망운산 괴정동구간"
#query = "10시 30분"
query = "큰산임도 돈산리구간"
query = "배미산 봉덕리구간"
query = "배미산 삼성인력개발원등산로입구구간"

#query_list = [query1, query2, query3, query4, query5, query6]
query_list = [query]

for i in query_list:
    predicts = ner.predict(i)
    tags = ner.predict_tags(i)
    print(predicts)
    print(tags)

# sen = p.pos(query5)
# print(sen)ls