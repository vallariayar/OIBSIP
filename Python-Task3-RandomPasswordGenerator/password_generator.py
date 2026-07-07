import random
import string


def get_length():
    while True:
        value = input("Enter desired password length (min 8): ").strip()
        try:
            length = int(value)
        except ValueError:
            print("Error: Please enter a whole number.")
            continue
        if length < 8:
            print("Error: Length must be at least 8 characters.")
            continue
        return length


def get_character_types():
    print("\nChoose character types to include (select at least 2):")
    print("  1. Uppercase letters (A-Z)")
    print("  2. Lowercase letters (a-z)")
    print("  3. Numbers (0-9)")
    print("  4. Symbols (!@#$%^&*...)")

    while True:
        choices = input("Enter numbers separated by spaces (e.g., 1 2 3): ").strip()
        selected = set(choices.split())

        valid_options = {"1", "2", "3", "4"}
        if not selected.issubset(valid_options) or not selected:
            print("Error: Please enter valid options from 1-4.")
            continue
        if len(selected) < 2:
            print("Error: You must select at least 2 character types.")
            continue

        pools = []
        if "1" in selected:
            pools.append(string.ascii_uppercase)
        if "2" in selected:
            pools.append(string.ascii_lowercase)
        if "3" in selected:
            pools.append(string.digits)
        if "4" in selected:
            pools.append("!@#$%^&*()-_=+[]{};:,.<>?/")

        return pools


def generate_password(length, pools):
    # Ensure at least one character from each selected pool
    password_chars = [random.choice(pool) for pool in pools]

    all_chars = "".join(pools)
    remaining = length - len(password_chars)
    password_chars += [random.choice(all_chars) for _ in range(remaining)]

    random.shuffle(password_chars)
    return "".join(password_chars)


def main():
    print("=== Random Password Generator ===\n")

    length = get_length()
    pools = get_character_types()

    password = generate_password(length, pools)

    print(f"\nGenerated Password: {password}")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nGenerate another password? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()