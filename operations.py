from enum import Enum


class Operations(Enum):
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
    CHECK_BALANCE = 4


def is_valid_operation(operation):
    return operation in {op.value for op in Operations}


def operation_message(selected_operation):
    match selected_operation:
        case Operations.DEPOSIT:
            return "Digite o valor a ser depositado: \n"
        case Operations.WITHDRAW:
            return "Digite o valor a ser sacado: \n"
        case Operations.TRANSFER:
            return "Digite o valor a ser transferido: \n"
        case Operations.CHECK_BALANCE:
            return ""
        case _:
            return "Operação inválida, tente novamente.\n"
