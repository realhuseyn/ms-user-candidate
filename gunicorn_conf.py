import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

# Gunicorn config variables
loglevel = use_loglevel
workers = 1
bind = use_bind
keepalive = 120
errorlog = "-"
bind = f"{host}:{port}"