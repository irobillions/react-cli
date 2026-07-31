import pytest

from react_generator.generator import Generator


@pytest.fixture
def gen(tmp_path):
    return Generator(src_path=tmp_path / "src")


def test_service_default_is_functional(gen, tmp_path):
    gen.generate("service", "api", "data")
    ts = (tmp_path / "src" / "api" / "DataService.ts").read_text(encoding="utf-8")
    assert "function" in ts
    assert "class" not in ts


def test_service_singleton_flag_uses_class(gen, tmp_path):
    gen.generate("service", "api", "data", flags=("singleton",))
    ts = (tmp_path / "src" / "api" / "DataService.ts").read_text(encoding="utf-8")
    assert "class DataService" in ts


def test_singleton_flag_ignored_for_other_kinds(gen, tmp_path):
    assert gen.generate("component", "", "button", flags=("singleton",)) is True
    assert (tmp_path / "src" / "Button" / "Button.tsx").exists()