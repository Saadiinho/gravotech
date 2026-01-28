import pytest

from gravotech.utils.errors import check_err


@pytest.mark.parametrize(
    "input_err, expected_msg",
    [
        ("ER 2 1", "Context error (invalid state): Initialization (code: 2.1)"),
        (
            "ER 2 state",
            "Context error (invalid state): graveuse not in correct state (code: 2.state)",
        ),
    ],
)
def test_check_err_success(input_err: str, expected_msg: str):
    """Vérifie que les réponses qui ne sont pas des erreurs passent sans problème."""
    assert check_err(input_err) == expected_msg
