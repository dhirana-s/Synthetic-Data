# validator.py
import numpy as np

class Validator:
    @staticmethod
    def check_ranges(row, schema):
        """Check if numeric columns respect min/max."""
        violations = []
        for col, info in schema["columns"].items():
            val = row[col]
            if info["type"] in ["int", "float"]:
                if not (info["min"] <= val <= info["max"]):
                    violations.append(f"{col}={val} out of range")
        return violations

    @staticmethod
    def check_dependencies(row, schema):
        """Check dependency constraints."""
        violations = []
        for dep in schema.get("dependencies", []):
            if "condition" in dep and not dep["condition"](row):
                violations.append(f"Dependency violated for {dep['if']}")
        return violations

    def validate_row(self, row, schema):
        """Validate a row fully."""
        return self.check_ranges(row, schema) + self.check_dependencies(row, schema)

    
    def check_correlations(rows, col_pairs, threshold=0.1):
        """Check that correlation between columns matches expectation (naive)"""
        violations = []
        for col_x, col_y, expected_r in col_pairs:
            vals_x = np.array([row[col_x] for row in rows])
            vals_y = np.array([row[col_y] for row in rows])
            corr = np.corrcoef(vals_x, vals_y)[0,1]
            if abs(corr - expected_r) > threshold:
                violations.append(f"{col_x}-{col_y} corr={corr:.2f} deviates from {expected_r}")
        return violations
