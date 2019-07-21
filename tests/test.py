import sqlite3 as sq

import pytest

from bot.bd_interacting import *
import os

@pytest.fixture
def storage():
    os.system("rm test.db")
    os.system('sqlite3 test.db ";"')
    storage=Storage("test.db")
    return storage

def test_creating_db(storage):
    storage
    tables = storage.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    assert [("taxa",), ("descriptions",)] == tables.fetchall()
    storage.cursor.execute("SELECT * FROM taxa")
