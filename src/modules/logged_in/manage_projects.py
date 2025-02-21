from src.lib.terminal import Terminal
from src.lib.database import Database
import uuid


def manage_projects():
    db = Database()

    while True:
        Terminal.clear()
        Terminal.print_header("Gerenciamento de Projetos")
        print()

        try:
            option = Terminal.select(
                "Escolha uma opção:",
                [
                    "Listar projetos",
                    "Cadastrar projeto",
                    "Remover projeto",
                    "Gerar relatório de projetos",
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
                list_projects(db)
            case 1:
                register_project(db)
            case 2:
                remove_project(db)
            case 3:
                generate_project_report(db)
            case 4:
                break
            case _:
                Terminal.clear()
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                continue


def list_projects(db: Database):
    Terminal.clear()
    Terminal.print_header("Lista de Projetos")
    print()

    projects = db.read_all("projetos")

    if not projects:
        print("Nenhum projeto cadastrado.")
    else:
        for proj in projects:
            print(f"ID: {proj['id']}")
            print(f"Nome: {proj['nome']}")
            print(f"Descrição: {proj['descricao']}")
            print("-" * 30)

    input("Pressione Enter para continuar...")


def register_project(db: Database):
    while True:
        Terminal.clear()
        Terminal.print_header("Cadastro de Projeto")
        print()

        name = input("Nome: ")
        description = input("Descrição: ")

        exists = db.read("projetos", "nome", name)

        if exists:
            Terminal.clear()
            print("Nome de projeto já cadastrado.")

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

        db.create("projetos", {
            "id": uuid.uuid4().hex,
            "nome": name,
            "descricao": description,
        })

        print("Projeto cadastrado com sucesso!")
        input("Pressione Enter para continuar...")
        break


def remove_project(db: Database):
    Terminal.clear()
    Terminal.print_header("Remover Projeto")
    print()

    name = input("Digite o nome do projeto a ser removido: ")

    project = db.read("projetos", "nome", name)

    if not project:
        print("Projeto não encontrado.")
    else:
        db.delete("projetos", "nome", name)
        print("Projeto removido com sucesso!")

    input("Pressione Enter para continuar...")


def generate_project_report(db: Database):
    Terminal.clear()
    Terminal.print_header("Relatório de Projetos")
    print()

    projects = db.read_all("projetos")

    if not projects:
        print("Nenhum projeto cadastrado.")
    else:
        print("=" * 50)
        print("RELATÓRIO DE PROJETOS")
        print("=" * 50)
        print()
        for proj in projects:
            print(f"Projeto: {proj['nome']}")
            print(f"Descrição: {proj['descricao']}")
            print("-" * 50)

    input("Pressione Enter para continuar...")
