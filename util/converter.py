import sys
import glob
import json
import re
from pathlib import Path

## creates JSON from provided txt files
## txt file format:
#Q These are the opening lines of a song by The Rolling Stones, which first appeared as the opening track on the 1968 album, Beggars Banquet.  Guess the song.

# Please allow me to introduce myself
# Im a man of wealth and taste
# Ive been around for a long long year stolen many mans soul and faith
# I was around when Jesus Christ had His moment of doubt and pain
# ^ Sympathy for the Devil
# A Harlem Shuffle
# B Jumpin Jack Flash
# C Get off My Cloud
# D Sympathy for the Devil

#Q2 ....

## json file format
# todo

# get file(s) and convert to json
def parse_files(paths):
    triviaList = {}
    totalErrors = 0

    for p in paths: # f in files
        path = Path(p)
        if path.is_dir(): # sanity check
            continue

        category = path.stem
        triviaList.setdefault(category, [])

        # question cursor
        current = None

        with path.open(mode="r", encoding="ISO-8859-1", errors="replace") as f:
            id = 1 # format error checking
            for data in f: # data == line
                line = data.strip()

                # Start new question
                if line.startswith("#Q "):
                    if current:
                        triviaList[category].append(current)
                    current = {"question": line[3:], "choices": []}
                # Answer line
                elif line.startswith("^ "):
                    if current is not None:
                        current["answer"] = line[2:]
                # Choice line (e.g., "A option")
                elif re.match(r"^[A-Z] ", line):
                    if current is not None:
                        current["choices"].append(line[2:])
                elif not line: #  This ensures empty lines aren't always treated as EOquestion
                    if current and current.get("answer") is not None:
                        triviaList[category].append(current)
                        current = None
                        continue
                    else: # ignore incorrectly placed empty lines
                        print("bad format @ ", category," ", id)
                        totalErrors+=1
                        continue
                else: # includes "" intentionally for space issues
                    # Continuation of question text
                    if current is not None:
                        current["question"] += "\n" + line
                id+=1

        # At EOF, push last question
        if current:
            triviaList[category].append(current)

    print("total errors: ", totalErrors)
    return triviaList


# main
args = sys.argv[1:] 
if not args:
    print("Usage: py converter.py <file1> <file2> ... OR py converter.py folder/*")
    sys.exit(1)

# for globs
files = []
for arg in args:
    matches = glob.glob(arg) or [arg]

    for m in matches:
        p = Path(m) # get arg as path for iteration↓
        if p.is_dir():
            for child in p.iterdir(): # check each file in dir
                if child.is_file(): # if a file (assumedly a correct format)
                    files.append(str(child)) # add her to the list
        else: # just a file
            files.append(str(p))

formattedJSON = []
if not files:
    print("Invalid input provided.")
    sys.exit(1)

print("Will process: ")
for f in files:
    print("    ", f)
formattedJSON = parse_files(files)

export_path = Path("CategorisedQuestionList.json")
# export the new list
with export_path.open(mode="w", encoding="utf-8") as f:
    json.dump(formattedJSON, f, ensure_ascii=False, indent=2)

print(f"Trivia questions exported to {export_path} as a formatted JSON file")
