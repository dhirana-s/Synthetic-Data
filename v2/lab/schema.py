from typing import Dict, Any

tabular_schema: Dict[str, Any] = {
    "columns": {
        "age": {
            "type": "int",
            "min": 18,
            "max": 65,
            "distribution": "normal",  # normal or uniform
            "mean": 35,
            "std": 10
        },
        "salary": {
            "type": "float",
            "min": 20000,
            "max": 200000,
            "distribution": "conditional",  # will condition on experience and department
            "cohorts": ["Engineering", "HR", "Sales", "Marketing"]
        },
        "department": {
            "type": "categorical",
            "categories": ["Engineering", "HR", "Sales", "Marketing"],
            "probabilities": [0.4, 0.2, 0.25, 0.15]
        },
        "experience_years": {
            "type": "int",
            "min": 0,
            "max": 40,
            "distribution": "conditional",  # conditioned on age
        }
    },
    "dependencies": [
        # experience_years <= age - 18
        {"if": "experience_years", "condition": lambda row: row["experience_years"] <= row["age"] - 18}
    ]
}
