# 🏦💸 Construção de um Sistema Bancário com Python - Bootcamp dio

> A título de validação esqueci que no PC que realizei os desafios estava configurando a conta do git do meu irmão (Yago). Mas os desafios foram realizados por mim (Danilo) 😄

## Descrição

Este projeto é um Sistema Bancário desenvolvido em Python, como parte do desafio proposto pelo Bootcamp da Digital Innovation One (DIO). O objetivo principal do sistema é permitir a realização de operações bancárias básicas, como depósitos, saques, criação de contas, e exibição de extratos. O sistema foi desenvolvido com uma arquitetura orientada a objetos, utilizando conceitos de herança, polimorfismo e abstração.

## Funcionalidades
O sistema bancário implementa as seguintes funcionalidades:

- Criar um novo usuário: O sistema permite criar clientes, vinculando informações como nome, CPF, data de nascimento e endereço.
- Criar uma nova conta: É possível criar contas correntes para os clientes cadastrados, associando as contas aos usuários.
- Realizar depósito: O usuário pode realizar depósitos em sua conta corrente.
- Realizar saque: O sistema permite saques, respeitando limites de saque por dia e o saldo disponível.
- Exibir extrato: Permite visualizar todas as transações realizadas em uma conta, incluindo depósitos e saques.
- Listar contas: Exibe a lista de todas as contas cadastradas no sistema.

## Regras de Negócio
- Um cliente pode ter uma ou mais contas bancárias.
- Para realizar uma transação (depósito ou saque), o cliente precisa estar cadastrado no sistema e possuir uma conta.
- Cada conta tem um limite diário de saques e um limite de valor por saque.
- Não é possível realizar saques com valor superior ao saldo disponível.
- O sistema impede mais de dois saques por dia.

## Estrutura de Código
O código está organizado em classes que representam as entidades do sistema bancário. Cada classe possui responsabilidades bem definidas, garantindo uma separação clara de responsabilidades e uma boa manutenção do código.

Classes Principais
- Cliente: Representa os clientes do banco, contendo informações pessoais e a lista de contas associadas.
- Conta: Representa uma conta bancária, contendo o saldo, o histórico de transações, e métodos para realizar depósitos e saques.
- ContaCorrente: Uma classe derivada de Conta, com limites de saque e saques diários.
- Transação: Classe abstrata para representar uma transação financeira. As classes Saque e Deposito herdam de Transação.
- Historico: Armazena o histórico de todas as transações realizadas em uma conta.
- Iterador de Contas: Permite iterar sobre todas as contas cadastradas no sistema para visualização.

## Exemplo de Uso
No menu principal, você verá as seguintes opções:

```
=============== MENU ================
[d]    Depositar
[s]    Sacar
[e]    Extrato
[nc]   Nova conta
[lc]   Listar contas
[nu]   Novo usuário
[q]    Sair
```


## Fluxo de Exemplo:
Criar um novo usuário:

Selecione a opção [nu] para cadastrar um novo cliente, informando CPF, nome, data de nascimento e endereço.
Criar uma conta:

Selecione a opção [nc] e associe uma conta ao cliente criado.
Realizar um depósito:

Selecione a opção [d], informe o CPF do cliente e o valor do depósito.
Realizar um saque:

Selecione a opção [s], informe o CPF do cliente e o valor do saque.
Exibir extrato:

Selecione a opção [e] para visualizar todas as transações e o saldo da conta.

## Tecnologias Utilizadas
- Python 3: Linguagem de programação principal.
- Programação Orientada a Objetos (POO): Implementada para garantir a modularidade e manutenibilidade do código.

## Melhorias Futuras
Algumas possíveis melhorias e funcionalidades adicionais para o sistema:

- Implementar autenticação com senha para o acesso às contas.
- Adicionar suporte a transferências entre contas.
- Criar uma interface gráfica para facilitar a interação do usuãrio com o sistema.
- Armazenamento das contas e transações em banco de dados ou arquivos XML, CSV, etc.

___

Feito para o Bootcamp DIO - NTT DATA - Engenharia de Dados com Python 🚀
