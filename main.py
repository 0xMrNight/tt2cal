import os, json
from cal_generator import generate_ical_file

SEM_START = "2026-07-06"
SEM_END = "2026-11-03"

SLOTS_PATH = "data/slots.json"
CLEAN_TT = "data/tt_clean.csv"

ICS_OUT = "data/tt.ical"

def load_slots():
    if not os.path.exists(SLOTS_PATH):
        from generate_slots import generate
        print(f"{SLOTS_PATH} not found. Generating...")
        generate()
    
    with open(SLOTS_PATH, 'r') as f:
        return json.load(f)

def run():
    if not os.path.exists(CLEAN_TT):
        from cleaner import clean_csv
        clean_csv(out=CLEAN_TT)
    
    slots = load_slots()

    generate_ical_file(CLEAN_TT, slots, SEM_START, SEM_END, ICS_OUT)

if __name__ == "__main__":
    run()