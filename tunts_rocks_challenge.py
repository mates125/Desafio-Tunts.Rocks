import pandas as pd
import numpy as np
import gspread 
from url_convertion import convert_google_sheet_url
import math

#readind the dataframe
url = 'https://docs.google.com/spreadsheets/d/1qgPQ_uiRrkDv4eF_oBzOB0WhxlH8OlTC9ygGsdbmXVc/edit#gid=0'
new_url = convert_google_sheet_url(url)
df = pd.read_csv(new_url)
print("Result: \n", df, "\n")

#data treatment and total of classes
df.columns = df.iloc[1]

print(df, "\n", "\n")

classes_number = int(df["Matricula"][0].split(": ")[1])

df = df.drop(index=[0, 1])

print("Total classes:", classes_number, "\n", "\n", "DataFrame: \n", df)

#Situation and grade for final approval calculation

df["P1"] = pd.to_numeric(df["P1"])
df["P2"] = pd.to_numeric(df["P2"])
df["P3"] = pd.to_numeric(df["P3"])
df["Faltas"] = pd.to_numeric(df["Faltas"])

df["Média"] = (df["P1"] + df["P2"] + df["P3"])/30

print("Averages: \n", df["Média"], "\n", "\n")

max_missed = classes_number / 4
print("Max missed classes: \n", max_missed, "\n", "\n")

situation = [df["Faltas"] > max_missed, df["Média"] < 5, (df["Média"] >= 5) & (df["Média"] < 7), df["Média"] >= 7] 
options = ["Reprovado por Falta", "Reprovado por Nota", "Exame Final", "Aprovado"]

df["Situação"] = np.select(situation, options)

print("Situation: \n", df["Situação"], "\n", "\n")

df["Nota para Aprovação Final"] = np.where(df["Situação"] == "Exame Final", (10 - df["Média"]), 0)
df["Nota para Aprovação Final"] = df["Nota para Aprovação Final"].apply(np.ceil).astype('int')
df.drop(columns=["Média"], inplace = True)

print("Final dataframe: \n", df)

gc = gspread.service_account(filename='googleapi-keys-sample.json')

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1qgPQ_uiRrkDv4eF_oBzOB0WhxlH8OlTC9ygGsdbmXVc/edit#gid=0')

worksheet = sh.worksheet("engenharia_de_software")

worksheet.update([df.columns.values.tolist()] + df.values.tolist(), 'A3')