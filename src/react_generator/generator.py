from pathlib import Path

from react_generator import templates
from react_generator.naming import format_name
from react_generator.specs import SPECS, GeneratorSpec, FileTemplate
from react_generator.console import Colors, paint


class Generator:
    def __init__(self, src_path: Path | None = None):
        self.src_path = src_path or Path("src")

    def create_file(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _resolve_files(self, spec: GeneratorSpec, flags) -> tuple[FileTemplate, ...]:
        """Applique les overrides de template pour les flags actifs.
        Sans flag concerné, renvoie les fichiers du spec inchangés."""
        override = {}
        for flag in flags:
            override.update(spec.overrides.get(flag, {}))
        if not override:
            return spec.files
        return tuple(FileTemplate(f.extension, override.get(f.extension, f.template))
                     for f in spec.files)

    def _barrel_content(self, spec: GeneratorSpec, formatted: str) -> str:
        lines = [
            f"export {{ default }} from './{formatted}';" if spec.default_export
            else f"export * from './{formatted}';"
        ]
        if any(f.extension == ".types.ts" for f in spec.files):
            lines.append(f"export * from './{formatted}.types';")
        return "\n".join(lines) + "\n"

    def _planned_paths(self, files, spec: GeneratorSpec, target_dir: Path, formatted: str):
        paths = [(target_dir / f"{formatted}{f.extension}", f.template) for f in files]
        if spec.creates_folder:
            paths.append((target_dir / "index.ts", None))
        return paths

    def generate(self, kind: str, path: str, name: str,
                 dry_run: bool = False, flags=()) -> bool:
        spec = SPECS[kind]
        formatted, pascal, camel = format_name(name, kind)
        files = self._resolve_files(spec, flags)

        target_dir = self.src_path / path if path else self.src_path
        if spec.creates_folder:
            target_dir = target_dir / formatted

        planned = self._planned_paths(files, spec, target_dir, formatted)

        existing = [p for p, _ in planned if p.exists()]
        if existing:
            for p in existing:
                print(paint(f"✗ existe déjà : {p.as_posix()}", Colors.RED))
            return False

        written = []
        pending = []
        for file_path, template in planned:
            if template is None:
                content = self._barrel_content(spec, formatted)
            else:
                content = templates.render(template, name=formatted, pascal=pascal, camel=camel)
            pending.append((file_path, content))

        if not dry_run:
            for file_path, content in pending:
                self.create_file(file_path, content)
            written = [p for p, _ in pending]
        else:
            written = [p for p, _ in pending]

        self._report(kind, written, dry_run)
        return True

    def _report(self, kind: str, paths: list[Path], dry_run: bool) -> None:
        if dry_run:
            print(paint(f"[dry-run] {kind} :", Colors.YELLOW))
            label = "DRY"
        else:
            print(paint(f"✓ {kind} généré :", Colors.GREEN))
            label = "CREATE"
        for p in paths:
            print(f"  {label} {p.as_posix()}")