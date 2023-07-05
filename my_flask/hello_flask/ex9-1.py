from flask import Flask

# Flask 인스턴스 생성
# 초기화 입력 아규먼트로 현재 프로그램 명
#print(__name__) = "__main__"
app = Flask(__name__)

# 
# 데코레이터 기능을 사용하여, Flask의 route() 함수 호출
# route는 URI를 호출 했을때 실행되는 뷰 함수 정의
# "/" 는 URI의 루트 경로
@app.route('/')
def hello():
    return 'Hello Flask'


# ex9-1.py를 직접 실행했을 때 수행하는 내용 정의
if __name__ == '__main__':
    app.run()   # app.run(host='127.0.0.1', port='5000')
