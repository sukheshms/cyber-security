import string
from pathlib import Path


# -----------------------------
# Load common passwords
# -----------------------------
def load_common_passwords():
    file_path = Path("common_passwords.txt")

    if not file_path.exists():
        return {
            "123456",
            "password",
            "12345678",
            "qwerty",
            "admin",
            "welcome",
            "password123"
        }

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return {
                line.strip().lower()
                for line in file
                if line.strip()
            }
    except OSError:
        return set()


# -----------------------------
# Check predictable patterns
# -----------------------------
def has_predictable_pattern(password):
    lower_password = password.lower()

    predictable_patterns = [
        "123456",
        "12345678",
        "qwerty",
        "abcdef",
        "password",
        "admin",
        "welcome"
    ]

    for pattern in predictable_patterns:
        if pattern in lower_password:
            return True

    return False


# -----------------------------
# Analyze password
# -----------------------------
def analyze_password(password, common_passwords):
    result = {
        "length": len(password),
        "uppercase": any(char.isupper() for char in password),
        "lowercase": any(char.islower() for char in password),
        "number": any(char.isdigit() for char in password),
        "special": any(char in string.punctuation for char in password),
        "common": password.lower() in common_passwords,
        "predictable": has_predictable_pattern(password)
    }

    score = 0

    # Length
    if len(password) >= 8:
        score += 1

    # Character types
    if result["uppercase"]:
        score += 1

    if result["lowercase"]:
        score += 1

    if result["number"]:
        score += 1

    if result["special"]:
        score += 1

    # Reduce score for risky characteristics
    if result["common"]:
        score = max(0, score - 2)

    if result["predictable"]:
        score = max(0, score - 1)

    # Determine strength
    if score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    result["score"] = score
    result["strength"] = strength

    return result


# -----------------------------
# Generate suggestions
# -----------------------------
def generate_suggestions(result):
    suggestions = []

    if result["length"] < 8:
        suggestions.append("Use at least 8 characters.")

    if not result["uppercase"]:
        suggestions.append("Add at least one uppercase letter.")

    if not result["lowercase"]:
        suggestions.append("Add at least one lowercase letter.")

    if not result["number"]:
        suggestions.append("Add at least one number.")

    if not result["special"]:
        suggestions.append("Add at least one special character.")

    if result["common"]:
        suggestions.append("Avoid commonly used passwords.")

    if result["predictable"]:
        suggestions.append("Avoid predictable words or patterns.")

    if not suggestions:
        suggestions.append("No basic weaknesses detected.")

    return suggestions


# -----------------------------
# Display analysis
# -----------------------------
def display_result(password, result, suggestions):
    print("\n" + "=" * 50)
    print("           PASSWORD SECURITY ANALYZER")
    print("=" * 50)

    # Do not print the actual password.
    print(f"Password length      : {result['length']}")

    print(
        f"Uppercase letters    : "
        f"{'YES' if result['uppercase'] else 'NO'}"
    )

    print(
        f"Lowercase letters    : "
        f"{'YES' if result['lowercase'] else 'NO'}"
    )

    print(
        f"Numbers              : "
        f"{'YES' if result['number'] else 'NO'}"
    )

    print(
        f"Special characters   : "
        f"{'YES' if result['special'] else 'NO'}"
    )

    print(
        f"Common password      : "
        f"{'YES' if result['common'] else 'NO'}"
    )

    print(
        f"Predictable pattern  : "
        f"{'YES' if result['predictable'] else 'NO'}"
    )

    print("-" * 50)
    print(f"Security Score       : {result['score']}/5")
    print(f"Password Strength    : {result['strength']}")
    print("-" * 50)

    print("Recommendations:")

    for suggestion in suggestions:
        print(f" - {suggestion}")

    print("=" * 50)


# -----------------------------
# Main program
# -----------------------------
def main():
    common_passwords = load_common_passwords()

    print("=" * 50)
    print("       PASSWORD SECURITY ANALYZER")
    print("=" * 50)

    print("Enter a password to analyze.")
    print("Your password is analyzed locally and is not saved.")
    print()

    password = input("Enter password: ")

    if not password:
        print("Password cannot be empty.")
        return

    result = analyze_password(password, common_passwords)
    suggestions = generate_suggestions(result)

    display_result(password, result, suggestions)


if __name__ == "__main__":
    main()
