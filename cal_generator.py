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
        slots_raw = str(row['Slot'])
        slots = slots_raw.split('+') if slots_raw else []

        # group sessions per day
        sessions_day = {} 

        for slot_code in slots:
            if slot_code not in slots_data:
                print(f"Warning: Skipping unknown slot '{slot_code}'")
                continue
            
            for session in slots_data[slot_code]:
                day = session['day']
                if day not in sessions_day:
                    sessions_day[day] = []

                sessions_day[day].append({
                    'slot_code': slot_code,
                    'start': session['start'],
                    'end': session['end']
                })
                
        for day, session in sessions_day.items():
            st_times = [s['start'] for s in session]
            end_times = [s['end'] for s in session]

            if not st_times or not end_times:
                continue

            abs_start = min(st_times)
            abs_end = max(end_times)
            
            day_slot_code = "+".join([s['slot_code'] for s in session]) 

            dt_start, dt_end = first_occurrence(day, abs_start, abs_end, sst=sem_start)
            
            event = Event()
            event.add('summary', row['Course_Title'])
            event.add('location', row['Venue'] if pd.notna(row['Venue']) else "")
            event.add('description', f"{day_slot_code} {row['Faculty']} | {row['Course_Code']}")

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