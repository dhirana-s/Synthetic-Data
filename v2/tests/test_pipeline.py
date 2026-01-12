import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lab.generator import Generator
from lab.validator import Validator
from lab.schema import tabular_schema


# initialize generator and validator
gen = Generator(tabular_schema, seed=42)
validator = Validator()

# generate 10 rows with logs
for i in range(10):
    row, log = gen.generate_row_with_log()
    print(f"\nRow {i}: {row}")
    print("Audit log:")
    for col, reason in log.items():
        print(f" - {col}: {reason}")
    
    # validate row
    violations = validator.validate_row(row, tabular_schema)
    if violations:
        print("Violations:", violations)
    else:
        print("Valid row ✅")
