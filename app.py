import lib


def main():
    lib.create_table()  # 確保資料庫和資料表已建立

    while True:
        print("\n----- 電影管理系統 -----")
        print("1. 匯入電影資料檔")
        print("2. 查詢電影")
        print("3. 新增電影")
        print("4. 修改電影")
        print("5. 刪除電影")
        print("6. 匯出電影")
        print("7. 離開系統")
        print("------------------------")
        option = input("請選擇操作選項 (1-7): ")

        if option == '1':
            lib.import_movies()
        elif option == '2':
            lib.search_movies()
        elif option == '3':
            lib.add_movie()
        elif option == '4':
            lib.modify_movie()
        elif option == '5':
            lib.delete_movies()
        elif option == '6':
            lib.export_movies()
        elif option == '7':
            print("系統已退出。")
            break
        else:
            print("無效選項，請重新選擇。")

if __name__ == '__main__':
    main()