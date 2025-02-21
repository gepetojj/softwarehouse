from src.lib.terminal import Terminal
from src.lib.database import Database

def login():
    while True:
        Terminal.clear()
        Terminal.print_header("Login de funcionário")
        print()

        email = input("Email: ")

        db = Database()
        exists = db.read("funcionarios", "email", email)

        if not exists:
            Terminal.clear()
            print("Email não encontrado.")
            
            try:
                option = Terminal.select(
                    "Deseja tentar novamente?",
                    ["Sim", "Não"]
                )
            except Exception as e:
                Terminal.clear()
                print(e)
                input("Pressione Enter para continuar...")
                continue

            if option == 0:
                continue
            else:
                break

        return exists
