import os
import time
import torch
from copy import deepcopy
from ..nmt import HFNlpModel
from . import app, MODELS


def timer(func):
    def func_in():
        start_time = time.time()
        res = func()
        end_time = time.time()
        print("Inference coasts: {:.0f}ms".format((end_time - start_time) * 1000))
        return res

    return func_in


def get_model(config, device=-1):# build nmt model
    if isinstance(config, dict):
        pass
    elif isinstance(config, str):
        config = get_model_config(config)
    else:
        raise Exception("wrong config type")
    if not config["name"] in MODELS.keys():
        conf = deepcopy(config)
        conf["path"] = os.path.join(app.config["NMT_MODEL_DIR"], conf["path"])
        if config["type"] == "huggingface":
            MODELS[config["name"]] = HFNlpModel(conf, device)
        else:
            raise Exception("unsupported model type")
    return MODELS[config["name"]]


def model_filter(src="", tgt="", model=""):
    result = app.config["MODELS_CONFIG"]
    if src:
        result = result[result["src"] == src]
    if tgt:
        result = result[result["tgt"] == tgt]
    if model:
        result = result[result["name"] == model]
    return result


def get_model_config(name):
    for conf in app.config["NMT_CONFIG"]["models"]:
        if conf["name"] == name:
            return conf


def get_avilable_device():
    device = {"cpu": -1}
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            device["cuda:%d" % i] = {"id": i, "ram": device_avilable_ram(i)}
    return device


def device_avilable_ram(idx=0):
    if not torch.cuda.is_available() or idx >= torch.cuda.device_count():
        return 0
    total_memory = torch.cuda.get_device_properties(idx).total_memory
    used_memory = torch.cuda.memory_allocated(idx)
    free_memory = total_memory - used_memory  # 剩余显存(GB)
    return free_memory


def choose_device(device):
    device_count = torch.cuda.device_count()
    if isinstance(device, str):
        if not device.isdigit():
            if device == "gpu" or device == "cuda":
                largert_ram = 0
                for i in range(device_count):
                    ram = device_avilable_ram(i)
                    if ram > largert_ram:
                        device = i
                        largert_ram = ram
            else:
                device = -1
        else:
            device = int(device)
    if device >= device_count:
        device = device_count - 1
    if device < 0:
        device = -1
    return device
