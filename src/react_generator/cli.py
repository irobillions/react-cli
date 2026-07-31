import argparse
import sys

from react_generator.generator import Generator
from react_generator.specs import resolve_kind, SPECS
from react_generator.console import Colors, paint


def split_path_name(path_name: str) -> tuple[str, str]:
    """'components/ui/Button' -> ('components/ui', 'Button')."""
    parts = path_name.strip("/").split("/")
    name = parts[-1]
    path = "/".join(parts[:-1])
    return path, name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="react-gen",
        description="Angular-CLI-style schematic generator for React.",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    gen = sub.add_parser("generate", aliases=["g"], help="Generate a schematic.")
    gen.add_argument(
        "kind",
        help="component|service|hook|redux|context (aliases: c|s|h|r|ctx)",
    )
    gen.add_argument("path_name", help="Path + name, e.g. components/ui/Button")
    gen.add_argument("--path", help="Override the directory derived from path_name.")
    gen.add_argument("--dry-run", action="store_true", help="Preview the files without writing anything.")
    gen.add_argument("--singleton", action="store_true",
                     help="Generate a service as a singleton class instead of functions.")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        kind = resolve_kind(args.kind)
    except KeyError:
        valid = ", ".join(sorted(SPECS))
        print(paint(f"✗ type inconnu : {args.kind!r}. Valides : {valid}", Colors.RED))
        return 2

    path, name = split_path_name(args.path_name)
    if args.path:
        path = args.path
    if not name:
        print(paint("✗ nom de schematic manquant", Colors.RED))
        return 2

    flags = tuple(f for f in ("singleton",) if getattr(args, f, False))
    ok = Generator().generate(kind, path, name, dry_run=args.dry_run, flags=flags)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
