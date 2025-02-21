from src.lib.terminal import Terminal
from src.lib.database import Database
import uuid


def manage_customers():
    db = Database()

    while True:
        Terminal.clear()
        Terminal.print_header("Gerenciamento de Clientes")
        print()

        try:
            option = Terminal.select(
                "Escolha uma opção:",
                [
                    "Listar clientes",
                    "Cadastrar cliente",
                    "Remover cliente",
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
                list_customers(db)
            case 1:
                register_client(db)
            case 2:
                remove_client(db)
            case 3:
                break
            case _:
                Terminal.clear()
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                continue


def list_customers(db: Database):
    Terminal.clear()
    Terminal.print_header("Lista de Clientes")
    print()

    customers = db.read_all("clientes")

    if not customers:
        print("Nenhum cliente cadastrado.")
    else:
        for client in customers:
            print(f"ID: {client['id']}")
            print(f"Nome: {client['nome']}")
            print("-" * 30)

    input("Pressione Enter para continuar...")


def register_client(db: Database):
    while True:
        Terminal.clear()
        Terminal.print_header("Cadastro de Cliente")
        print()

        name = input("Nome: ")

        exists = db.read("clientes", "nome", name)

        if exists:
            Terminal.clear()
            print("Cliente já cadastrado.")

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

        db.create("clientes", {
            "id": uuid.uuid4().hex,
            "nome": name,
        })

        print("Cliente cadastrado com sucesso!")
        input("Pressione Enter para continuar...")
        break


def remove_client(db: Database):
    Terminal.clear()
    Terminal.print_header("Remover Cliente")
    print()

    name = input("Digite o nome do cliente a ser removido: ")

    client = db.read("clientes", "nome", name)

    if not client:
        print("Cliente não encontrado.")
    else:
        db.delete("clientes", "nome", name)
        print("Cliente removido com sucesso!")

    input("Pressione Enter para continuar...")
