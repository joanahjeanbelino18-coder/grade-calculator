from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data Structure: Python List to store subject dictionaries
subjects = []

@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        # 1. Sequence & Variables
        name = request.form.get("subject", "").strip()
        units_raw = request.form.get("units", "")
        grade_raw = request.form.get("grade", "")

        # 2. Selection (Input Validation)
        try:
            units = float(units_raw)
            grade = float(grade_raw)

            if not name or units <= 0 or grade < 0 or grade > 100:
                error = "Enter a valid subject name, positive units, and a grade between 0 and 100."
            else:
                status = "Passed" if grade >= 75 else "Failed"
                # Append dictionary to List
                subjects.append({
                    "name": name,
                    "units": units,
                    "grade": grade,
                    "status": status
                })
                return redirect(url_for("index"))
        except ValueError:
            error = "Units and grade must be numeric values."

    # 3. Iteration (For Loop through the List)
    total_units = 0
    total_weighted_score = 0

    for sub in subjects:
        total_units += sub["units"]
        total_weighted_score += sub["grade"] * sub["units"]

    # 4. Calculation & Multi-way Selection (If / Elif / Else)
    if total_units > 0:
        average = total_weighted_score / total_units
        if average >= 90:
            remark = "Excellent (Dean's List Candidate)"
        elif average >= 75:
            remark = "Passed"
        else:
            remark = "Failed (Needs Improvement)"
    else:
        average = 0.0
        remark = "-"

    return render_template(
        "index.html",
        subjects=subjects,
        total_units=total_units,
        average=round(average, 2),
        remark=remark,
        error=error
    )

@app.route("/clear", methods=["POST"])
def clear():
    subjects.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)