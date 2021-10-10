from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_env(env, fallback) -> str:
  env=getenv(env)

  if env is None:
    return fallback

  return env


GITHUB_TOKEN=get_env('GITHUB_TOKEN', None)
TARGET_USER=get_env('TARGET_USER', 'marcelovicentegc')