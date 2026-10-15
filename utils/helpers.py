
def display_title(title):
    print("\n" + "=" * 45)
    print(title.center(45))
    print("=" * 45)


def pause():
    input("\nPress Enter to continue...")


def confirm_action(message):
    answer = input(f"{message} (yes/no): ").strip().lower()
    return answer in ("yes", "y")

