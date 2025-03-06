from dateutil.parser import parse
import spacy
import streamlit as st

nlp = spacy.load("en_core_web_sm")

def parse_date_time_from_text(text):
    doc = nlp(text)
    entities_dict = {'TIME': None, 'DATE': None}
    for ent in doc.ents:
        if ent.label_ in entities_dict:
            entities_dict[ent.label_] = ent.text
    return entities_dict


entities_dict = parse_date_time_from_text("I'm free on 20th of September at 12 am for a coffee")

print(entities_dict)

