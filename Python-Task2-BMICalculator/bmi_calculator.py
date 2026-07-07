def get_positive_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
        except ValueError:
            print("Error: Please enter a valid number (e.g., 65.5).")
            continue
        if num <= 0:
            print("Error: Value must be greater than zero.")
            continue
        return num


def get_height_m():
    while True:
        height = get_positive_float("Enter your height (m): ")
        if height > 3:
            # Likely entered in cm instead of meters (e.g., 160 instead of 1.60)
            converted = height / 100
            print(f"Note: {height} looks like it's in centimeters. Using {converted:.2f} m instead.")
            return converted
        return height


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def main():
    print("=== BMI Calculator ===\n")

    weight = get_positive_float("Enter your weight (kg): ")
    height = get_height_m()

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print(f"\nYour BMI: {bmi:.2f}")
    print(f"Category: {category}")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nCalculate another? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break