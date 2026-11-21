"""Build an RPM package from an already built Linux bundle.

The Rust build is not repeated here: `scripts/package.py` produces
`target/bundle/netease-music-gpui/` (executable plus the `assets/` directory
the app resolves relative to the executable), and this script packs that
bundle together with the desktop entry and the icons into a source tarball,
then lets rpmbuild turn it into a binary RPM.

Usage:

    python3 scripts/build_rpm.py                     # target/bundle -> dist/
    python3 scripts/build_rpm.py --bundle <dir> --output-dir <dir>

Requires `rpmbuild` (Fedora: `dnf install rpm-build`, Ubuntu: `apt install rpm`).
"""

import argparse
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "packaging/rpm/netease-music-gpui.spec"
DESKTOP = ROOT / "packaging/linux/netease-music-gpui.desktop"
ICONS = ROOT / "packaging/linux/icons"


def read_version():
    with (ROOT / "Cargo.toml").open("rb") as file:
        return tomllib.load(file)["package"]["version"]


def collect(bundle, version):
    """Return the payload of the source tarball as {relative path: source path}."""
    executable = bundle / "netease-music-gpui"
    assets = bundle / "assets"
    if not executable.is_file():
        raise SystemExit(f"Missing executable: {executable}")
    if not assets.is_dir():
        raise SystemExit(f"Missing assets directory: {assets}")
    payload = {
        "netease-music-gpui": executable,
        "netease-music-gpui.desktop": DESKTOP,
        "netease-music-gpui-128.png": ICONS / "netease-music-gpui-128.png",
        "netease-music-gpui-256.png": ICONS / "netease-music-gpui-256.png",
        "LICENSE": ROOT / "LICENSE",
        "README.md": ROOT / "README.md",
    }
    for path in payload.values():
        if not path.is_file():
            raise SystemExit(f"Missing packaging input: {path}")
    payload["assets"] = assets
    return payload


def write_tarball(payload, version, destination):
    """Write the source tarball; the top directory matches %setup -n."""
    prefix = f"netease-music-gpui-{version}"
    with tarfile.open(destination, "w:gz") as archive:
        for name, source in sorted(payload.items()):
            archive.add(source, arcname=f"{prefix}/{name}")


def write_spec(version, destination):
    """Copy the spec and align its Version with Cargo.toml."""
    text = SPEC.read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines():
        if line.startswith("Version:"):
            line = f"Version:        {version}"
        lines.append(line)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(bundle, output_dir):
    version = read_version()
    payload = collect(bundle, version)
    with tempfile.TemporaryDirectory(prefix="netease-music-gpui-rpm-") as temporary:
        topdir = Path(temporary) / "rpmbuild"
        for name in ("SOURCES", "SPECS", "BUILD", "RPMS", "SRPMS"):
            (topdir / name).mkdir(parents=True)
        tarball = topdir / "SOURCES" / f"netease-music-gpui-{version}.tar.gz"
        write_tarball(payload, version, tarball)
        spec = topdir / "SPECS" / "netease-music-gpui.spec"
        write_spec(version, spec)
        subprocess.run([
            "rpmbuild", "-ba",
            "--define", f"_topdir {topdir}",
            str(spec),
        ], check=True)
        built = sorted((topdir / "RPMS").rglob("*.rpm"))
        if not built:
            raise SystemExit("rpmbuild produced no RPM")
        output_dir.mkdir(parents=True, exist_ok=True)
        for rpm in built:
            target = output_dir / rpm.name
            shutil.copy2(rpm, target)
            print(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=ROOT / "target/bundle/netease-music-gpui",
                        help="Directory produced by scripts/package.py on Linux")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist",
                        help="Directory the RPM is copied to")
    args = parser.parse_args()
    if shutil.which("rpmbuild") is None:
        raise SystemExit("rpmbuild not found: install rpm-build (Fedora) or rpm (Ubuntu)")
    build(args.bundle.resolve(), args.output_dir.resolve())


if __name__ == "__main__":
    main()
