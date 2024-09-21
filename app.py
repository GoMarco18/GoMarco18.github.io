from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate required grades
def calculate_required_grades(prelim_grade):
    # Define constants
    PASSING_GRADE = 75  # Minimum passing grade is 75%
    MAXIMUM_GRADE = 100  # Maximum grade is 100%
    MIDTERM_WEIGHT = 0.30
    FINAL_WEIGHT = 0.50
    PRELIM_WEIGHT = 0.20

    # Calculate the total contribution from prelims
    prelim_contribution = prelim_grade * PRELIM_WEIGHT

    # Check if the prelim score is enough to pass with 75% in midterm and final
    if prelim_contribution + (PASSING_GRADE * MIDTERM_WEIGHT) + (PASSING_GRADE * FINAL_WEIGHT) >= PASSING_GRADE:
        return f"You can pass with at least 75% in both Midterms and Finals."

    # Calculate the remaining grades required for midterm and final
    remaining_to_pass = PASSING_GRADE - prelim_contribution

    # Check if it's impossible to pass
    if remaining_to_pass > (MIDTERM_WEIGHT * MAXIMUM_GRADE) + (FINAL_WEIGHT * MAXIMUM_GRADE):
        return "It's impossible to pass, even with perfect scores in Midterms and Finals."

    # Calculate required scores in Midterm and Final assuming equal performance
    min_midterm = remaining_to_pass / (MIDTERM_WEIGHT + FINAL_WEIGHT) * MIDTERM_WEIGHT
    min_final = remaining_to_pass / (MIDTERM_WEIGHT + FINAL_WEIGHT) * FINAL_WEIGHT

    # Adjust the result if the required scores are higher than 100%
    if min_midterm > MAXIMUM_GRADE or min_final > MAXIMUM_GRADE:
        return "To pass, you need more than 100% in either Midterms or Finals, which is impossible."

    # If the minimum grades are within the 75% to 100% range
    if min_midterm >= PASSING_GRADE and min_final >= PASSING_GRADE:
        return f"To pass, you need at least {min_midterm:.2f}% in Midterms and {min_final:.2f}% in Finals."
    else:
        return f"You can pass with a minimum of 75% in both Midterms and Finals."

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Get input from the form
            prelim_grade = float(request.form['prelim_grade'])

            if prelim_grade < 0 or prelim_grade > 100:
                error = "Prelim grade must be between 0 and 100."
            else:
                # Calculate the required grades
                result = calculate_required_grades(prelim_grade)
        except ValueError:
            error = "Please enter a valid numerical grade."

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)