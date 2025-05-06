import os
import sys
import subprocess
import importlib.util
from pathlib import Path
import pytest

repo_root   = Path(__file__).parent.parent
gpt_dir     = repo_root / "Eulogy-Quest" / "GPT"
module_path = gpt_dir / "updateNPCs.py"

if not module_path.is_file():
    raise FileNotFoundError(f"Cannot find updateNPCs.py at {module_path}")

spec = importlib.util.spec_from_file_location("updateNPCs", str(module_path))
updateNPCs = importlib.util.module_from_spec(spec)
sys.modules["updateNPCs"] = updateNPCs
spec.loader.exec_module(updateNPCs)


def test_extract_names_by_file_suffix(tmp_path):
    d = tmp_path / "build" / "quest"
    d.mkdir(parents=True)
    (d / "foo_target.txt").write_text("Alice\n")
    (d / "bar_item.txt").write_text("Bob\n")
    targets = updateNPCs.extract_names_by_file_suffix(str(d), "_target")
    items   = updateNPCs.extract_names_by_file_suffix(str(d), "_item")
    assert targets == ["Alice"]
    assert items   == ["Bob"]


def test_stream_sql_to_mariadb(monkeypatch):
    calls = []
    def fake_run(cmd, input=None):
        calls.append((cmd, input))
        class R: pass
        return R()
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setenv("MARIADB_ROOT_PASSWORD", "pw")
    monkeypatch.setenv("MARIADB_DATABASE", "db")
    sql = "SELECT 1;"
    updateNPCs.stream_sql_to_mariadb(sql)
    assert len(calls) == 1, "expected one call to subprocess.run"
    cmd, data = calls[0]
    assert any(part == "mysql" for part in cmd), f"'mysql' not found in {cmd}"
    assert data == b"SELECT 1;", "SQL was not passed correctly"


def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setenv("MARIADB_ROOT_PASSWORD", "pw")
    monkeypatch.setenv("MARIADB_DATABASE", "db")
    monkeypatch.setenv("DB_USER", "user")

    monkeypatch.setattr(sys, "argv", ["prog"])
    result = updateNPCs.main()

    captured = capsys.readouterr()
    assert "Usage: python3 updateNPCs.py <quest_name>" in captured.out
    assert result is None


def test_main_with_files(monkeypatch):
    monkeypatch.setattr(
        updateNPCs,
        "extract_names_by_file_suffix",
        lambda path, suffix: ["NPCONE"] if suffix == "_target" else ["ITEMONE"]
    )
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, input=None: calls.append((cmd, input)))
    monkeypatch.setenv("MARIADB_ROOT_PASSWORD", "pw")
    monkeypatch.setenv("MARIADB_DATABASE", "db")
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setattr(updateNPCs, "__file__", str(Path("/no/real/path/updateNPCs.py")))
    monkeypatch.setattr(sys, "argv", ["prog", "doesntmatter"])
    updateNPCs.main()
    assert any(
        b"REPLACE" in payload or b"INSERT" in payload
        for _, payload in calls
    ), "No REPLACE/INSERT seen"
    assert any(
        b"UPDATE spawnentry" in payload
        for _, payload in calls
    ), "No UPDATE spawnentry seen"
