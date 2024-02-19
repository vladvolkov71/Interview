from main import is_balanced
import pytest


class Tests_pytest:

    @pytest.mark.parametrize('string, rec', [
        ('()[]{}', True),
        ('(]', False),
        ('[([])((([[[]]])))]{()}', True),
        ('{{[(])]}}', False)
    ])
    def test_is_balanced(self, string: str, rec):
        assert is_balanced(string) is rec
