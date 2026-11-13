
import math
import re


def parse_declaration(text):
    if not isinstance(text, str) or text.count(':') != 1:
        return None

    category, value = text.split(':')
    category = category.strip().lower()

    if not category:
        return None

    try:
        value = float(value)
    except (ValueError, OverflowError):
        return None

    if not math.isfinite(value) or value < 0:
        return None

    return category, value


def duty_amount(text):
    if not isinstance(text, str) or text.count('@') != 1:
        return None

    value, rate = text.split('@')

    try:
        value = float(value)
        rate = float(rate)
    except (ValueError, OverflowError):
        return None

    if not math.isfinite(value) or not math.isfinite(rate):
        return None

    if value < 0 or not 0 <= rate <= 100:
        return None

    result = value * rate / 100

    if not math.isfinite(result):
        return None

    return result


def hs_chapter(code):
    if not isinstance(code, str):
        return None

    code = code.strip()

    if not re.fullmatch(r'[0-9]{4}(?:[0-9]{2}|\.[0-9]{2})?', code):
        return None

    chapter = int(code[:2])

    if not 1 <= chapter <= 97 or chapter == 77:
        return None

    return chapter


def main():
    print("==== Running parse_declaration ====")
    user_input = input("Enter category:value (e.g. electronics:25000): ")
    result = parse_declaration(user_input)
    print("Category and Value:", result)

    print("\n==== Running duty_amount ====")
    user_input = input("Enter value@rate (e.g. 25000@20): ")
    result = duty_amount(user_input)
    print("Duty Amount:", result)

    print("\n==== Running hs_chapter ====")
    user_input = input("Enter an HS code (e.g. 8517.12): ")
    result = hs_chapter(user_input)
    print("Chapter:", result)


if __name__ == "__main__":
    main()
