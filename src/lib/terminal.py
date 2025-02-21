class Terminal:
    def __init__(self):
        pass

    @staticmethod
    def print_header(title: str):
        padding_x = 2
        padding_y = 1

        print(f"\n{'=' * (len(title) + padding_x * 2)}")
        print("\n" * (max(0, padding_y - 1)))
        print(f"{' ' * padding_x}{title}")
        print("\n" * (max(0, padding_y - 1)))
        print(f"{'=' * (len(title) + padding_x * 2)}")
