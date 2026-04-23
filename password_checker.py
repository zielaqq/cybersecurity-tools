# password_checker.py
import re
import string


def check_password_strength(password):
    score = 0
    feedback = []

    # Długość hasła
    length = len(password)
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
        feedback.append("⚠️  Hasło powinno mieć co najmniej 12 znaków")
    else:
        feedback.append("❌ Hasło jest zbyt krótkie (min. 8 znaków)")

    # Wielkie litery
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("❌ Dodaj wielkie litery (A-Z)")

    # Małe litery
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Dodaj małe litery (a-z)")

    # Cyfry
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Dodaj cyfry (0-9)")

    # Znaki specjalne
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("❌ Dodaj znaki specjalne (!@#$%^&*)")

    # Sprawdź popularne hasła
    common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome']
    if password.lower() in common_passwords:
        score = 0
        feedback.append("🚨 To hasło jest na liście najpopularniejszych haseł!")

    # Oceń siłę
    if score >= 6:
        strength = "🟢 SILNE"
        color = "\033[92m"
    elif score >= 4:
        strength = "🟡 ŚREDNIE"
        color = "\033[93m"
    else:
        strength = "🔴 SŁABE"
        color = "\033[91m"

    return {
        'score': score,
        'strength': strength,
        'feedback': feedback,
        'color': color
    }


def print_banner():
    """Wyświetla banner programu"""
    print("\n" + "=" * 50)
    print("🔐  PASSWORD STRENGTH CHECKER  🔐")
    print("    By Hubert Zieliński")
    print("=" * 50 + "\n")


def main():
    print_banner()

    while True:
        password = input("Wprowadź hasło do sprawdzenia (lub 'q' aby wyjść): ")

        if password.lower() == 'q':
            print("\n👋 Dziękuję za skorzystanie z programu!")
            break

        if not password:
            print("❌ Hasło nie może być puste!\n")
            continue

        # Sprawdź hasło
        result = check_password_strength(password)

        # Wyświetl wyniki
        print("\n" + "-" * 50)
        print(f"Długość hasła: {len(password)} znaków")
        print(f"Ocena: {result['score']}/7 punktów")
        print(f"{result['color']}Siła hasła: {result['strength']}\033[0m")

        if result['feedback']:
            print("\n📋 Rekomendacje:")
            for tip in result['feedback']:
                print(f"  {tip}")
        else:
            print("\n✅ Hasło spełnia wszystkie wymagania!")

        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()