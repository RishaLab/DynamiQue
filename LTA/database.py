import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE t_messages (id int, m_name text, m_text text, m_keyword)"

cursor.execute(create_table)

messages = [
    (1, 'face', 'This is a trail comment section ping me @dheeraj', 'recursion'),
    (2,'tweet','This is not a drill, evacuate', 'sorting'),
    (3,'insta', 'like my picture spam spam spam','algorithm')
]

insert_query = "INSERT INTO t_messages VALUES (?, ?, ?, ?)"

cursor.executemany(insert_query, messages)

connection.commit()

connection.close()

