from src.lib.terminal import Terminal
from src.lib.database import Database
import uuid


def manage_employees():
    db = Database()

    while True:
        Terminal.clear()
        Terminal.print_header("Gerenciamento de Funcionários")
        print()

        try:
            option = Terminal.select(
                "Escolha uma opção:",
                [
                    "Listar funcionários",
                    "Cadastrar funcionário",
                    "Remover funcionário",
                    "Voltar"
                ]
            )
        except Exception as e:
            Terminal.clear()
            print(e)
            input("Pressione Enter para continuar...")
            continue

        match option:
            case 0:
                list_employees(db)
            case 1:
                register_employee(db)
            case 2:
                remove_employee(db)
            case 3:
                break
            case _:
                Terminal.clear()
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                continue


def list_employees(db: Database):
    Terminal.clear()
    Terminal.print_header("Lista de Funcionários")
    print()

    employees = db.read_all("funcionarios")

    if not employees:
        print("Nenhum funcionário cadastrado.")
    else:
        for emp in employees:
            print(f"ID: {emp['id']}")
            print(f"Nome: {emp['nome']}")
            print(f"Email: {emp['email']}")
            print(f"Telefone: {emp['telefone']}")
            print("-" * 30)

    input("Pressione Enter para continuar...")


def register_employee(db: Database):
    while True:
        Terminal.clear()
        Terminal.print_header("Cadastro de Funcionário")
        print()

        name = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")

        exists = db.read("funcionarios", "email", email)

        if exists:
            Terminal.clear()
            print("Email já cadastrado.")

            try:
                option = Terminal.select(
                    "Deseja tentar novamente?", ["Sim", "Não"])
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

        print("Funcionário cadastrado com sucesso!")
        input("Pressione Enter para continuar...")
        break


def remove_employee(db: Database):
    Terminal.clear()
    Terminal.print_header("Remover Funcionário")
    print()

    email = input("Digite o email do funcionário a ser removido: ")

    employee = db.read("funcionarios", "email", email)

    if not employee:
        print("Funcionário não encontrado.")
    else:
        db.delete("funcionarios", "email", email)
        print("Funcionário removido com sucesso!")

    input("Pressione Enter para continuar...")
