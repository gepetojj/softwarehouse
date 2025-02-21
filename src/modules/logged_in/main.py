from src.lib.terminal import Terminal
from src.modules.logged_in.manage_employees import manage_employees


def logged_in(user: dict):
    while True:
        Terminal.clear()
        Terminal.print_header(f"Bem vindo, {user['nome']}!")
        print()

        try:
            option = Terminal.select(
                "O que deseja fazer?",
                [
                    "Gerenciar funcionários",
                    "Gerenciar projetos",
                    "Gerenciar caixa",
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
                manage_employees()
            case 1:
                manage_projects()
            case 2:
                manage_cash()
            case 3:
                break
            case _:
                Terminal.clear()
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                continue
