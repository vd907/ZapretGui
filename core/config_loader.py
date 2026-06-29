# core/config_loader.py
from pathlib import Path
import tomllib


class ConfigLoader:

    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    CONFIG_DIR = ASSETS_DIR / "config"
    STYLES_DIR = ASSETS_DIR / "styles"
    ICONS_DIR = ASSETS_DIR / "icons"

    CONFIG_PATH = CONFIG_DIR / "config.toml"
    QSS_PATH = STYLES_DIR / "style.qss"
    TEXTS_PATH = CONFIG_DIR / "texts.toml"

    _config = None
    _qss = None
    _texts = None

    @classmethod
    def config(cls) -> dict:
        if cls._config is None:
            path = cls.CONFIG_PATH
            cls._config = tomllib.loads(path.read_text("utf-8")) if path.exists() else {}
        return cls._config

    @classmethod
    def texts(cls) -> dict:
        if cls._texts is None:
            path = cls.TEXTS_PATH
            cls._texts = tomllib.loads(path.read_text("utf-8")) if path.exists() else {}
        return cls._texts

    @classmethod
    def get_text(cls, *keys):
        value = cls.texts()
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            else:
                return None
        return value if value != {} else None

    @classmethod
    def get(cls, *keys):
        value = cls.config()
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            else:
                return None
        scale = cls.config().get("scale", {}).get("factor", 1.0)
        if isinstance(value, (int, float)) and keys[-1] != "factor":
            return int(value * scale)
        return value if value != {} else None

    @classmethod
    def qss(cls) -> str:
        if cls._qss is None:
            path = cls.QSS_PATH
            cls._qss = path.read_text("utf-8") if path.exists() else ""
        return cls._qss