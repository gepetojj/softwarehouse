from src.lib.terminal import Terminal
from src.lib.database import Database
import uuid


def manage_cash():
    db = Database()

    while True:
        Terminal.clear()
        Terminal.print_header("Gerenciamento Financeiro")
        print()

        try:
            option = Terminal.select(
                "Escolha uma opção:",
                [
                    "Listar transações",
                    "Cadastrar transação",
                    "Remover transação",
                    "Gerar relatório financeiro",
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
                list_transactions(db)
            case 1:
                register_transaction(db)
            case 2:
                remove_transaction(db)
            case 3:
                generate_financial_report(db)
            case 4:
                break
            case _:
                Terminal.clear()
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                continue


def list_transactions(db: Database):
    Terminal.clear()
    Terminal.print_header("Lista de Transações")
    print()

    transactions = db.read_all("financeiro")

    if not transactions:
        print("Nenhuma transação registrada.")
    else:
        for trans in transactions:
            print(f"ID: {trans['id']}")
            print(f"Nome: {trans['nome']}")
            print(f"Descrição: {trans['descricao']}")
            print(f"Tipo: {trans['tipo']}")
            print(f"Valor: R$ {float(trans['valor']):.2f}")
            print("-" * 30)

    input("Pressione Enter para continuar...")


def register_transaction(db: Database):
    while True:
        Terminal.clear()
        Terminal.print_header("Cadastro de Transação")
        print()

        name = input("Nome: ")
        description = input("Descrição: ")
        tipo = Terminal.select("Tipo da transação:", ["ENTRADA", "SAÍDA"])

        while True:
            valor_str = input(
                "Valor (use '.' ou ',' para separar centavos): "
            ).replace(",", ".")
            try:
                valor = float(valor_str)
                if valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")
                break
            except ValueError:
                print("Valor inválido. Digite um número positivo.")
                input("Pressione Enter para tentar novamente...")

        db.create("financeiro", {
            "id": uuid.uuid4().hex,
            "nome": name,
            "descricao": description,
            "tipo": "ENTRADA" if tipo == 0 else "SAÍDA",
            "valor": valor,
        })

        print("Transação cadastrada com sucesso!")
        input("Pressione Enter para continuar...")
        break


def remove_transaction(db: Database):
    Terminal.clear()
    Terminal.print_header("Remover Transação")
    print()

    name = input("Digite o nome da transação a ser removida: ")

    transaction = db.read("financeiro", "nome", name)

    if not transaction:
        print("Transação não encontrada.")
    else:
        db.delete("financeiro", "nome", name)
        print("Transação removida com sucesso!")

    input("Pressione Enter para continuar...")


def generate_financial_report(db: Database):
    Terminal.clear()
    Terminal.print_header("Relatório Financeiro")
    print()

    transactions = db.read_all("financeiro")

    if not transactions:
        print("Nenhuma transação registrada.")
    else:
        total_entrada = sum(
            float(trans['valor']) for trans in transactions if trans['tipo'] == "ENTRADA")
        total_saida = sum(float(trans['valor'])
                          for trans in transactions if trans['tipo'] == "SAÍDA")
        saldo = total_entrada - total_saida

        print("=" * 50)
        print("RELATÓRIO FINANCEIRO")
        print("=" * 50)
        print()
        for trans in transactions:
            print(
                f"{trans['tipo']}: {trans['nome']} - R$ {float(trans['valor']):.2f}")
        print("-" * 50)
        print(f"Total Entradas: R$ {total_entrada:.2f}")
        print(f"Total Saídas: R$ {total_saida:.2f}")
        print(f"Saldo Final: R$ {saldo:.2f}")

    input("Pressione Enter para continuar...")
