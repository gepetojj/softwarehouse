class Terminal:
    def __init__(self):
        pass

    @staticmethod
    def clear():
        print("\033[H\033[J")

    @staticmethod
    def print_header(title: str, padding_x: int = 2, padding_y: int = 1):
        print(f"\n{'=' * (len(title) + padding_x * 2)}")
        print("\n" * (max(0, padding_y - 1)))
        print(f"{' ' * padding_x}{title}")
        print("\n" * (max(0, padding_y - 1)))
        print(f"{'=' * (len(title) + padding_x * 2)}")

    @staticmethod
    def select(label: str, options: list[str]) -> int:
        print(label + "\n")
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        print()

        try:
            value = int(input("Escolha uma opção: ")) - 1
            if value < 0 or value > len(options) - 1:
                raise ValueError("Opção inválida.")

            return value
        except:
            raise ValueError("Opção inválida.")
