"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os
import yaml
from copy import deepcopy
from typing import Iterable
import pandas as pd
from . import app
from ..nmt import parseLang


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def model_info(config: dict):
    models_info = []
    for model in config:
        langs = model["lang"]
        if isinstance(langs, str):
            modelInfo = deepcopy(model)
            modelInfo["src"], modelInfo["tgt"] = parseLang(langs)
            models_info.append(modelInfo)
        elif isinstance(langs, Iterable):
            for lang in langs:
                modelInfo = deepcopy(model)
                modelInfo["lang"] = lang
                modelInfo["src"], modelInfo["tgt"] = parseLang(lang)
                models_info.append(modelInfo)
    return pd.DataFrame(models_info).drop_duplicates()


def dir_checker(path):
    if not os.path.isdir(path):
        raise Exception("directory not found: {}".format(path))


def file_checker(path):
    if not os.path.isfile(path):
        raise Exception("file not found: {}".format(path))


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv("FLASK_SECRET", "Secret")

    APP_DIR = os.path.dirname(__file__)
    BACKEND_DIR = os.path.dirname(APP_DIR)
    ROOT_DIR = os.path.dirname(BACKEND_DIR)
    FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
    DIST_DIR = os.path.join(FRONTEND_DIR, "dist")
    dir_checker(DIST_DIR)
    
    NMT_DIR = os.path.join(BACKEND_DIR, "nmt")
    NMT_MODEL_DIR = os.path.join(NMT_DIR, "models")
    
    config_path = os.path.join(NMT_DIR, "config.yaml")
    file_checker(config_path)
    NMT_CONFIG = load_yaml(config_path)
    MODELS_CONFIG = model_info(NMT_CONFIG["models"])
    
    MODELS_PRELOAD = os.getenv("MODELS_PRELOAD", False)


app.config.from_object("backend.app.config.Config")
