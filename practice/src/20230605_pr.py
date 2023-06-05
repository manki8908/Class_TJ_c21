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
    #'database' : 'work',
    'port' : 3306,
    'charset':'utf8',
    'use_unicode' : True}


# 회원정보 삽입 서브루틴
def create_goods():

    try :

        # db 연동 객체 
        conn = pymysql.connect(**config)

        # sql문 실행 객체
        cursor = conn.cursor()

        # -------------- 초기화 
        # db가 없으면 생성
        sql = "create database if not exists test_db;"
        cursor.execute(sql)
        conn.commit() # db 반영

        sql = "show databases"
        cursor.execute(sql)
        dbs = cursor.fetchall()
        print(dbs)
                # table 유무 확인
        if dbs:
            print('DataBase 있음')
        else:
            print('DataBase 없음')

        sql = "use test_db;"
        cursor.execute(sql)
        conn.commit() # db 반영


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
        sql = """ create table if not exists goods(
        code integer primary key,
        name varchar(30) not null,
        su integer  default 0,
        dan real default 0.0
        )"""
        #print("111111111")
        cursor.execute(sql)
        #print("222222222")

        # -------------- 기존 입력값 조회
        sql = """ select * from goods;"""
        cursor.execute(sql)
        #print("111111111")
        rows = cursor.fetchall()
        print("기존 상품리스트 = ", len(rows))
        for row in rows:
            print(row)
        

        # -------------- 상품 정보 삽입
        while (True) :

            # 상품 입력
            in_code = input("상품 코드 입력 : (종료하고 싶으면 엔터)")
            #print("코드: ", in_code)
            if in_code == "" : break

            # 회원 이름 중복 조회
            print( " 상품 코드 중복 조회 ")
            sql = f"select * from goods where code = {int(in_code)}"
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

                code = int(in_code)
                name = input("name 입력 : ")
                su = int(input("su 입력 : "))
                dan = float(input("dan 입력 : "))
                #print(code, name, su, dan)
                #print(type(code), type(name), type(su), type(dan))
                sql = f"INSERT INTO goods VALUES({code}, '{name}', {su}, {dan})"
                #print("22222")
                cursor.execute(sql)
                #print("3333")
                conn.commit() # db 반영

                print("===상품등록===")
                print("코드 입력: ", code)
                print("이름 입력: ", name)
                print("수량 입력: ", su)
                print("단가 입력: ", dan)            
                print("상품 등록을 성공했습니다.")

    except Exception as e:
        print("db 연동 error : ", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
            
        
def select_total_record():

    try:

        # db 연동 객체 
        conn = pymysql.connect(**config)
        # sql문 실행 객체
        cursor = conn.cursor()

        sql = "use test_db;"
        cursor.execute(sql)
        conn.commit() # db 반영
        
        # 전체 레코드 조회
        sql = "select * from goods"
        cursor.execute(sql)
        rows = cursor.fetchall()

        print("===상품 전체조회===")
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

        # db 연동 객체 
        conn = pymysql.connect(**config)
        # sql문 실행 객체
        cursor = conn.cursor()

        sql = "use test_db;"
        cursor.execute(sql)
        conn.commit() # db 반영
        
        # 전체 레코드 조회
        sql = "select * from goods"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # -------------- 단일 상품 조회
        n = 0
        while (True) :
            n += 1
            name = input("조회 이름 입력 : 끝내고 싶으면 엔터")
            if name == "" : break

            print(f"===상품조회{n}===")
            sql = f"select * from goods where name like '%{name}%'"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows: 
                for row in rows:
                    print(f"조회결과는 코드:{row[0]} 이름:{row[1]}, 수량:{row[2]}, 단가:{row[3]} 입니다.")
            else:
                print("조회결과 입력한 이름에 맞는 상품이 었습니다.")


    except Exception as e:
        print("db 연동 error : ", e)
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()


def main():
    while True:
        #os.system('cls')
        print("---상품관리---")
        print("상품    등록 : 1 ")
        print("상품목록조회 : 2 ")
        print("상품개별조회 : 3 ")
        print("상품    수정 : 4 ")
        print("상품    삭제 : 5 ")
        sel = int(input("작업을 선택하세요 : "))
        if sel == 1 :
            create_goods()
            os.system("pause")
        elif sel == 2 :
            select_total_record()
            os.system("pause")
        elif sel == 3 :
            select_one_record()
            os.system("pause")
        elif sel == 4 :
            print("상품 수정기능은 준비중입니다. ")
            os.system("pause")
        elif sel == 5 :
            print("상품 삭제기능은 준비중입니다. ")
            os.system("pause")
        else :
            print("잘못 선택했습니다. ")
            os.system("pause")


if __name__ == '__main__':

    main()