import sys
sys.path.insert(0,'../')
from utils.Preprocess import Preprocess
from model.intent.IntentModel import IntentModel


p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
#               userdic='../utils/user_dic.tsv')
                userdic='../utils/mtn_user_dict.tsv')

intent = IntentModel(model_name='../model/intent/intent_model.h5', proprocess=p)
#query = "오늘 탕수육 주문 가능한가요?"
#query = "도덕봉 옥곤리구간"
#query = "9시 30분"
query = "1"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)

