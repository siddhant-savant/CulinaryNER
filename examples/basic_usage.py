"""
Basic CulinaryNER Usage Examples

Demonstrates how to use the trained model for entity extraction.

Authors: Akshatha Poojari and Siddhant Sawant
"""

import spacy

# Load trained model
print("Loading CulinaryNER model...")
nlp = spacy.load("../models/spacy_baseline/model-best")

# Example restaurant reviews
reviews = [
    "The slow-roasted duck with crispy skin was absolutely divine.",
    "Chef Marco's signature carbonara uses aged parmesan and guanciale.",
    "The tender wagyu beef was perfectly grilled with a smoky finish.",
    "Loved the al dente pasta with fresh basil and rich tomato sauce.",
    "Their miso black cod is glazed to perfection - truly umami-rich!",
]

print("\n" + "="*70)
print("CULINARY ENTITY EXTRACTION EXAMPLES")
print("="*70)

for i, text in enumerate(reviews, 1):
    print(f"\nReview {i}:")
    print(f"  {text}")
    
    doc = nlp(text)
    
    if doc.ents:
        print("  Entities:")
        for ent in doc.ents:
            print(f"    • {ent.text:25} → {ent.label_}")
    else:
        print("    No entities detected")
    
    print("-" * 70)
