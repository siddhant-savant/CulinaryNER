"""
CulinaryNER Evaluation Script

Evaluate a trained spaCy NER model on test data.

Usage:
    python evaluate.py --model models/spacy_baseline --data test_data.json

Authors: Siddhant Sawant and Akshatha Poojari
"""

import json
import argparse
import spacy
from spacy.training import Example
from spacy.scorer import Scorer


def load_test_data(filepath):
    """Load test data in spaCy format."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


def evaluate_model(model_path, test_data_path):
    """
    Evaluate trained model on test set.
    
    Args:
        model_path: Path to trained spaCy model
        test_data_path: Path to test data JSON
    """
    # Load model
    print(f"Loading model from {model_path}...")
    nlp = spacy.load(model_path)
    
    # Load test data
    print(f"Loading test data from {test_data_path}...")
    test_data = load_test_data(test_data_path)
    
    # Create evaluation examples
    examples = []
    for item in test_data:
        text = item['text']
        entities = [(e[0], e[1], e[2]) for e in item['entities']]
        
        doc = nlp(text)
        example = Example.from_dict(doc, {"entities": entities})
        examples.append(example)
    
    # Score model
    scorer = Scorer()
    scores = scorer.score(examples)
    
    # Print results
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    
    print("\nOverall Performance:")
    print(f"  Precision: {scores['ents_p']:.3f}")
    print(f"  Recall:    {scores['ents_r']:.3f}")
    print(f"  F1 Score:  {scores['ents_f']:.3f}")
    
    print("\nPer-Entity Performance:")
    print("-" * 60)
    print(f"{'Entity':<15} {'Precision':<12} {'Recall':<12} {'F1 Score':<12}")
    print("-" * 60)
    
    if 'ents_per_type' in scores:
        for label, metrics in sorted(scores['ents_per_type'].items()):
            p = metrics['p']
            r = metrics['r']
            f = metrics['f']
            print(f"{label:<15} {p:<12.3f} {r:<12.3f} {f:<12.3f}")
    
    print("=" * 60)
    
    return scores


def main():
    parser = argparse.ArgumentParser(description="Evaluate CulinaryNER model")
    parser.add_argument("--model", required=True, help="Path to trained model")
    parser.add_argument("--data", required=True, help="Path to test data JSON")
    
    args = parser.parse_args()
    
    scores = evaluate_model(args.model, args.data)


if __name__ == "__main__":
    main()
