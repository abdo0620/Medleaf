import os

i=os.listdir("files/drug_text_files/")
j=os.listdir("files/drug_json_files/")
for file in i :
    if file[-3:]=="txt":
        os.remove("files/drug_text_files/"+ file)

for file in j :
    if file[-3:]=="json":
        os.remove("files/drug_json_files/"+ file)
        

        
