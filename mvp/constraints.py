# enforces mental health rules so the data makes sense by fixing obviously impossible records. here is where domain knowledge must come in.


def apply_constraints(data):
    for i in range(len(data["diagnosis"])):
        if data["diagnosis"][i] == "none": # ie. if someone has no diagnosis, their PHQ-9 and GAD-7 must be low
            data["phq9"][i] = min(data["phq9"][i], 4)
            data["gad7"][i] = min(data["gad7"][i], 4)

        if data["diagnosis"][i] == "depression": # if depression, must have high PHQ-9
            data["phq9"][i] = max(data["phq9"][i], 10)

        if data["diagnosis"][i] == "anxiety": # if anxiety, must have high GAD-7
            data["gad7"][i] = max(data["gad7"][i], 10)

    return data
