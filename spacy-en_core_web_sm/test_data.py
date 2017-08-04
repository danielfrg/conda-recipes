import sys
import spacy
from spacy import util
from spacy.deprecated import resolve_model_name

def is_present(name):
    data_path = util.get_data_path()
    model_name = resolve_model_name(name)
    model_path = data_path / model_name
    return model_path.exists()

assert is_present('en') is True

# Test for english
nlp = spacy.load('en')

doc = nlp('London is a big city in the United Kingdom.')
assert doc[0].text == 'London'
assert doc[0].ent_iob > 0
assert doc[0].ent_type_ == 'GPE'

assert doc[1].text == 'is'
assert doc[1].ent_iob > 0
assert doc[1].ent_type_ == ''
