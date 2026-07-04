# tt2cal - VIT Timetable to iCalendar Converter

This project parses a student timetable exported from VTOP and converts it into an `.ics` file, allowing you to easily import your class schedule into Google Calendar, Apple Calendar, or Microsoft Outlook.

## Prerequisites

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Setup and Data Extraction

Follow these steps to extract your timetable from VTOP:

1. Log in to **VTOP** and navigate to **Academics** > **Time Table**.
2. Choose the semester (e.g., Fall Semester 2026-27).
3. Select and copy the entire timetable grid (including headers like Sl.No, Class Group, Course, etc.).
4. Paste the data into Excel or a similar spreadsheet editor.
5. Save the file as a CSV named `tt_raw.csv` and place it inside the `data/` directory:
```text
data/tt_raw.csv
```

## Running the Script

Execute the main script:

```bash
python main.py
```

### Process Flow:

* The script cleans your `data/tt_raw.csv` file into a structured `data/tt_clean.csv`.
* It calculates accurate dates for each recurring classes based on the configured semester start and end dates.

## Output

Once the script completes successfully, the final calendar file will be generated at:

```text
data/tt.ical
```

You can import this `tt.ical` file directly into any standard calendar application to populate your weekly class schedule.