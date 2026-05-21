import sqlite3
import json

con = sqlite3.connect("trivia.db")
cur = con.cursor()

# Count total questions
cur.execute("SELECT COUNT(*) FROM trivia")
total = cur.fetchone()[0]
print(f"Total questions: {total}")

# whole table
# cur.execute("""
#     SELECT category, question, answer, choices
#     FROM trivia""")

# change above to following to make random single question show
cur.execute("""
    SELECT category, question, answer, choices
    FROM trivia
    ORDER BY RANDOM()
    LIMIT 1;""")

rows = cur.fetchall()

for id, row in enumerate(rows, 1):
    category, question, answer, choices_json = row
    try:
        choices = json.loads(choices_json)
    except json.JSONDecodeError:
        print("ERROR AT ID: " + id, start="\n")

    print(f"Question {id}:", end=" ")
    print(f"Category: {category}")
    print(f"{question}", end=" ")
    for i, choice in enumerate(choices, 1):
        print(f"  {chr(64+i)}. {choice}", end=" ")
    print(f"Answer: {answer}")

con.close()
