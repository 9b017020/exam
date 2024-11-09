import os
import json
import sqlite3



# 定義資料庫和檔案路徑常數
DB_PATH = 'movies.db'
JSON_IN_PATH = 'movies.json'
JSON_OUT_PATH = 'exported.json'


def connect_db() -> sqlite3.Connection:
    """
    連接到資料庫，如果資料庫不存在會自動建立
    :return: sqlite3.Connection 物件
    """
    return sqlite3.connect(DB_PATH)


def list_rpt() -> None:
    """
    列出資料庫中的所有電影
    """
    try:
        with connect_db() as conn:
            conn.row_factory = sqlite3.Row  # 使查詢結果以字典形式回傳
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            movies = cursor.fetchall()

            if movies:
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':<15}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}{'評分':{chr(12288)}<10}")
                print("-" * 50)
                for movie in movies:
                    print(f"{movie['title']:{chr(12288)}<10}{movie['director']:<15}{movie['genre']:{chr(12288)}<10}{movie['year']:{chr(12288)}<10}{movie['rating']:{chr(12288)}<10}")
            else:
                print("資料庫中沒有電影資料")
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生其它錯誤: {e}')


def create_table() -> None:
    """
    建立資料表，若資料表不存在
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                director TEXT NOT NULL,
                                genre TEXT NOT NULL,
                                year INTEGER NOT NULL,
                                rating REAL NOT NULL CHECK(rating >= 1.0 AND rating <= 10.0)
                            )''')
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生其它錯誤: {e}')


def import_movies() -> None:
    """
    匯入電影資料檔案
    """
    try:
        if not os.path.exists(JSON_IN_PATH):
            print("找不到電影資料檔案！")
            return

        with open(JSON_IN_PATH, 'r', encoding='utf-8') as file:
            try:
                movies = json.load(file)
            except json.JSONDecodeError:
                print("JSON 檔案格式錯誤！")
                return

        with connect_db() as conn:
            cursor = conn.cursor()
            for movie in movies:
                try:
                    cursor.execute('''INSERT INTO movies (title, director, genre, year, rating)
                                      VALUES (?, ?, ?, ?, ?)''',
                                   (movie['title'], movie['director'], movie['genre'], movie['year'], movie['rating']))
                except sqlite3.IntegrityError:
                    print(f"電影 {movie['title']} 已經存在！")
            conn.commit()

        print("電影資料匯入完成！")
    except Exception as e:
        print(f'發生錯誤: {e}')


def search_movies() -> None:
    """
    查詢電影資料
    """
    try:
        with connect_db() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = input("查詢全部電影嗎？(y/n): ")
            if query.lower() == 'y':
                cursor.execute("SELECT * FROM movies")
                movies = cursor.fetchall()
            else:
                title = input("請輸入電影名稱: ")
                cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f'%{title}%',))
                movies = cursor.fetchall()

            if movies:
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}{'評分':{chr(12288)}<10}")
                print("-" * 85)
                for movie in movies:
                    print(f"{movie['title']:{chr(12288)}<10}{movie['director']:<12}{movie['genre']:{chr(12288)}<10}{movie['year']:{chr(12288)}<10}{movie['rating']:{chr(12288)}<10}")
            else:
                print("查無資料")
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生錯誤: {e}')


def add_movie() -> None:
    """
    新增電影資料
    """
    try:
        title = input("電影名稱: ")
        director = input("導演: ")
        genre = input("類型: ")
        year_str = input("上映年份: ")
        rating_str = input("評分 (1.0 - 10.0): ")

        # 檢查年份和評分的合法性
        if not year_str.isdigit():
            print("年份格式錯誤，應為數字！")
            return
        year = int(year_str)

        if not (1.0 <= float(rating_str) <= 10.0):
            print("評分格式錯誤，應為 1.0 到 10.0 之間的數字！")
            return
        rating = float(rating_str)

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO movies (title, director, genre, year, rating)
                              VALUES (?, ?, ?, ?, ?)''',
                           (title, director, genre, year, rating))
            conn.commit()

        print("電影已新增")
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生錯誤: {e}')


def modify_movie() -> None:
    """
    修改電影資料
    """
    try:
        title = input("請輸入要修改的電影名稱: ")

        with connect_db() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
            movie = cursor.fetchone()

            if movie:
                # 顯示電影的當前資料
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}{'評分':{chr(12288)}<10}")
                print("-" * 85)

                # 動態根據資料類型選擇格式化方式
                print(f"{movie['title']:{chr(12288)}<10} {movie['director']:<12} {movie['genre']:{chr(12288)}<10} "
                      f"{str(movie['year']).center(5, chr(12288))} {str(movie['rating']).center(12, chr(12288))}")

                # 請使用者輸入新的電影資料
                new_title = input(f"請輸入新的電影名稱 (若不修改請直接按 Enter): ")
                new_director = input(f"請輸入新的導演 (若不修改請直接按 Enter): ")
                new_genre = input(f"請輸入新的類型 (若不修改請直接按 Enter): ")
                new_year = input(f"請輸入新的上映年份 (若不修改請直接按 Enter): ")
                new_rating = input(f"請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ")

                # 若使用者沒有輸入新值，則保留原值
                new_title = new_title if new_title else movie['title']
                new_director = new_director if new_director else movie['director']
                new_genre = new_genre if new_genre else movie['genre']
                new_year = int(new_year) if new_year else movie['year']
                new_rating = float(new_rating) if new_rating else movie['rating']


                # 更新資料庫中的電影資料
                cursor.execute('''UPDATE movies SET title = ?, director = ?, genre = ?, year = ?, rating = ?
                                  WHERE id = ?''',
                               (new_title, new_director, new_genre, new_year, new_rating, movie['id']))
                conn.commit()

                print("資料已修改")
            else:
                print("電影未找到")
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生錯誤: {e}')

def delete_movies() -> None:
    """
    刪除電影資料
    """
    try:
        query = input("刪除全部電影嗎？(y/n): ")

        with connect_db() as conn:
            conn.row_factory = sqlite3.Row  # 確保結果是字典形式
            cursor = conn.cursor()

            if query.lower() == 'y':
                cursor.execute("DELETE FROM movies")
                conn.commit()
                print("所有電影資料已刪除")
            else:
                title = input("請輸入要刪除的電影名稱: ")
                cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f'%{title}%',))
                movie = cursor.fetchone()

                if movie:
                    # 確認返回的資料是字典
                    if isinstance(movie, sqlite3.Row):
                        # 顯示電影資料
                        print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<10}{'評分':{chr(12288)}<10}")
                        print("-" * 85)
                        print(f"{movie['title']:{chr(12288)}<10}{movie['director']:<15}{movie['genre']:{chr(12288)}<10}{movie['year']:{chr(12288)}<12}{movie['rating']:{chr(12288)}<10}")

                    else:
                        print("返回的資料不是字典格式")
                        return

                    confirmation = input(f"是否要刪除電影 {movie['title']}? (y/n): ")
                    if confirmation.lower() == 'y':
                        cursor.execute("DELETE FROM movies WHERE id = ?", (movie['id'],))
                        conn.commit()
                        print("電影已刪除")
                    else:
                        print("未刪除")
                else:
                    print("未找到匹配的電影")

    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生錯誤: {e}')



def export_movies() -> None:
    """
    匯出電影資料至 JSON 檔案，若使用者選擇匯出特定電影則根據名稱過濾
    """
    try:
        export_all = input("匯出全部電影嗎？(y/n): ")

        if export_all.lower() == 'y':
            # 匯出所有電影
            query = "SELECT * FROM movies"
        else:
            # 匯出特定電影
            title = input("請輸入要匯出的電影名稱: ")
            query = "SELECT * FROM movies WHERE title = ?"

        with connect_db() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (title,) if title else ())
            movies = cursor.fetchall()

            if not movies:
                print("未找到指定的電影資料。")
                return

            movie_list = []
            for movie in movies:
                movie_list.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'director': movie['director'],
                    'genre': movie['genre'],
                    'year': movie['year'],
                    'rating': movie['rating']
                })

        with open(JSON_OUT_PATH, 'w', encoding='utf-8') as file:
            json.dump(movie_list, file, ensure_ascii=False, indent=4)

        print(f"電影資料已匯出至 {JSON_OUT_PATH}")

    except Exception as e:
        print(f'發生錯誤: {e}')

