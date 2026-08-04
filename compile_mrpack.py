#!/usr/bin/env python
import json
import pathlib
import sys
import tempfile
import zipfile


def main() -> int:
    script_dir = pathlib.Path(__file__).resolve().parent
    index_file = script_dir / "mastery.modrinth.index.json"
    overrides_dir = script_dir / "overrides"
    output_file = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else script_dir / "mastery-1.0.0.mrpack"

    if not index_file.is_file():
        raise SystemExit(f"Missing index file: {index_file}")

    with index_file.open("r", encoding="utf-8") as handle:
        json.load(handle)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    seen = {"modrinth.index.json"}

    with tempfile.NamedTemporaryFile(
        dir=output_file.parent,
        prefix=f".{output_file.name}.",
        suffix=".tmp",
        delete=False,
    ) as temp_handle:
        temp_path = pathlib.Path(temp_handle.name)

    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            archive.write(index_file, "modrinth.index.json")

            if overrides_dir.exists():
                for path in sorted(overrides_dir.rglob("*")):
                    if not path.is_file():
                        continue

                    archive_name = path.relative_to(script_dir).as_posix()
                    if archive_name in seen:
                        raise SystemExit(f"Duplicate archive path: {archive_name}")

                    seen.add(archive_name)
                    archive.write(path, archive_name)

        temp_path.replace(output_file)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

    print(f"Wrote {output_file}")
    print(f"Archive entries: {len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
