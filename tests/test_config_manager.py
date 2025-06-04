import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.configmanager import ConfigManager

def test_get_style_from_file(tmp_path):
    cfg_path = tmp_path / "conf.json"
    with cfg_path.open("w", encoding="utf-8") as f:
        json.dump({"style": "Világos"}, f)

    cm = ConfigManager(str(cfg_path))
    cm.load_config()
    assert cm.get_style() == "Világos"


def test_get_style_default_when_missing(tmp_path):
    cfg_path = tmp_path / "conf.json"
    with cfg_path.open("w", encoding="utf-8") as f:
        json.dump({}, f)

    cm = ConfigManager(str(cfg_path))
    cm.load_config()
    assert cm.get_style() == "Sötét"
