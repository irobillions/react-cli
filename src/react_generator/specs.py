from dataclasses import dataclass, field

from react_generator import templates as t


@dataclass(frozen=True)
class FileTemplate:
    extension: str
    template: str


@dataclass(frozen=True)
class GeneratorSpec:
    files: tuple[FileTemplate, ...]
    creates_folder: bool = False
    default_export: bool = False
    # overrides[flag] = {extension: template_alternatif}
    overrides: dict = field(default_factory=dict)


SPECS: dict[str, GeneratorSpec] = {
    "component": GeneratorSpec(
        creates_folder=True,
        default_export=True,
        files=(
            FileTemplate(".tsx", t.COMPONENT_TSX),
            FileTemplate(".module.scss", t.COMPONENT_SCSS),
            FileTemplate(".test.tsx", t.COMPONENT_TEST),
            FileTemplate(".types.ts", t.COMPONENT_TYPES),
        ),
    ),
    "service": GeneratorSpec(
        files=(
            FileTemplate(".ts", t.SERVICE_FUNCTIONAL_TS),   # défaut = fonctions
            FileTemplate(".test.ts", t.SERVICE_TEST),
        ),
        overrides={"singleton": {".ts": t.SERVICE_TS}},     # --singleton = classe
    ),
    "hook": GeneratorSpec(files=(
        FileTemplate(".ts", t.HOOK_TS),
        FileTemplate(".test.ts", t.HOOK_TEST),
    )),
    "redux": GeneratorSpec(files=(
        FileTemplate(".ts", t.REDUX_TS),
        FileTemplate(".test.ts", t.REDUX_TEST),
    )),
    "context": GeneratorSpec(
        creates_folder=True,
        default_export=False,
        files=(
            FileTemplate(".tsx", t.CONTEXT_TSX),
            FileTemplate(".types.ts", t.CONTEXT_TYPES),
            FileTemplate(".test.tsx", t.CONTEXT_TEST),
        ),
    ),
}

ALIASES: dict[str, str] = {
    "c": "component", "s": "service", "h": "hook", "r": "redux", "ctx": "context",
}


def resolve_kind(raw: str) -> str:
    kind = ALIASES.get(raw, raw)
    if kind not in SPECS:
        raise KeyError(kind)
    return kind