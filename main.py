from src.lib.terminal import Terminal
from src.modules.register import register
from src.modules.login import login
from src.modules.logged_in.main import logged_in
import sys


while True:
    Terminal.clear()
    Terminal.print_header("Bem vindo ao sistema de gerenciamento")
    print()

    try:
        option = Terminal.select(
            "O que deseja fazer?",
            ["Entrar", "Cadastrar", "Sair"]
        )
    except Exception as e:
        Terminal.clear()
        print(e)
        input("Pressione Enter para continuar...")
        continue

    match option:
        case 0:
            user = login()
            if not user:
                sys.exit(1)
            logged_in(user)
        case 1:
            register()
        case 2:
            Terminal.clear()
            Terminal.print_header("Até logo!")
            break
        case _:
            Terminal.clear()
            print("Opção inválida.")
            input("Pressione Enter para continuar...")
