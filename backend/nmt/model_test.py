# # -*- coding: utf-8 -*-
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("./backend/nmt/models/en-ja")

# model = AutoModelForSeq2SeqLM.from_pretrained("./backend/nmt/models/en-ja").cuda().eval()

# text = "There's no one in the office."
# # Tokenize the text
# batch = tokenizer(text, return_tensors='pt')

# # Make sure that the tokenized text does not exceed the maximum
# # allowed size of 512
# batch["input_ids"] = batch["input_ids"][:, :1024].cuda()
# batch["attention_mask"] = batch["attention_mask"][:, :1024].cuda()

# # Perform the translation and decode the output
# translation = model.generate(**batch)
# result = tokenizer.batch_decode(translation, skip_special_tokens=True)
# print(result)

# # print(model.cpu())

from . import HFNlpModel
import yaml

if __name__ == '__main__':
    with open('/home/ljj/code/py/nlp/nlp_web_flask/translation-webui/backend/nmt/config.yaml', 'r') as f:
        data = yaml.safe_load(f)
    m = HFNlpModel(data['models'][2])
    print(m("this is a book.", src='en', tgt='jp'))
    pass