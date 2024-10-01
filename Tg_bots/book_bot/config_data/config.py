from environs  import Env
from dataclasses import dataclass

@dataclass
class TgBot:
      token:str

@dataclass
class Config:
      tgbot:TgBot


def load_config(path:str=None):
      env =  Env()
      env.read_env(path)

      return Config(tgbot=TgBot(token=env('BOT_TOKEN')))