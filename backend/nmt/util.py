import torch
from typing import Iterable


def device_check(device):
    if not torch.cuda.is_available() or device < 0:
        return "cpu"
    device_count = torch.cuda.device_count()
    if device >= device_count:
        device = device_count - 1
    return torch.device(device)


def parseLang(lang):
    assert isinstance(lang, str)
    langs = lang.split("-")
    assert len(langs) == 2
    return langs


def parseLangInfo(langInfo):

    assert langInfo
    if isinstance(langInfo, str):
        return [parseLang(langInfo)]
    elif isinstance(langInfo, Iterable):
        return [parseLang(lang) for lang in langInfo]
    else:
        raise Exception("config format wrong")
