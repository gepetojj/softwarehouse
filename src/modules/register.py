from src.lib.terminal import Terminal
from src.lib.database import Database
import uuid

def register():
    while True:
        Terminal.clear()
        Terminal.print_header("Cadastro de funcionário")
        print()

        name = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        secret_code = input("Código secreto: ")

        if secret_code != "1234":
            Terminal.clear()
            print("Código secreto inválido.")
            input("Pressione Enter para continuar...")
            continue

        db = Database()
        exists = db.read("funcionarios", "email", email)

        if exists:
            Terminal.clear()
            print("Email já cadastrado.")
            
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

        db.create("funcionarios", {
            "id": uuid.uuid4().hex,
            "nome": name,
            "email": email,
            "telefone": telefone,
        })
        break