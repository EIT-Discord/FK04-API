import pdfplumber
import camelot
import pandas as pd
import re
import os

final_df = pd.DataFrame(columns = ["Tag", "Anfang", "Ende", "Fach", "Gruppe", 
                                   "Raum", "Profesor", "Studiengruppe", 
                                   "Semestervorstand", "Vorlesungsperiode"])

def cidToChar(cidx):
    return chr(int(re.findall(r'\(cid\:(\d+)\)',cidx)[0]) + 29)

def char(xx):
    output = ""
    for x in xx.split('\n'):
        if x != "" and x != "(cid:3)":
            cids = re.findall(r'\(cid\:\d+\)', x)
            for cid in cids:
                x = x.replace(cid, cidToChar(cid))
            output = output + "\n" + x
    return output

def pdf_to_dataframe(file_path):
    
    table = pd.DataFrame(columns = ["Tag", "Anfang", "Ende", "Fach", "Gruppe", 
                                   "Raum", "Profesor", "Studiengruppe", 
                                   "Semestervorstand", "Vorlesungsperiode"])

    with pdfplumber.open(f"{file_path}") as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    text = char(text)

    group = re.findall(r'Studiengruppe:\s+([a-zA-Z0-9_]+)', text)[0]
    decan = re.findall(r'Semestervorstand:\s+([a-zA-Z0-9_]+)', text)[0]
    time = re.findall(r'Vorlesungsperiode\s+([a-zA-Z0-9_]+)', text)[0]

    tables = camelot.read_pdf(file_path, line_scale = 30, copy_text=['v'])

    df = tables[0].df
    df = df.applymap(char)


    # cleaning data
    for index in range(1, len(df.columns)):
        col_data = df[index].tolist()
        _flag = 0 
        for i, data in enumerate(col_data):
            if i == 0 or data == "":
                continue
            if i == len(col_data) - 1:
                i = i-2

            if data == col_data[i + 1]: # check to see if cell needs correction
                continue

            if _flag == 1: # check if previous cell was changed 
                col_data[i] = col_data[i - 1]
                _flag = 0
                continue

            items = data.split("\n")
            next_items = col_data[i + 1].split("\n") # if cell was not identified correctly, then concat currentcell with next
            if  next_items != [""] and len(items) < 5: # if cell data is too small to be an entry concate next one
                col_data[i] = col_data[i] + col_data[i + 1]
                _flag = 1
        df[index] = col_data

    days = df.iloc[0]
    cols = []
    days[0] = "Zeiten"
    for i, day in enumerate(days):
        if day != "":
            cols.append(day.strip())
        else:
            cols.append(cols[i-1])
    df.iloc[0] = cols
    for index in range(1, len(df.columns)):

        day_df = df[[0, index]]
        times = day_df[0]
        subjects = day_df[index].tolist()
        subjects = [x for x in subjects if str(x) != 'nan']
        day = subjects[0]
        subjects = set(subjects[1:])

        for i, s in enumerate(subjects):
            if i == 0:
                continue
            df_subject = day_df.loc[day_df[index] == s]
            data = dict()

            first_line = df_subject.iloc[0]
            last_line = df_subject.iloc[-1]

            times = first_line[0].split("\n")
            items = first_line[index].split("\n")

            data["Studiengruppe"] = group
            data["Semestervorstand"] = decan
            data["Vorlesungsperiode"] = time

            data["Gruppe"] = items[1]
            data["Profesor"] = items[2]
            data["Fach"] = items[3]
            data["Raum"] = items[4]

            data["Tag"] = day
            data["Anfang"] = times[2]
            data["Ende"] = last_line[0].split("\n")[3]
            
            table = table.append(data, ignore_index=True)
            
    return table
        
path_of_the_directory = 'C:/Users/Hakan/OneDrive/005_Notebooks/Stundenplankonvertierer'
ext = ('.pdf')
for files in os.listdir(path_of_the_directory):
    if files.endswith(ext):
        final_df = final_df.append(pdf_to_dataframe(files), ignore_index=True)
