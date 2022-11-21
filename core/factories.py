import os

envsettings = os.getenv("settings")

if envsettings in ["dev", "local"]:
    from core.settings.devsettings import DevSettings
    settings = DevSettings()

elif envsettings in ["prod", "default"]:
    from core.settings.prodsettings import ProdSettings
    settings = ProdSettings()
else:
    raise SystemExit(
        "settings for app not exported. example:  ```export settings=dev```")
