import random
import numpy as np
from .schema import tabular_schema

class Generator:
    def __init__(self, schema, seed=None):
        self.schema = schema
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    # generator.py (updated _sample_numeric)
    def _sample_numeric(self, col_info, col_name=None, row=None):
        """Sample numeric value using distributions and conditional logic"""
        if col_info.get("distribution") == "normal":
            val = int(np.random.normal(col_info["mean"], col_info["std"]))
            return max(min(val, col_info["max"]), col_info["min"])  # clamp to bounds

        elif col_info.get("distribution") == "conditional":
            # experience_years conditional on age
            if col_name == "experience_years" and row:
                return random.randint(0, row["age"] - 18)
            # salary conditional on experience and department
            elif col_name == "salary" and row:
                base = 20000
                dept_multiplier = {
                    "Engineering": 1.5,
                    "HR": 1.0,
                    "Sales": 1.2,
                    "Marketing": 1.1
                }
                exp_factor = 1 + (row["experience_years"] / 40)  # more experience → higher salary
                salary = base * dept_multiplier.get(row["department"], 1.0) * exp_factor
                # add some noise for realism
                noise = np.random.normal(0, 5000)
                salary = max(min(salary + noise, col_info["max"]), col_info["min"])
                return round(salary, 2)
            else:
                # default fallback
                return random.randint(col_info["min"], col_info["max"])
        else:
            # uniform fallback
            return random.randint(col_info["min"], col_info["max"])


    def _sample_column(self, col_name, row=None):
        col_info = self.schema["columns"][col_name]

        if col_info["type"] == "int" or col_info["type"] == "float":
            # For experience, condition on age
            conditioned_value = row["age"] if row and col_name == "experience_years" else None
            return self._sample_numeric(col_info, conditioned_value)
        elif col_info["type"] == "categorical":
            categories = col_info["categories"]
            probabilities = col_info.get("probabilities", None)
            return random.choices(categories, weights=probabilities, k=1)[0]
        else:
            raise ValueError(f"Unknown type {col_info['type']}")

    def generate_row(self):
        """Generate one row respecting dependencies and conditional distributions"""
        row = {}
        # sample department first if other columns depend on it
        if "department" in self.schema["columns"]:
            row["department"] = self._sample_column("department")

        for col in self.schema["columns"]:
            if col not in row:  # skip department since already sampled
                row[col] = self._sample_column(col, row)

        # Apply dependencies
        for dep in self.schema.get("dependencies", []):
            if "condition" in dep:
                while not dep["condition"](row):
                    row[dep["if"]] = self._sample_column(dep["if"], row)
        return row

    

    def generate_row_with_log(self):
        """Generate row and store why each value was sampled"""
        row = {}
        log = {}
        
        # sample department first
        row["department"] = self._sample_column("department")
        log["department"] = f"Random choice weighted by probabilities"

        for col in self.schema["columns"]:
            if col != "department":
                val = self._sample_column(col, row)
                row[col] = val
                log[col] = f"Sampled using distribution={self.schema['columns'][col].get('distribution','uniform')}"
        
        # enforce dependencies
        for dep in self.schema.get("dependencies", []):
            if "condition" in dep:
                while not dep["condition"](row):
                    row[dep["if"]] = self._sample_column(dep["if"], row)
                    log[dep["if"]] = f"Resampled to satisfy dependency {dep}"
        
        return row, log


    def generate(self, n_rows):
        """Generate multiple rows"""
        return [self.generate_row() for _ in range(n_rows)]
