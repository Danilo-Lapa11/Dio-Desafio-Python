import textwrap
from datetime import datetime
from dataclasses import dataclass
import pytz
from abc import ABC, abstractmethod


@dataclass
class PessoaFisica:
    nome: str
    data_nascimento: str
    cpf: str
    endereco: str
    contas: list = None

    def __post_init__(self):
        if self.contas is None:
            self.contas = []


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now(pytz.utc).strftime("%d-%m-%Y %H:%M:%S")
        })

    def gerar_relatorio(self):
        for transacao in self.transacoes:
            yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        return [
            transacao for transacao in self.transacoes
            if datetime.strptime(transacao['data'], "%d-%m-%Y %H:%M:%S").date() == data_atual
        ]


class Conta:
    def __init__(self, numero: int, cliente: PessoaFisica):
        self._numero = numero
        self._agencia = "0001"
        self._saldo = 0.0
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float):
        if valor <= 0:
            print("Valor inválido!")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente!")
            return False
        self._saldo -= valor
        print("Saque realizado com sucesso!")
        return True

    def depositar(self, valor: float):
        if valor <= 0:
            print("Valor inválido!")
            return False
        self._saldo += valor
        print("Depósito realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: PessoaFisica, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float):
        if valor > self._limite:
            print("O valor excede o limite de saque!")
            return False
        saques_realizados = len([t for t in self.historico.transacoes if t['tipo'] == 'Saque'])
        if saques_realizados >= self._limite_saques:
            print("Limite de saques diários excedido!")
            return False
        return super().sacar(valor)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        Deposito(valor).registrar(conta)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        Saque(valor).registrar(conta)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n Já existe cliente com esse CPF! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado, fluxo de criação de conta encerrado! ")
        return

    conta = ContaCorrente(numero=numero_conta, cliente=cliente, limite=500, limite_saques=3)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if not contas:
        print("\nNão há contas cadastradas.")
        return
    for conta in contas:
        print(f"Agência: {conta.agencia}\tNúmero: {conta.numero}\tTitular: {conta.cliente.nome}\tSaldo: R$ {conta.saldo:.2f}")


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente: PessoaFisica):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return None
    return cliente.contas[0]


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida! Escolha novamente.")

main()
