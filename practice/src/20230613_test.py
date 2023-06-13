# 모듈 로드
import pymysql
import sys
import os
print(pymysql.version_info) # 버전확인

import datetime
from datetime import datetime, date
from re import findall, match, sub


# db 연결 환경변수 설정
config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '0000',
    #'database' : 'work',
    'port' : 3306,
    'charset':'utf8',
    'use_unicode' : True}

class InputFilter :

    # studID = int(in_code)
    # name = input("name 입력 : ")
    # jumin1 = input("주민번호 앞자리(6자리) 입력 : ")
    # jumin2 = input("주민번호 뒷자리(7자리) 입력 : ")
    # addr1 = input("지번주소 입력 : ")
    # addr2 = input("도로명주소 입력 : ")


    def __init__(self):   
        self.inputValueFilter_result = False
        self.studID = ''
        self.name = ""
        self.jumin = ""
        self.addr1 = ""
        self.addr2 = ""

    def setID(self, studID) :

        if len(studID) != 8 :
            print("학번이 8자리 이상입니다.")
            self.inputValueFilter_result = False

        elif not(1900 <= int(studID[0:4]) <= 2023):
            print("학번이 년도 범위를 초과하였습니다.")
            self.inputValueFilter_result = False

        elif not( 1 <= int(studID[4:6]) <=99 ):
            print("학과코드가 잘못되었습니다.")
            self.inputValueFilter_result = False

        elif not( 1 <= int(studID[6:8]) <=99 ):
            print("학번순번이 잘못되었습니다.")
            self.inputValueFilter_result = False  

        else:
            self.inputValueFilter_result = True
            self.studID = studID
        return self.inputValueFilter_result


    def setJumin(self, jumin) :
    
                
        flag = {}
        if int(jumin[7]) == 1 or int(jumin[7]) == 2: year = int(jumin[0:2]) + 1900
        if int(jumin[7]) == 3 or int(jumin[7]) == 4: year = int(jumin[0:2]) + 2000
        #
        if year % 4 ==0 :
            if year % 100 == 0 :
                if year % 400 == 0:
                    year = '윤년'
                    month = [31,29,31,30,31,30,31,31,30,31,30,31]
                else:
                    year = '평년'
                    month = [31,28,31,30,31,30,31,31,30,31,30,31]
            else:
                year = '윤년'
                month = [31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            year = '평년'
            month = [31,28,31,30,31,30,31,31,30,31,30,31]

        #
        result = match('[0-9]{6}-[1-4][0-9]{6}', jumin)
        if len(jumin[0:]) > 14 :
            flag['flag1'] = '년도의 자리수 또는 뒷자리의 첫 숫자오류'
            flag1 = False
        else:
            flag['flag1'] = '*'
            flag1 = True
        #
        if 1 <= int(jumin[2:4]) <= 12 :  # 월의 숫자를 필터링
            flag['flag2'] = '*'
            flag2 = True
        else:
            flag['flag2'] = '앞자리의 월 오류'
            flag2 = False
        #
        if len(jumin[7:]) > 7 :
            flag['flag3'] = '뒷자리의 글자수 오류'
            flag3 = False
        else:
            flag['flag3'] = '*'
            flag3 = True
        #

        if 1 <= int(jumin[4:6]) <= month[(int(jumin[2:4]))-1] :  # 일의 숫자가 1 이상이면서 month 리스트의 해당 인덱스 요소의 숫자 이하인지 필터링
            flag['flag4'] = '*'
            flag4 = True
        else:
            flag4 = False
            flag['flag4'] = '앞자리중 월에 대한 일자 오류'
        #

        ###
        if result and flag1 and flag2 and flag3 and flag4 and flag4 :
            print('****주민번호 필터링 성공 ')
            self.inputValueFilter_result = True
            self.jumin = jumin
            
        else :
            print('잘못된 주민번호')
            print('flag[flag1] : ', flag['flag1'])
            print('flag[flag2] : ', flag['flag2'])
            print('flag[flag3] : ', flag['flag3'])
            print('flag[flag4] : ', flag['flag4'])
        
        return self.inputValueFilter_result
    

def userInput():
    ui1 = InputFilter()

    while True:
        if ui1.setID(input("학번을 입력하세요 : ")) :
            in_id = ui1.studID
            break
        else:
            continue

    in_name = input("name 입력 : ")
    
    while True:
        j1 = input("주민번호 앞자리를 입력하세요 : ")
        j2 = input("주민번호 뒷자리를 입력하세요 : ")
        if ui1.setJumin(j1+'-'+j2) :
            in_jumin1 = ui1.jumin[0:6]
            in_jumin2 = ui1.jumin[7:15]
            break
        else:
            continue


    in_addr1 = input("지번주소 입력 : ")
    in_addr2 = input("도로명주소 입력 : ")

    # studID = int(in_code)

    # jumin1 = input("주민번호 앞자리(6자리) 입력 : ")
    # jumin2 = input("주민번호 뒷자리(7자리) 입력 : ")



    return in_id, in_name, in_jumin1, in_jumin2, in_addr1, in_addr2




class CrudStud():

    # # 조회 품목 문자
    find_arg = None
    is_it_there = False

    # 생성자
    def __init__(self, config=config):
        self.config = config


# DB 및 테이블 서브루틴
    def create_table(self):

        try :

            # db 연동 객체 
            conn = pymysql.connect(**self.config)
            # sql문 실행 객체
            cursor = conn.cursor()

            # -------------- 초기화 
            # db가 없으면 생성
            sql = "create database if not exists work;"
            cursor.execute(sql)
            conn.commit() # db 반영

            sql = "show databases"
            cursor.execute(sql)
            dbs =   cursor.fetchall()
            print(dbs)
                    # table 유무 확인
            if dbs:
                print('DataBase 있음')
            else:
                print('DataBase 없음')

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영


            # 전체 table 목록 출력
            sql = "show tables"
            cursor.execute(sql)
            tables =    cursor.fetchall()
            print(tables)

            # table 유무 확인
            if tables:
                print('table 있음')
            else:
                print('table 없음')


            # -------------- table 생성 및 리스트 출력
            # 회원정보(이름, 나이, 회원번호)
            sql = """ create table if not exists stud(
                    studID varchar(8), 
	                name varchar(20), 
                    jumin1 varchar(6), 
                    jumin2 varchar(7),
                    addr1 varchar(20),
                    addr2 varchar(20)
                    )
                    """
            #print("111111111")
            cursor.execute(sql)
            #print("222222222")

            # -------------- 기존 입력값 조회
            sql = """ select * from stud;"""
            cursor.execute(sql)
            #print("111111111")
            rows =  cursor.fetchall()
            print("기존 학생리스트 = ", len(rows))
            for row in rows:
                print(row)

        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()


    # 상품 입력 서브루틴
    def insert_table(self):

        try :

            # db 연동 객체 
            conn = pymysql.connect(**self.config)

            # sql문 실행 객체
            cursor = conn.cursor()

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영

            # -------------- 기존 입력값 조회
            sql = """ select * from stud;"""
            cursor.execute(sql)
            #print("111111111")
            rows =  cursor.fetchall()
            print("기존 상품리스트 = ", len(rows))
            for row in rows:
                print(row)


            # -------------- 상품 정보 삽입
            while (True) :

                # 상품 입력
                in_code = input("학생 코드 입력 : (종료하고 싶으면 엔터)")
                #print("코드: ", in_code)
                if in_code == "" : break

                # 회원 이름 중복 조회
                print( " 학생 코드 중복 조회 ")
                sql = f"select * from stud where studID = {int(in_code)}"
                #print(sql)
                cursor.execute(sql)
                #print("33333")
                rows =  cursor.fetchall()

                #print("44444")

                if len(rows) > 0:
                    print('회원이 존재합니다, 다시입력하시거나 입력을 멈춥니다(엔터)')
                    #os.system("pause")  # 프로그램 멈춤
                    #os.system('cls')    # 터미널 출력 지우기
                    continue
                else:

                    # studID = int(in_code)
                    # name = input("name 입력 : ")
                    # jumin1 = input("주민번호 앞자리(6자리) 입력 : ")
                    # jumin2 = input("주민번호 뒷자리(7자리) 입력 : ")
                    # addr1 = input("지번주소 입력 : ")
                    # addr2 = input("도로명주소 입력 : ")

                    
                    iValue = userInput()

                    #print(code, name, su, dan)
                    #print(type(code), type(name), type(su), type(dan))
                    sql = f"INSERT INTO stud VALUES('{iValue[0]}', '{iValue[1]}', '{iValue[2]}', '{iValue[3]}', '{iValue[4]}', '{iValue[5]}')"
                    #print("22222")
                    cursor.execute(sql)
                    #print("3333")
                    conn.commit() # db 반영

                    print("===상품등록===")
                    print("코드 입력: ", iValue[0])
                    print("이름 입력: ", iValue[1])
                    print("주민번호 앞자리 입력: ", iValue[2])
                    print("주민번호 뒷자리 입력: ", iValue[3])            
                    print("지번 주소 입력 : ", iValue[4])
                    print("도로명 주소 입력 : ", iValue[5])
                    print("상품 등록을 성공했습니다.")

        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


    # 상품 전체목록 조회 서브루틴
    def select_all_record(self):

        try:

            # db 연동 객체 
            conn = pymysql.connect(**self.config)
            # sql문 실행 객체
            cursor = conn.cursor()

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영

            # 전체 레코드 조회
            sql = "select * from stud"
            cursor.execute(sql)
            rows =  cursor.fetchall()

            print(f"===학생 전체조회(검색된 레코드수: {len(rows)})===")
            names = [description[0] for description in  cursor.description]
            #print(names)
            for i in range(len(names)):
                if i is len(names)-1:
                    print(str(names[i]).ljust(15))
                else:
                    print(str(names[i]).ljust(15), end="\t")
                    #print(str(names[i]).ljust(15))

            for row in rows:
                for i in range(len(row)):
                    if i is len(row)-1:
                        print(str(row[i]).ljust(15))
                    else:
                        print(str(row[i]).ljust(15), end="\t")
                        #print(str(row[i]).ljust(15))

        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()


    # 단일 상품 조회(code or 상품명)
    def select_one_record(self):

        try:

            # db 연동 객체 
            conn = pymysql.connect(**self.config)
            # sql문 실행 객체
            cursor = conn.cursor()

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영

            # 전체 레코드 삽입
            sql = "select * from stud"
            cursor.execute(sql)
            rows =  cursor.fetchall()

            # -------------- 단일 상품 조회
            n = 0
            while (True) :
                n += 1

                farg = input("학생 조회(코드번호) : (조회를 끝내고 싶으면 엔터)   ")

                if farg == "" : 
                    break
                else:
                    self.find_arg = farg

                farg = int(farg)                    
                sql = f"select * from stud where studID = {farg}"
                

                print(f"===상품조회{n}===")
                cursor.execute(sql)
                rows =  cursor.fetchall()

                if rows: 
                    for row in rows:
                        #print(f"조회결과는 코드:{row[0]} 이름:{row[1]}, 수량:{row[2]}, 단가:{row[3]} 입니다.")
                        print(row)
                    self.is_it_there = True
                else:
                    print("조회결과 입력한 코드에 맞는 학생정보가 없습니다. 다시 입력해주세요")
                    self.is_it_there = False
      

        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

    def delete_record(self):

        try:

            # db 연동 객체 
            conn = pymysql.connect(**self.config)
            # sql문 실행 객체
            cursor = conn.cursor()

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영  

            n = 0
            while (True) :
                n += 1

                # 삭제를 위한 현재 레코드 리스트 출력
                self.select_all_record()  

                # 삭제 품목 조회
                self.select_one_record()

                #print("self.find_arg", self.find_arg)
                # 삭제 진행
                if self.is_it_there: 
                    print("삭제할 코드번호가 존재합니다, 삭제를 진행합니다.")   

                    # -------------- 단일 삭제 상품 조회 및 삭제
                    # .. 삭제                          

                    darg = self.find_arg.strip()
                    sql = f"delete from stud where studID like '%{darg}%'"

                    #print('11111111', sql)
                    cursor.execute(sql) # sql문 실행
                    #print("222222")
                    conn.commit()
                    #print("3333")

                    # 삭제후 레코드 리스트 출력
                    print("삭제에 성공하였습니다. 수정된 리스트를 다시 출력합니다.")
                    self.select_all_record()

                    break

                else: 
                    self.select_all_record()
                    in_code = input("삭제할 코드번호가 존재하지 않습니다, 다시 목록을 조회합니다 : (종료= 엔터, 다시진행=1)")
                    #print("코드: ", in_code)
                    if in_code == "" :  break


        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()


    # 수정기능 추가
    def update_record(self):

        try:

            # db 연동 객체 
            conn = pymysql.connect(**self.config)
            # sql문 실행 객체
            cursor = conn.cursor()

            sql = "use work;"
            cursor.execute(sql)
            conn.commit() # db 반영  

            n = 0
            while (True) :
                n += 1

                # 수정 위한 현재 레코드 리스트 출력
                self.select_all_record()  

                # 수정 품목 조회
                self.select_one_record()

                # 수정 진행
                if self.is_it_there: 
                    print("수정할 학생정보가 존재합니다, 수정 내용을 입력하세요.") 


                    iValue = userInput()

                    #print(code, name, su, dan)
                    #print(type(code), type(name), type(su), type(dan))
                    sql = f"update stud set name = '{iValue[1]}', jumin1 = '{iValue[2]}', jumin2 = '{iValue[3]}', addr1 = '{iValue[4]}', addr2 = '{iValue[5]}' where studID = {iValue[0]}"      
                    #sql = f"update goods set name = '{iValue[0]}' ,su = {iValue[1]} ,dan={iValue[2]} where code = {in_code}"
                    

                    # studID = input("학생 코드 입력 : ")
                    # name = input("name 입력 : ")
                    # jumin1 = input("주민번호 앞자리(6자리) 입력 : ")
                    # jumin2 = input("주민번호 뒷자리(7자리) 입력 : ")
                    # addr1 = input("지번주소 입력 : ")
                    # addr2 = input("도로명주소 입력 : ")

                    # # .. 수정                              
                    # sql = f"update goods set name='{name}', jumin1='{jumin1}', jumin2='{jumin2}', addr1='{addr1}', addr2='{addr2}' where code={studID}"

                    #print('11111111', sql)
                    cursor.execute(sql) # sql문 실행
                    #print("222222")
                    conn.commit()
                    #print("3333")

                    # 삭제후 레코드 리스트 출력
                    print("수정에 성공하였습니다. 수정된 리스트를 다시 출력합니다.")
                    self.select_all_record()

                    break

                else: 
                    self.select_all_record()
                    in_code = input("수정할 학생정보가 존재하지 않습니다, 다시 목록을 조회합니다 : (종료= 엔터, 다시진행=1)")
                    #print("코드: ", in_code)
                    if in_code == "" :  break


        except Exception as e:
            print("db 연동 error : ", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()



    def main(self):

        # DB 및 table 유무 조회 및 생성
        stud_table.create_table()

        while True:
            #os.system('cls')
            print("---상품관리---")
            print("학생    등록 : 1 ")
            print("학생목록조회 : 2 ")
            print("학생개별조회 : 3 ")
            print("학생    수정 : 4 ")
            print("학생    삭제 : 5 ")
            print("프로그램종료 : 9 ")
            sel = int(input("작업을 선택하세요 : "))
            if sel == 1 :
                stud_table.insert_table()
                os.system("pause")
            elif sel == 2 :
                stud_table.select_all_record()
                os.system("pause")
            elif sel == 3 :
                stud_table.select_one_record()
                os.system("pause")
            elif sel == 4 :
                stud_table.update_record()
                os.system("pause")
            elif sel == 5 :
                stud_table.delete_record()
                os.system("pause")
            elif sel == 9 :
                print("프로그램을 종료합니다")
                sys.exit(0) # 1=강제종료, 0=일반종료(에러포함)
            else :
                print("잘못 선택했습니다. ")
                os.system("pause")




if __name__ == '__main__':

    # 학생관리 클래스 객체 생성
    print(config)
    stud_table = CrudStud(config)

    stud_table.main()

    

    



