import pandas as pd

def clean_csv(raw="data/tt_raw.csv", out="data/tt_clean.csv"):
    df = pd.read_csv(raw)

    metadata_cols = [
        "Sl.No",
        "Class Id",
        "Faculty Details",
        "L T P J C",
    ]
    df[metadata_cols] = df[metadata_cols].ffill()

    # clean string columns before aggregation 
    df["Course"] = df["Course"].fillna("").str.strip()
    df["Slot/ Venue"] = df["Slot/ Venue"].fillna("").str.strip().str.replace(r"\s*-\s*$", "", regex=True)
    df["Faculty Details"] = df["Faculty Details"].str.replace(r"\s*-\s*$", "", regex=True).str.strip()

    # collapse the multi-row blocks using groupby and custom aggregation
    df_clean = df.groupby("Class Id", as_index=False).agg({
        "Sl.No": "first",
        "Faculty Details": "first",
        "L T P J C": "first",
        "Course": lambda x: " ".join([i for i in x if i]),
        "Slot/ Venue": lambda x: {
            "Slot": next((i for i in x if "+" in i or (i and not any(char.isdigit() for char in i.split('-')[0]))), None) or next((i for i in x if i), ""),
            "Venue": next((i for i in x if any(char.isdigit() for char in i) and "+" not in i), "")
        }
    })

    # expand slot/venue column
    slots_venues = pd.DataFrame(df_clean["Slot/ Venue"].tolist())
    df_clean[["Slot", "Venue"]] = slots_venues[["Slot", "Venue"]]

    # remove any whitespaces in venue
    df_clean["Venue"] = df_clean["Venue"].str.replace(r"\s+", "", regex=True)

    # extract Course Code, Title, and Type 
    regex_pattern = r"(?P<Course_Code>[A-Z0-9]+)\s*-\s*(?P<Course_Title>.*?)\s*\(\s*(?P<Course_Type>.*?)\s*\)"
    df_clean[["Course_Code", "Course_Title", "Course_Type"]] = df_clean["Course"].str.extract(regex_pattern)

    # convert credits to integer
    df_clean["L T P J C"] = df_clean["L T P J C"].apply(lambda x: x.split()[-1]).astype(float).astype(int)

    df_clean = df_clean.rename(columns={
        "L T P J C": "Credits",
        "Class Id": "Class_ID",
        "Faculty Details": "Faculty"
    })

    final_cols = [
        "Class_ID",
        "Course_Code",
        "Course_Title",
        "Course_Type",
        "Credits",
        "Slot",
        "Venue",
        "Faculty"
    ]

    df_clean = df_clean[final_cols]

    df_clean.to_csv(out, index=False)

    print("Timetable cleaned successfully")
    print(df_clean)

if __name__ == "__main__":
    clean_csv()