"""RPM packaging checks use temporary files; they never build the application."""

from pathlib import Path
import tarfile
import tempfile
import unittest

from build_rpm import collect, read_version, write_spec, write_tarball


class BuildRpmTests(unittest.TestCase):
    def test_tarball_keeps_executable_and_assets_next_to_each_other(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "bundle/netease-music-gpui"
            (bundle / "assets/icons").mkdir(parents=True)
            (bundle / "assets/icons/logo.svg").write_bytes(b"icon")
            executable = bundle / "netease-music-gpui"
            executable.write_bytes(b"executable")
            executable.chmod(0o755)
            version = read_version()
            payload = collect(bundle, version)
            archive = root / f"netease-music-gpui-{version}.tar.gz"
            write_tarball(payload, version, archive)
            with tarfile.open(archive) as packed:
                names = packed.getnames()
                prefix = f"netease-music-gpui-{version}"
                self.assertIn(f"{prefix}/netease-music-gpui", names)
                self.assertIn(f"{prefix}/assets/icons/logo.svg", names)
                self.assertIn(f"{prefix}/netease-music-gpui.desktop", names)
                self.assertIn(f"{prefix}/netease-music-gpui-128.png", names)
                self.assertIn(f"{prefix}/netease-music-gpui-256.png", names)
                member = packed.getmember(f"{prefix}/netease-music-gpui")
                self.assertTrue(member.mode & 0o111)

    def test_missing_assets_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "bundle/netease-music-gpui"
            bundle.mkdir(parents=True)
            (bundle / "netease-music-gpui").write_bytes(b"executable")
            with self.assertRaises(SystemExit):
                collect(bundle, read_version())

    def test_spec_version_follows_cargo_toml(self):
        with tempfile.TemporaryDirectory() as temporary:
            spec = Path(temporary) / "netease-music-gpui.spec"
            write_spec("9.9.9", spec)
            text = spec.read_text(encoding="utf-8")
            self.assertIn("Version:        9.9.9", text)
            self.assertNotIn(f"Version:        {read_version()}", text)


if __name__ == "__main__":
    unittest.main()
