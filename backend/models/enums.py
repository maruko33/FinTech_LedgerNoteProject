from enum import Enum

class AccountType(str, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    EQUITY = "EQUITY"


class EntrySource(str, Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"


class EntryStatus(str, Enum):
    POSTED = "POSTED"
    VOID = "VOID"


class BudgetPeriod(str, Enum):
    MONTHLY = "MONTHLY"
