import re
from string import ascii_letters, digits, punctuation
from db import  RUN_SQL
from uuid import uuid4
from random import random

def randomstr(): return uuid4().hex
def rnd(l=6): return ''.join([f'{random().__str__().split(".")[0]}' for i in range(l)])
def verifyUsername(name: str):
    if not name:
        return False
    for i in name:
        if i not in digits + ascii_letters + ' _-.':
            return False
    return True

def verifyMail(mail: str):
    return re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        mail
    ) is not None

def verifyPswd(password: str) -> bool:
    strength = 0
    strength += any(c.isalpha() for c in password)
    strength += any(c in punctuation for c in password)
    strength += any(c.isdigit() for c in password)
    strength += (len(password) >= 8)
    return strength == 4

async def isUnique(item, col, table):
    query = f"SELECT COUNT(*) FROM {table} WHERE {col} = '{item}';"
    selected = await RUN_SQL(query,True)
    return not bool(selected[0].get("COUNT(*)") if selected else 0)

def escapeSQL(s) -> str:
    return str(s).replace("'", "''")

