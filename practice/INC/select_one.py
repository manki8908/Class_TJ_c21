def select_item(table, name):

    # 상품명 조회
    n = 0
    while (True) :
        n += 1
        name = input("조회 이름 입력 : 끝내고 싶으면 엔터")
        if name == "" :
            break;
        print(f"===회원조회{n}===")
        sql = f"select * from tb1 where {table} like '%{name}%'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        if rows: 
            for row in rows:
                print(f"조회결과는 이름:{row[0]} 나이:{row[1]}, 수량:{row[2]} 입니다.")
        else:
            print("조회결과 입력한 이름에 맞는 회원이 었습니다.")