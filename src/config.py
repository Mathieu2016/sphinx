from pydantic import BaseModel


class SphinxConfig:
    open_ai_key: str = ''
    open_ai_proxy: str = 'http://127.0.0.1:15732'
