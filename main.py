import sqlite3

# データベース接続
conn = sqlite3.connect("school.db")
c = conn.cursor()

# --- テーブル定義 ---
c.execute('''
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    day TEXT NOT NULL,
    period TEXT NOT NULL,
    room TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(class_id) REFERENCES classes(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    item TEXT,
    weight INTEGER,
    FOREIGN KEY(class_id) REFERENCES classes(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    title TEXT,
    deadline TEXT,
    submitted INTEGER DEFAULT 0,
    FOREIGN KEY(class_id) REFERENCES classes(id)
)
''')
conn.commit()

# --- 授業登録 ---
def register_class():
    name = input("科目名: ")
    day = input("曜日: ")
    period = input("時限: ")
    room = input("教室: ")
    c.execute("INSERT INTO classes (name, day, period, room) VALUES (?, ?, ?, ?)", (name, day, period, room))
    conn.commit()
    print("授業を登録しました。")

# --- 時間割表示 ---
def show_timetable():
    print("--- 登録された時間割 ---")
    days_order = ['月', '火', '水', '木', '金']
    c.execute("SELECT * FROM classes")
    all_classes = c.fetchall()
    all_classes.sort(key=lambda x: (days_order.index(x[2]), int(x[3][0]) if x[3][0].isdigit() else 99))
    for cls in all_classes:
        print(f"{cls[2]} {cls[3]}限: {cls[1]}（{cls[4]}）")

# --- 出席登録 ---
def record_attendance():
    show_timetable()
    class_id = int(input("出席する授業IDを入力: "))
    date = input("日付 (例: 2025-06-19): ")
    status = input("出席状況（出席/欠席/遅刻）: ")
    c.execute("INSERT INTO attendance (class_id, date, status) VALUES (?, ?, ?)", (class_id, date, status))
    conn.commit()
    print("出席を記録しました。")

# --- 出席表示 ---
def show_attendance():
    c.execute('''
        SELECT classes.name, attendance.date, attendance.status
        FROM attendance
        JOIN classes ON attendance.class_id = classes.id
        ORDER BY attendance.date
    ''')
    records = c.fetchall()
    print("--- 出席記録一覧 ---")
    for r in records:
        print(f"{r[1]}: {r[0]} - {r[2]}")

# --- 評価登録 ---
def register_evaluation():
    show_timetable()
    class_id = int(input("評価を設定する授業IDを入力: "))
    item = input("評価項目（例: 試験、レポート）: ")
    weight = int(input("評価割合（%）: "))
    c.execute("INSERT INTO evaluations (class_id, item, weight) VALUES (?, ?, ?)", (class_id, item, weight))
    conn.commit()
    print("評価方法を登録しました。")

# --- 評価表示 ---
def show_evaluation():
    c.execute('''
        SELECT classes.name, evaluations.item, evaluations.weight
        FROM evaluations
        JOIN classes ON evaluations.class_id = classes.id
    ''')
    records = c.fetchall()
    print("--- 評価方法一覧 ---")
    for r in records:
        print(f"{r[0]}: {r[1]} {r[2]}%")

# --- 課題登録 ---
def register_assignment():
    show_timetable()
    class_id = int(input("課題を出す授業IDを入力: "))
    title = input("課題タイトル: ")
    deadline = input("締切日（例: 2025-07-01）: ")
    c.execute("INSERT INTO assignments (class_id, title, deadline) VALUES (?, ?, ?)", (class_id, title, deadline))
    conn.commit()
    print("課題を登録しました。")

# --- 課題表示 ---
def show_assignments():
    c.execute('''
        SELECT assignments.id, classes.name, assignments.title, assignments.deadline, assignments.submitted
        FROM assignments
        JOIN classes ON assignments.class_id = classes.id
    ''')
    records = c.fetchall()
    print("--- 課題一覧 ---")
    for r in records:
        status = "提出済" if r[4] else "未提出"
        print(f"[{r[0]}] {r[1]}: {r[2]}（締切: {r[3]}） - {status}")

# --- 課題提出状況更新 ---
def update_assignment():
    show_assignments()
    assignment_id = int(input("提出状況を変更する課題ID: "))
    c.execute("UPDATE assignments SET submitted = 1 WHERE id = ?", (assignment_id,))
    conn.commit()
    print("提出状況を更新しました。")

# --- メインループ ---
def main():
    while True:
        print("\n===== メニュー =====")
        print("1. 授業を登録する")
        print("2. 時間割を表示する")
        print("3. 出席を記録する")
        print("4. 出席記録を表示する")
        print("5. 評価方法を登録する")
        print("6. 評価方法を表示する")
        print("7. 課題を登録する")
        print("8. 課題一覧を表示する")
        print("9. 課題提出状況を更新する")
        print("0. 終了")

        choice = input("番号を選んでください: ")
        if choice == "1":
            register_class()
        elif choice == "2":
            show_timetable()
        elif choice == "3":
            record_attendance()
        elif choice == "4":
            show_attendance()
        elif choice == "5":
            register_evaluation()
        elif choice == "6":
            show_evaluation()
        elif choice == "7":
            register_assignment()
        elif choice == "8":
            show_assignments()
        elif choice == "9":
            update_assignment()
        elif choice == "0":
            print("終了します。")
            break
        else:
            print("無効な入力です。")

    conn.close()

if __name__ == "__main__":
    main()
