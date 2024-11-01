import re


def test_cli(poetry):
    """Test if my poetry fixture is working."""

    result = poetry(
        "--version",
        "--no-ansi",
    )

    assert result.returncode == 0
    assert re.search(r"Poetry \(version \d+\.\d+\.\d+\)", result.stdout)
