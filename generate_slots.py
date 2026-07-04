import json

TIMINGS = [
    # Morning 
    {"theory": ("08:00", "08:50"), "lab": ("08:00", "08:50")}, 
    {"theory": ("08:55", "09:45"), "lab": ("08:50", "09:40")}, 
    {"theory": ("09:50", "10:40"), "lab": ("09:50", "10:40")}, 
    {"theory": ("10:45", "11:35"), "lab": ("10:40", "11:30")}, 
    {"theory": ("11:40", "12:30"), "lab": ("11:40", "12:30")}, 
    {"theory": ("12:35", "13:25"), "lab": ("12:30", "13:20")}, 
    # Afternoon
    {"theory": ("14:00", "14:50"), "lab": ("14:00", "14:50")}, 
    {"theory": ("14:55", "15:45"), "lab": ("14:50", "15:40")}, 
    {"theory": ("15:50", "16:40"), "lab": ("15:50", "16:40")}, 
    {"theory": ("16:45", "17:35"), "lab": ("16:40", "17:30")}, 
    {"theory": ("17:40", "18:30"), "lab": ("17:40", "18:30")}, 
    {"theory": ("18:35", "19:25"), "lab": ("18:30", "19:20")}  
]

GRID = {
    "MO": [
        "A1/L1", "F1/L2", "D1/L3", "TB1/L4", "TG1/L5", "S11/L6",
        "A2/L31", "F2/L32", "D2/L33", "TB2/L34", "TG2/L35", "S3/L36"
    ],
    "TU": [
        "B1/L7", "G1/L8", "E1/L9", "TC1/L10", "TAA1/L11", "L12",
        "B2/L37", "G2/L38", "E2/L39", "TC2/L40", "TAA2/L41", "S1/L42"
    ],
    "WE": [
        "C1/L13", "A1/L14", "F1/L15", "TD1/L16", "TBB1/L17", "L18",
        "C2/L43", "A2/L44", "F2/L45", "TD2/L46", "TBB2/L47", "S4/L48"
    ],
    "TH": [
        "D1/L19", "B1/L20", "G1/L21", "TE1/L22", "TCC1/L23", "L24",
        "D2/L49", "B2/L50", "G2/L51", "TE2/L52", "TCC2/L53", "S2/L54"
    ],
    "FR": [
        "E1/L25", "C1/L26", "TA1/L27", "TF1/L28", "TDD1/L29", "S15/L30",
        "E2/L55", "C2/L56", "TA2/L57", "TF2/L58", "TDD2/L59", "L60"
    ]
}

def generate():
    slots_json = {}
    
    for day, slots in GRID.items():
        for col_idx, slot_string in enumerate(slots):
            timing = TIMINGS[col_idx]
            
            parts = [p.strip() for p in slot_string.split('/')]
            
            for part in parts:
                if part.startswith('L'):
                    start, end = timing['lab']
                else:
                    start, end = timing['theory']
                
                if part not in slots_json:
                    slots_json[part] = []

                slots_json[part].append({
                    "day": day,
                    "start": start,
                    "end": end
                })
                
    with open('data/slots.json', 'w') as f:
        json.dump(slots_json, f, indent=2)
        
    print("Successfully generated data/slots.json!")

if __name__ == "__main__":
    generate()