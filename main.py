from src.lib.terminal import Terminal


while True:
    Terminal.clear()
    Terminal.print_header("Bem vindo ao sistema de gerenciamento")
    print("\n")

    try:
        option = Terminal.select(
            "O que deseja fazer?",
            ["Entrar", "Cadastrar", "Sair"]
        )
    except ValueError as e:
        Terminal.clear()
        print(e)
        input("Pressione Enter para continuar...")
        continue

    match option:
        case 0:
            continue
        case 1:
            continue
        case 2:
            Terminal.clear()
            Terminal.print_header("Até logo!")
            break
        case _:
            Terminal.clear()
            print("Opção inválida.")
            input("Pressione Enter para continuar...")
