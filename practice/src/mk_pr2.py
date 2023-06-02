# mysql 소스코드 
import pymysql
import sys
import os

print(pymysql.version_info) # 버전확인


# db 연결 환경변수 설정
config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '0000',
    'database' : 'work',
    'port' : 3306,
    'charset':'utf8',
    'use_unicode' : True}


# 회원정보 삽입 서브루틴
def member_create():

    try :

        # -------------- 초기화 
        # db 연동 객체 
        conn = pymysql.connect(**config)
        # sql문 실행 객체
        cursor = conn.cursor()

        # 전체 table 목록 출력
        sql = "show tables"
        cursor.execute(sql)
        tables = cursor.fetchall()
        print(tables)

        # table 유무 확인
        if tables:
            print('table 있음')
        else:
            print('table 없음')


        # -------------- 회원 table 생성 ( tb1 )
        # 회원정보(이름, 나이, 회원번호)
        sql = """ create table if not exists tb1(
        name varchar(20),
        age int,
        num int
        );"""
        cursor.execute(sql)

        # -------------- 기존 입력값 조회
        sql = """ select * from tb1;"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("기존 회원명수 = ", len(rows))
        for row in rows:
            print(row)
        

        # -------------- 회원 정보 삽입
        while (True) :
            # 한번 입력사이클 후 종료하고 싶으면 엔터
            name = input("회원 이름 입력 : (종료하고 싶으면 엔터)")
            #print("이름: ", name)

            if name == "" : break

            # 회원 이름 중복 조회
            #print( " 회원 이름 중복 조회 ")
            sql = f"select * from tb1 where name = '{name}'"
            #print(sql)
            cursor.execute(sql)
            #print("33333")
            rows = cursor.fetchall()

            #print("44444")

            if len(rows) > 0:
                print('회원이 존재합니다, 다시입력하시거나 입력을 멈춥니다(엔터)')
                #os.system("pause")  # 프로그램 멈춤
                #os.system('cls')    # 터미널 출력 지우기
                continue
            else:
                #name = input("이름 입력 : ")
                age = int(input("나이 입력 : "))
                num = int(input("수량 입력 : "))
                #print(name, age, num)
                #print(type(code), type(name), type(su), type(dan))
                sql = f"INSERT INTO tb1 VALUES('{name}', {age}, {num})"
                #print("22222")
                cursor.execute(sql)
                #print("3333")
                conn.commit() # db 반영
                #print("4444")

                print("===상품등록===")
                print("이름 입력: ", name)
                print("나이 입력: ", age)
                print("수량 입력: ", num)
                print("회원등록을 성공했습니다.")

    except Exception as e:
        print("db 연동 error : ", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
            
        
def select_total_record():

    try:
        
        conn = pymysql.connect(**config)
        # sql문 실행 객체
        cursor = conn.cursor()

        # 전체 레코드 조회
        sql = "select * from tb1"
        cursor.execute(sql)
        rows = cursor.fetchall()

        print("===회원 전체조회===")
        names = [description[0] for description in cursor.description]
        #print(names)
        for i in range(len(names)):
            if i is len(names)-1:
                print(names[i])
            else:
                print(names[i], end="\t")

        for row in rows:
            for i in range(len(row)):
                if i is len(row)-1:
                    print(row[i])
                else:
                    print(row[i], end="\t")

    except Exception as e:
        print("db 연동 error : ", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def select_one_record():

    try:
        
        conn = pymysql.connect(**config)
        # sql문 실행 객체
        cursor = conn.cursor()

        # 전체 레코드 조회
        sql = "select * from tb1"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # -------------- 단일 상품 조회
        n = 0
        while (True) :
            n += 1
            name = input("조회 이름 입력 : 끝내고 싶으면 엔터")
            if name == "" : break

            print(f"===회원조회{n}===")
            sql = f"select * from tb1 where name like '%{name}%'"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows: 
                for row in rows:
                    print(f"조회결과는 이름:{row[0]} 나이:{row[1]}, 수량:{row[2]} 입니다.")
            else:
                print("조회결과 입력한 이름에 맞는 회원이 었습니다.")


    except Exception as e:
        print("db 연동 error : ", e)
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()


def main():
    while True:
        os.system('cls')
        print("---회원관리---")
        print("회원    등록 : 1 ")
        print("회원목록조회 : 2 ")
        print("회원개별조회 : 3 ")
        print("회원    수정 : 4 ")
        print("회원    삭제 : 5 ")
        sel = int(input("작업을 선택하세요 : "))
        if sel == 1 :
            member_create()
            os.system("pause")
        elif sel == 2 :
            select_total_record()
            os.system("pause")
        elif sel == 3 :
            select_one_record()
            os.system("pause")
        elif sel == 4 :
            print("회원수정기능은 준비중입니다. ")
            os.system("pause")
        elif sel == 5 :
            print("회원삭제기능은 준비중입니다. ")
            os.system("pause")
        else :
            print("잘못 선택했습니다. ")
            os.system("pause")


if __name__ == '__main__':

    main()