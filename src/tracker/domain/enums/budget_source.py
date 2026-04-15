from enum import StrEnum


class BudgetSource(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"
    CREDIT_DEBT = "credit_debt"
    DEBIT_DEBT = "debit_debt"
    SPLIT_RECEIVABLE = "split_receivable"
    SPLIT_PAYABLE = "split_payable"
