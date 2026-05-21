import json
import sqlite3
import sys
import glob
from pathlib import Path

# get path to json
args = sys.argv[1:] 
if not args:
    print("Usage: py json2sql.py <file1>") # this will maybe be updated one day
    sys.exit(1)

# sql time
con = sqlite3.connect("trivia.db")
cur = con.cursor()

# mAke the table
cur.execute(""" 
CREATE TABLE IF NOT EXISTS trivia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    choices TEXT NOT NULL,
    UNIQUE(category, question)
)
""")

# CURRENTLY OVERWORKED AND REDUNDANT
files = []
for arg in args:
    matches = glob.glob(arg) or [arg]

    for m in matches: # i cbf making it take multiple files rn
        p = Path(m) # get arg as path (for TODO::iteration, but not rn)
        files.append(str(p))


JSONpath = []
if not files:
    print("Invalid input provided.")
    sys.exit(1)

# json import
data = None
for f in files:
    with open(f, "r", encoding="utf-8") as trivia_json:
        data = json.load(trivia_json)

counter = 0

# make some gd data, iterate that shit into the table
for category, questions in data.items():
    for q in questions:
        q["category"] = category # To ensure unique tag not triggered
        
        if not all(k in q for k in ("question", "answer", "choices")):
            print(f"\n!!! Skipping malformed question in category '{category}': {q}\n")
            counter+=1
            continue
    
        question = q["question"]
        answer = q["answer"]
        choices = json.dumps(q["choices"])  # store list as JSON text

        con.execute(
            "INSERT OR IGNORE INTO trivia (category, question, answer, choices) VALUES (?, ?, ?, ?)",
            (category, question, answer, choices)
        )

print("Total errors: ", counter)

# safety
con.commit()
con.close()