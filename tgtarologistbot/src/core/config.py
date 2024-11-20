from configparser import ConfigParser

TORTOISE_ORM = {
    "connections": {"default": "sqlite://data/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["tgtarologistbot.src.app.database.models"],
            "default_connection": "default",
        },
    },
}


class Config:
    SECTION = "DEFAULT"

    config = ConfigParser()
    config.read("data/config.ini")

    bot_token = config.get(SECTION, "bot_token")
    admin_tg_id = config.get(SECTION, "admin_tg_id")

    open_ai_api_key = config.get(SECTION, "open_ai_api_key")
    open_ai_model = config.get(SECTION, "open_ai_model")
    open_ai_max_tokens = config.get(SECTION, "open_ai_max_tokens")
    open_ai_temperature = config.get(SECTION, "open_ai_temperature")
