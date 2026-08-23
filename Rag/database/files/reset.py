import os
from path import Path 
PARENT_DIR= Path(__file__).parent
i=os.listdir(PARENT_DIR / "drug_text_files")
j=os.listdir(PARENT_DIR / "drug_json_files")
for file in i :
        os.remove(PARENT_DIR /"drug_text_files"/ file)

for file in j :
        os.remove(PARENT_DIR / "drug_json_files"/ file)

        
