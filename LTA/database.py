import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE t_message (id int, m_name text, m_text text, m_keyword)"

cursor.execute(create_table)

messages = [
    (1, 'BookOfPython', 'According to the March 1, 2015 run of the HTTP Archive, the average web page is now over 2 megabytes (2008 kb, to be precise). Bloated websites lead to slow load times, frustrated users and wasted energy. Mightybytes has identified four key areas where sustainability principles can be applied to the process of creating websites that are speedy, user-friendly and energy-efficient.', 'zero'),
    (2,'LearnToCodeInDays','JavaScript (JS) is a lightweight, interpreted, or just-in-time compiled programming language with first-class functions. While it is most well-known as the scripting language for Web pages, many non-browser environments also use it, such as Node.js, Apache CouchDB and Adobe Acrobat.','zero'),
    (3,'NoProbLem', 'Recursion is the process which comes into existence when a function calls a copy of itself to work on a smaller problem. Any function which calls itself is called recursive function, and such function calls are called recursive calls.','zero'),
    
]

insert_query = "INSERT INTO t_message VALUES (?, ?, ?, ?)"

cursor.executemany(insert_query, messages)

connection.commit()

connection.close()

