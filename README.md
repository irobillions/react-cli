# react-generator

An Angular-CLI-style schematic generator for React. Scaffold components,
services, hooks, Redux slices, and contexts from the command line — with
consistent naming, colocated tests, and barrel exports.

```bash
react-gen g c ui/Button
```

```
✓ component généré :
  CREATE src/ui/Button/Button.tsx
  CREATE src/ui/Button/Button.module.scss
  CREATE src/ui/Button/Button.test.tsx
  CREATE src/ui/Button/Button.types.ts
  CREATE src/ui/Button/index.ts
```

## Installation

Requires Python 3.10+.

### Global use (recommended)

Install with [`pipx`](https://pipx.pypa.io/) so the `react-gen` command is
available from any directory, isolated from your other Python packages:

```bash
pipx install --editable .
```

On Windows, install `pipx` first if you don't have it:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Close and reopen your terminal after `ensurepath` so the updated `PATH` is
loaded.

### Local / development install

From the project root, inside your virtual environment:

```bash
pip install -e .
```

## Usage

```
react-gen generate <kind> <path/name> [options]
react-gen g <kind> <path/name> [options]
```

`g` is an alias for `generate`. The last segment of `<path/name>` is the schematic
name; everything before it is the directory under `src/`.

### Schematic kinds

| Kind        | Alias | Output                                              | Folder |
| ----------- | ----- | --------------------------------------------------- | ------ |
| `component` | `c`   | `.tsx`, `.module.scss`, `.test.tsx`, `.types.ts`    | Yes    |
| `context`   | `ctx` | `.tsx`, `.types.ts`, `.test.tsx`                     | Yes    |
| `service`   | `s`   | `.ts`, `.test.ts`                                    | No     |
| `hook`      | `h`   | `.ts`, `.test.ts`                                    | No     |
| `redux`     | `r`   | `.ts`, `.test.ts`                                    | No     |

`component` and `context` each generate their own folder plus a barrel
`index.ts`. The other kinds are flat files placed directly in the target
directory.

### Options

| Option        | Description                                                        |
| ------------- | ----------------------------------------------------------------- |
| `--dry-run`   | Preview the files that would be created without writing anything.  |
| `--singleton` | Generate a service as a singleton class instead of plain functions.|
| `--path DIR`  | Override the directory derived from `<path/name>`.                 |

## Naming

Names are normalized automatically, so you can pass any casing and the correct
convention is applied per kind:

| Kind        | Input           | Result             |
| ----------- | --------------- | ------------------ |
| `component` | `user-profile`  | `UserProfile`      |
| `service`   | `data`          | `DataService`      |
| `hook`      | `auth`          | `useAuth`          |
| `redux`     | `counter`       | `counterSlice`     |
| `context`   | `user`          | `UserContext`      |

Redundant prefixes/suffixes you type yourself are stripped to avoid duplication
(`useCounter` → `useCounter`, not `useuseCounter`; `DataService` → `DataService`,
not `DataServiceService`). Digits are preserved (`Button2` stays `Button2`).

## Examples

```bash
# Component in src/ui/Button/ with a barrel export
react-gen g c ui/Button

# Hook: src/hooks/useAuth.ts + test
react-gen g h hooks/useAuth

# Redux slice: src/store/counterSlice.ts + test
react-gen g r store/counter

# Context: src/context/UserContext/ with a barrel export
react-gen g ctx context/User

# Service as plain functions (default)
react-gen g s api/Data

# Service as a singleton class
react-gen g s api/Data --singleton

# Preview without writing to disk
react-gen g c ui/Modal --dry-run
```

## How it works

Each schematic kind is declared as data in a single registry (`SPECS`): its file
templates, whether it creates a folder, whether its barrel re-exports a default,
and any flag-driven template overrides. The generator itself is generic — it
reads the spec and writes files, with no per-kind branching. Adding a new kind is
one entry in the registry; adding a new flag (like `--singleton`) is one override
entry, with no change to the generator.

Generation is atomic: if any target file already exists, nothing is written and
the command reports the conflicts. You never end up with a half-created schematic.

## Development

```bash
# Run the test suite
pytest

# Format and lint
ruff format .
ruff check --fix .
```

The project uses a `src/` layout, so tests run against the installed package.
Run `pip install -e .` once before testing.

## License

MIT © Christ Bouka