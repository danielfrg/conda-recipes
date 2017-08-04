import sys
import spacy
from spacy import util
from spacy.deprecated import resolve_model_name

def is_present(name):
    data_path = util.get_data_path()
    model_name = resolve_model_name(name)
    model_path = data_path / model_name
    return model_path.exists()

assert is_present('es') is True

nlp = spacy.load('es')
