import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GIT_BASH_CANDIDATES = [
    "C:\\Program Files\\Git\\bin\\bash.exe",
    "C:\\Program Files\\Git\\usr\\bin\\bash.exe",
    "bash",
]


def find_bash():
    for candidate in GIT_BASH_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return "bash"


class HookScriptTests(unittest.TestCase):
    def run_cmd(self, cmd, home):
        env = os.environ.copy()
        env["HOME"] = home.as_posix()
        env["USERPROFILE"] = str(home)
        env["CLAUDE_CONFIG_DIR"] = f"{home.as_posix()}/.claude"
        return subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )

    def test_install_upgrades_old_two_file_install(self):
        with tempfile.TemporaryDirectory(prefix="gon-hooks-upgrade-") as tmp:
            home = Path(tmp)
            hooks_dir = home / ".claude" / "hooks"
            hooks_dir.mkdir(parents=True)
            (home / ".claude" / "settings.json").write_text("{}\n", encoding="utf-8")
            (hooks_dir / "gon-activate.js").write_text("")
            (hooks_dir / "gon-mode-tracker.js").write_text("")

            self.run_cmd([find_bash(), "hooks/install.sh"], home)

            statusline = hooks_dir / "gon-statusline.sh"
            self.assertTrue(statusline.exists())
            settings = json.loads((home / ".claude" / "settings.json").read_text(encoding="utf-8"))
            self.assertIn("statusLine", settings)
            self.assertIn(statusline.as_posix(), settings["statusLine"]["command"])

    def test_install_reconfigures_missing_statusline(self):
        with tempfile.TemporaryDirectory(prefix="gon-hooks-statusline-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            hooks_dir = claude_dir / "hooks"
            hooks_dir.mkdir(parents=True)

            for name in ("gon-activate.js", "gon-mode-tracker.js", "gon-statusline.sh"):
                (hooks_dir / name).write_text("")

            settings = {
                "hooks": {
                    "SessionStart": [{"hooks": [{"type": "command", "command": f'node "{hooks_dir / "gon-activate.js"}"'}]}],
                    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": f'node "{hooks_dir / "gon-mode-tracker.js"}"'}]}],
                }
            }
            (claude_dir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
            result = self.run_cmd([find_bash(), "hooks/install.sh"], home)
            self.assertNotIn("Nothing to do", result.stdout)
            updated = json.loads((claude_dir / "settings.json").read_text(encoding="utf-8"))
            self.assertIn((hooks_dir / "gon-statusline.sh").as_posix(), updated["statusLine"]["command"])

    def test_uninstall_preserves_custom_statusline(self):
        with tempfile.TemporaryDirectory(prefix="gon-hooks-uninstall-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            hooks_dir = claude_dir / "hooks"
            hooks_dir.mkdir(parents=True)

            for name in ("gon-activate.js", "gon-mode-tracker.js", "gon-statusline.sh"):
                (hooks_dir / name).write_text("")

            settings = {
                "statusLine": {"type": "command", "command": "bash /tmp/custom-status-with-gon.sh"},
                "hooks": {
                    "SessionStart": [{"hooks": [{"type": "command", "command": f'node "{hooks_dir / "gon-activate.js"}"'}]}],
                    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": f'node "{hooks_dir / "gon-mode-tracker.js"}"'}]}],
                },
            }
            (claude_dir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
            self.run_cmd([find_bash(), "hooks/uninstall.sh"], home)
            updated = json.loads((claude_dir / "settings.json").read_text(encoding="utf-8"))
            self.assertEqual(updated["statusLine"]["command"], "bash /tmp/custom-status-with-gon.sh")
            self.assertNotIn("hooks", updated)

    def test_activate_does_not_nudge_when_custom_statusline_exists(self):
        with tempfile.TemporaryDirectory(prefix="gon-hooks-activate-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)
            (claude_dir / "settings.json").write_text(
                json.dumps({"statusLine": {"type": "command", "command": "bash /tmp/my-statusline.sh"}}) + "\n",
                encoding="utf-8",
            )
            result = self.run_cmd(["node", "hooks/gon-activate.js"], home)
            self.assertNotIn("STATUSLINE SETUP NEEDED", result.stdout)
            self.assertEqual((claude_dir / ".gon-active").read_text(), "full")


if __name__ == "__main__":
    unittest.main()
