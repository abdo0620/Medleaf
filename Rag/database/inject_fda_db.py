"""Entry point for indexing the downloaded FDA labels."""

import sys 
from pathlib import Path
PARENT_DIR=Path(__file__).parent 
sys.path.append(str(PARENT_DIR))
import initialize_db


initialize_db.initialize_fda_drugs()
