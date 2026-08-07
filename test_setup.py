import spacy

nlp = spacy.load("en_core_web_sm")

text = """
Hetvi Gandhi studied Computer Science at the University of California, San Diego.
She worked at Esri Global in Sharjah from June 2025 to August 2025.
"""

doc = nlp(text)

print("spaCy loaded successfully.")
print("\nDetected entities:")

for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")