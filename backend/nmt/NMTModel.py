from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import traceback
from .util import device_check, parseLangInfo


class HFNlpModel:

    def __init__(self, conf: dict, device: int = -1, thread: int = 1):
        try:
            self.langs = parseLangInfo(conf["lang"])
            self.device = device_check(device)
            self.translator = {}
            self.tokenizer = AutoTokenizer.from_pretrained(conf["path"])
            self.model = (
                AutoModelForSeq2SeqLM.from_pretrained(conf["path"])
                .to(self.device)
                .eval()
            )
            self.maxStep = conf["max-length"]
        except:
            traceback.print_exc()

    def __call__(self, input: str, skip_special_tokens=True, src="", tgt=""):
        if len(self.langs) > 1:
            if src and tgt:
                if "{src}-{tgt}" not in self.translator.keys():
                    self.translator["{src}-{tgt}"] = pipeline(
                        "translation",
                        model=self.model,
                        tokenizer=self.tokenizer,
                        src_lang=src,
                        tgt_lang=tgt,
                        max_length=512,
                    )
                return self.translator["{src}-{tgt}"](input)[0]['translation_text']
            else:
                return ""
        else:
            # multi_language method in not implemented yet

            batch = self.tokenizer(input, return_tensors="pt")
            # allowed size of 512
            batch["input_ids"] = batch["input_ids"][:, : self.maxStep].to(self.device)
            batch["attention_mask"] = batch["attention_mask"][:, : self.maxStep].to(
                self.device
            )

            # Perform the translation and decode the output
            translation = self.model.generate(**batch)
            result = self.tokenizer.batch_decode(
                translation, skip_special_tokens=skip_special_tokens
            )
            return result
