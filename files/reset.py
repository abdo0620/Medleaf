import os

i=os.listdir("files/drug_text_files/")
for file in i :
    if file[-3:]=="txt":
        os.remove("files/drug_text_files/"+ file)
