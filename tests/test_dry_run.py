import pytest

from react_generator.generator import Generator


@pytest.fixture
def gen(tmp_path):
    return Generator(src_path=tmp_path / "src")


def test_dry_run_writes_nothing(gen, tmp_path):
    assert gen.generate("component", "ui", "button", dry_run=True) is True
    assert not (tmp_path / "src").exists()   # aucun octet sur le disque


def test_dry_run_then_real_still_writes(gen, tmp_path):
    gen.generate("component", "ui", "button", dry_run=True)      # preview : rien écrit
    assert gen.generate("component", "ui", "button") is True     # vrai run : doit réussir
    assert (tmp_path / "src" / "ui" / "Button" / "Button.tsx").exists()


def test_dry_run_reports_paths(gen, tmp_path, capsys):
    gen.generate("component", "", "button", dry_run=True)
    out = capsys.readouterr().out
    assert "dry-run" in out and "DRY" in out and "Button.tsx" in out