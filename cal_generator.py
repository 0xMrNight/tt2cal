import pandas as pd
from datetime import datetime
from icalendar import Calendar, Event, vRecur

def first_occurrence(day: str, st: str, end: str, sst: str) -> tuple[datetime, datetime]:
    """Calculates dtstart and dtend for the first occurrence of a slot"""
    weekday_map = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    target_day = weekday_map[day]

    start = datetime.strptime(sst, "%Y-%m-%d")

    days_ahead = (target_day - start.weekday()) % 7
    target_date = start + pd.Timedelta(days=days_ahead)
    
    start_h, start_m = map(int, st.split(":"))
    end_h, end_m = map(int, end.split(":"))
    
    dtstart = target_date.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
    dtend = target_date.replace(hour=end_h, minute=end_m, second=0, microsecond=0)

    return dtstart, dtend

def generate_ical_file(csv_path: str, slots_data: dict, sem_start: str, sem_end: str, output_path: str):
    """Parses the cleaned timetable dataframe and exports it to an .ics file"""
    df = pd.read_csv(csv_path)

    cal = Calendar()
    cal.add('prodid', '-//VIT Timetable Converter//EN')
    cal.add('version', '2.0')
    
    until_datetime = datetime.strptime(sem_end, "%Y-%m-%d")

    for _, row in df.iterrows():
        # all slots as list
        curr_slots = str(row['Slot']).split('+') if pd.notna(row['Slot']) else []

        for slot_code in curr_slots:
            if slot_code not in slots_data:
                continue
            
            for session in slots_data[slot_code]:
                dt_start, dt_end = first_occurrence(session["day"], session["start"], session["end"], sst=sem_start)
                
                event = Event()
                event.add('summary', row['Course_Title'])
                event.add('location', row['Venue'] if pd.notna(row['Venue']) else "")
                event.add('description', f"{slot_code} {row['Faculty']} | {row['Course_Code']}")

                event.add('dtstart', dt_start)
                event.add('dtend', dt_end)

                # Set weekly recurrence rule until the end of the semester
                event.add('rrule', vRecur({
                    'FREQ': 'WEEKLY',
                    'UNTIL': until_datetime
                }))

                cal.add_component(event)

    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"iCalendar file generated at: '{output_path}'")