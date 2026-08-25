"""Remove generated FDA text and JSON files from the local data folders."""

from pathlib import Path
PARENT_DIR= Path(__file__).parent
i=(PARENT_DIR / "drug_text_files").iterdir()
j=(PARENT_DIR / "drug_json_files").iterdir()
for file in i:
        file.unlink()

for file in j:
        file.unlink()

        
