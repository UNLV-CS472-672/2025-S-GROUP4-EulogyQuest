import os
import sys
import json
import pytest

PRS = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'Eulogy-Quest',
        'GPT',
        'Holliday-quest',
        'src',
        'perl'
    )
)
sys.path.insert(0, PRS)

import dialogue_loader as dl

@pytest.fixture(autouse=True)
def clear_npc_dialogues():
    """Ensure npc_dialogues is empty before & after each test."""
    dl.npc_dialogues.clear()
    yield
    dl.npc_dialogues.clear()


def test_sanitize_filename_basic():
    assert dl.sanitize_filename("John Doe") == "John.pl"


def test_sanitize_filename_special_chars():
    assert dl.sanitize_filename("Jane O'Connor") == "Jane.pl"


def test_strip_brackets_from_keys():
    inp = {'[hello]': 'world', 'plain': 'text'}
    expected = {'hello': 'world', 'plain': 'text'}
    assert dl.strip_brackets_from_keys(inp) == expected


@pytest.mark.parametrize("inp,expected", [
    ("[ClickMe]", '[" . quest::saylink("ClickMe") . "]'),
    ("NoBrackets", "NoBrackets"),
])
def test_convert_click_text(inp, expected):
    assert dl.convert_click_text(inp) == expected


def test_apply_click_conversion_to_dialogue():
    text = "Welcome [Here] and [There]!"
    out = dl.apply_click_conversion_to_dialogue(text)
    assert out.count('quest::saylink("Here")') == 1
    assert out.count('quest::saylink("There")') == 1


def test_load_quest_file_and_global(tmp_path):
    data = {
        "npc_scripting": [
            {
                "name": "Alice Smith",
                "dialogue": {"[greet]": "Hello", "[bye]": "Goodbye"}
            }
        ]
    }
    fp = tmp_path / "sample.json"
    fp.write_text(json.dumps(data))

    returned = dl.load_quest_file(str(fp))
    assert returned == data["npc_scripting"]
    assert dl.npc_dialogues == [{"greet": "Hello", "bye": "Goodbye"}]


def test_create_hailblock():
    hail_text = "[Salute]"
    block = dl.create_hailblock(hail_text)
    assert "if ($text=~/hail/i)" in block
    assert 'quest::say("Greetings $name!' in block
    assert 'quest::saylink("Salute")' in block


def test_create_event_say_blocks_first_npc():
    dialogue = {
        "hello": "Hi [User]",
        "offer": "Take this",
        "parting-text": "Bye [User]",
        "unused": "Ignore me"
    }
    blocks = dl.create_event_say_blocks(dialogue, is_first_npc=True)
    assert len(blocks) == 2
    blk = blocks[-1]
    assert 'quest::saylink("User")' in blk
    assert 'quest::say("Bye [' in blk
    assert blk.strip().endswith("}")


def test_create_event_say_blocks_subsequent_npc():
    dialogue = {
        "hail": "Greetings",
        "foo": "Bar",
        "baz": "Qux",
        "offer": "Give",
        "parting-text": "Later"
    }
    blocks = dl.create_event_say_blocks(dialogue, is_first_npc=False)
    assert len(blocks) == 2
    assert any("if ($text=~/hail/i)" in b for b in blocks)
    assert any('/foo/i' in b and 'Bar' in b for b in blocks)


def test_create_event_item_block_first_npc():
    dialogue = {"offer": "Please take", "extra": "ignored"}
    lines = dl.create_event_item_block(dialogue, is_first_npc=True)
    assert lines == ['    quest::say("Please take");']


def test_create_event_item_block_subsequent_npc():
    dialogue = {"a": "1", "b": "2", "c": "3", "offer": "X", "parting-text": "Y"}
    lines = dl.create_event_item_block(dialogue, is_first_npc=False)
    assert len(lines) == 3
    assert 'quest::say("3")' in lines[0]
    assert 'quest::say("X")' in lines[1]
    assert 'quest::say("Y")' in lines[2]


def test_create_perl_file(tmp_path, capsys):
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        say = ['    if ($text=~/hi/i) { quest::say("Hello"); }']
        item = ['    quest::say("Take");']
        dl.create_perl_file("Bob Builder", say, item)
        fname = "Bob.pl"
        assert (tmp_path / fname).is_file()
        content = (tmp_path / fname).read_text()
        assert "sub EVENT_SAY {" in content
        assert 'quest::say("Hello")' in content
        assert "sub EVENT_ITEM {" in content
        assert 'quest::say("Take")' in content
        captured = capsys.readouterr()
        assert "Perl file created: Bob.pl" in captured.out
    finally:
        os.chdir(old)


def test_main_usage_prints(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["dialogue_loader.py"])
    dl.main()
    out = capsys.readouterr().out
    assert "Usage: python dialogue_loader.py <json_path>" in out


def test_main_creates_perl_files(tmp_path, monkeypatch):
    data = {
        "npc_scripting": [
            {"name": "Charlie Brown", "dialogue": {"[hi]": "Hello"}},
            {"name": "Lucy Van Pelt", "dialogue": {"[hey]": "Hey"}}
        ]
    }
    json_file = tmp_path / "input.json"
    json_file.write_text(json.dumps(data))

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        monkeypatch.setattr(sys, "argv", ["dialogue_loader.py", str(json_file)])
        dl.main()
        assert (tmp_path / "Charlie.pl").is_file()
        assert (tmp_path / "Lucy.pl").is_file()
    finally:
        os.chdir(old_cwd)
