from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


class NER:
    def __init__(self) -> None:
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.ner = pipeline("ner", model=model, tokenizer=tokenizer)
