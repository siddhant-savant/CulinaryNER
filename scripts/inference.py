"""
CulinaryNER Inference Script

Extract culinary entities from restaurant reviews using trained model.

Usage:
    python inference.py --model models/spacy_baseline --text "The truffle risotto was creamy."

Authors: Siddhant Sawant and Akshatha Poojari
"""

import argparse
import spacy


def extract_entities(model_path, text):
    """
    Extract culinary entities from text.
    
    Args:
        model_path: Path to trained spaCy model
        text: Review text to analyze
        
    Returns:
        List of (entity_text, label) tuples
    """
    nlp = spacy.load(model_path)
    doc = nlp(text)
    
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def main():
    parser = argparse.ArgumentParser(description="Extract culinary entities from text")
    parser.add_argument("--model", required=True, help="Path to trained model")
    parser.add_argument("--text", required=True, help="Text to analyze")
    
    args = parser.parse_args()
    
    print(f"Text: {args.text}\n")
    
    entities = extract_entities(args.model, args.text)
    
    if entities:
        print("Extracted entities:")
        for text, label in entities:
            print(f"  • {text:30} → {label}")
    else:
        print("No entities detected")


if __name__ == "__main__":
    main()
