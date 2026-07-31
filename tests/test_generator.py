"""Characterization tests for Generator.

Ils verrouillent le comportement ACTUEL avant tout refactor (dry-run, etc.).
On teste le contrat observable — fichiers créés, contenu du barrel, atomicité —
pas les détails internes des templates (qui peuvent changer sans casser le contrat).
"""

import pytest

from react_generator.generator import Generator


@pytest.fixture
def gen(tmp_path):
    """Un Generator qui écrit dans un src/ jetable propre à chaque test."""
    return Generator(src_path=tmp_path / "src")


def _names(directory):
    return {p.name for p in directory.iterdir() if p.is_file()}


# --- component : dossier + barrel default export --------------------------

def test_component_creates_folder_with_all_files(gen, tmp_path):
    assert gen.generate("component", "ui", "button") is True
    folder = tmp_path / "src" / "ui" / "Button"
    assert _names(folder) == {
        "Button.tsx",
        "Button.module.scss",
        "Button.test.tsx",
        "Button.types.ts",
        "index.ts",
    }


def test_component_barrel_reexports_default_and_types(gen, tmp_path):
    gen.generate("component", "", "button")
    barrel = (tmp_path / "src" / "Button" / "index.ts").read_text(encoding="utf-8")
    assert "export { default } from './Button';" in barrel
    assert "export * from './Button.types';" in barrel


def test_component_content_is_substituted(gen, tmp_path):
    gen.generate("component", "", "button")
    tsx = (tmp_path / "src" / "Button" / "Button.tsx").read_text(encoding="utf-8")
    assert "Button" in tsx
    assert "__NAME__" not in tsx  # aucune sentinelle non substituée ne fuit


# --- context : dossier + barrel named export (pas de default) -------------

def test_context_folder_uses_formatted_name(gen, tmp_path):
    gen.generate("context", "", "user")
    folder = tmp_path / "src" / "UserContext"
    assert folder.is_dir()
    assert _names(folder) == {
        "UserContext.tsx",
        "UserContext.types.ts",
        "UserContext.test.tsx",
        "index.ts",
    }


def test_context_barrel_uses_star_not_default(gen, tmp_path):
    gen.generate("context", "", "user")
    barrel = (tmp_path / "src" / "UserContext" / "index.ts").read_text(encoding="utf-8")
    assert "export * from './UserContext';" in barrel
    assert "default" not in barrel


# --- flat types : pas de dossier, pas de barrel ---------------------------

def test_service_is_flat_no_barrel(gen, tmp_path):
    gen.generate("service", "api", "data")
    api = tmp_path / "src" / "api"
    assert _names(api) == {"DataService.ts", "DataService.test.ts"}
    assert not (api / "index.ts").exists()


def test_hook_is_flat_and_prefixed(gen, tmp_path):
    gen.generate("hook", "", "auth")
    src = tmp_path / "src"
    assert (src / "useAuth.ts").exists()
    assert (src / "useAuth.test.ts").exists()


def test_redux_slice_naming(gen, tmp_path):
    gen.generate("redux", "store", "counter")
    store = tmp_path / "src" / "store"
    assert _names(store) == {"counterSlice.ts", "counterSlice.test.ts"}


# --- atomicité : un conflit n'écrit RIEN ----------------------------------

def test_conflict_is_atomic(gen, tmp_path):
    assert gen.generate("component", "ui", "button") is True
    folder = tmp_path / "src" / "ui" / "Button"
    before = _names(folder)

    assert gen.generate("component", "ui", "button") is False
    assert _names(folder) == before  # inchangé


def test_partial_conflict_still_blocks_everything(gen, tmp_path):
    folder = tmp_path / "src" / "Button"
    folder.mkdir(parents=True)
    (folder / "Button.types.ts").write_text("SENTINEL", encoding="utf-8")

    assert gen.generate("component", "", "button") is False
    assert (folder / "Button.types.ts").read_text(encoding="utf-8") == "SENTINEL"
    assert _names(folder) == {"Button.types.ts"}