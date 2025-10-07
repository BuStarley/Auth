import pytest
from sqlalchemy import text
from app.database import Base, engine, get_db


class TestDatabaseConnection:

    def test_connection(self):
        connection = engine.connect()
        assert connection is not None

        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
        connection.close()
