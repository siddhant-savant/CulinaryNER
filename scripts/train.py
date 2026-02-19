"""
CulinaryNER Training Script

Train a spaCy NER model for culinary entity extraction from restaurant reviews.

Usage:
    python train.py --data path/to/labelstudio_export.json --output models/my_model --epochs 30

Authors: Siddhant Sawant and Akshatha Poojari
"""

import json
import random
import argparse
from pathlib import Path
import spacy
from spacy.training import Example, offsets_to_biluo_tags
from spacy.util import minibatch, compounding
from spacy.scorer import Scorer


def convert_labelstudio_to_spacy(data):
    """
    Convert Label Studio annotations to spaCy training format.
    
    Args:
        data: List of Label Studio annotation objects
        
    Returns:
        List of tuples: (text, {"entities": [(start, end, label), ...]})
    """
    training_data = []
    
    for item in data:
        text = item['data']['text']
        
        # Skip items without annotations
        if not item.get('annotations') or len(item['annotations']) == 0:
            continue
        
        # Extract entities
        entities = []
        for result in item['annotations'][0]['result']:
            start = result['value']['start']
            end = result['value']['end']
            label = result['value']['labels'][0]
            entities.append((start, end, label))
        
        training_data.append((text, {"entities": entities}))
    
    return training_data


def clean_annotations(text, entities):
    """
    Remove broken annotations (overlaps and conflicts).
    Keep sentences with minor issues.
    
    Args:
        text: Review text
        entities: List of (start, end, label) tuples
        
    Returns:
        Cleaned list of entities, or empty list if unrecoverable
    """
    nlp_temp = spacy.blank("en")
    doc = nlp_temp.make_doc(text)
    
    # Remove duplicates
    unique_entities = []
    seen = set()
    for start, end, label in entities:
        key = (start, end, label)
        if key not in seen:
            unique_entities.append((start, end, label))
            seen.add(key)
    
    # Validate with ALL entities at once
    try:
        biluo_tags = offsets_to_biluo_tags(doc, unique_entities)
        return unique_entities
    except ValueError as e:
        # Only drop if actual conflicts
        if "conflicting" in str(e):
            return []
        return unique_entities
    except:
        return unique_entities


def load_and_prepare_data(filepath, train_split=0.8, dev_split=0.1):
    """
    Load Label Studio annotations and split into train/dev/test sets.
    
    Args:
        filepath: Path to Label Studio JSON export
        train_split: Proportion for training (default 0.8)
        dev_split: Proportion for development (default 0.1)
        
    Returns:
        Tuple of (train_data, dev_data, test_data)
    """
    # Load annotations
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} annotations from {filepath}")
    
    # Convert to spaCy format
    training_data = convert_labelstudio_to_spacy(data)
    print(f"Converted {len(training_data)} annotated sentences")
    
    # Clean annotations
    clean_data = []
    for text, annot in training_data:
        clean_ents = clean_annotations(text, annot['entities'])
        if clean_ents:
            clean_data.append((text, {"entities": clean_ents}))
    
    print(f"After cleaning: {len(clean_data)} sentences")
    print(f"Retention rate: {len(clean_data)/len(training_data)*100:.1f}%")
    
    # Shuffle and split
    random.shuffle(clean_data)
    n = len(clean_data)
    
    train_end = int(n * train_split)
    dev_end = train_end + int(n * dev_split)
    
    train_data = clean_data[:train_end]
    dev_data = clean_data[train_end:dev_end]
    test_data = clean_data[dev_end:]
    
    print(f"\nData split:")
    print(f"  Train: {len(train_data)} sentences ({train_split*100:.0f}%)")
    print(f"  Dev:   {len(dev_data)} sentences ({dev_split*100:.0f}%)")
    print(f"  Test:  {len(test_data)} sentences ({(1-train_split-dev_split)*100:.0f}%)")
    
    return train_data, dev_data, test_data


def train_ner_model(train_data, dev_data, n_epochs=30, dropout=0.5):
    """
    Train spaCy NER model on culinary entities.
    
    Args:
        train_data: Training examples
        dev_data: Development examples for evaluation
        n_epochs: Number of training epochs
        dropout: Dropout rate for regularization
        
    Returns:
        Trained nlp model
    """
    # Entity labels for CulinaryNER
    labels = [
        "DISH",        # Prepared dishes
        "INGREDIENT",  # Food components
        "TECHNIQUE",   # Cooking methods
        "FLAVOR",      # Taste descriptors
        "TEXTURE",     # Mouthfeel
        "CUISINE",     # Culinary styles
        "CHEF_NAME"    # Named chefs
    ]
    
    print(f"\nTraining model with entity types: {', '.join(labels)}")
    print("=" * 60)
    
    # Create blank model and add NER pipeline
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
    # Add labels
    for label in labels:
        ner.add_label(label)
    
    # Initialize training
    optimizer = nlp.begin_training()
    
    # Training parameters
    batch_size_start = 4.0
    batch_size_end = 32.0
    
    # Training loop
    for epoch in range(n_epochs):
        random.shuffle(train_data)
        losses = {}
        
        # Create batches with compounding size
        batches = minibatch(train_data, size=compounding(batch_size_start, batch_size_end, 1.001))
        
        # Update model
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            
            nlp.update(examples, drop=dropout, losses=losses, sgd=optimizer)
        
        # Evaluate on dev set every 5 epochs
        if epoch % 5 == 0:
            dev_examples = []
            for text, annotations in dev_data:
                doc = nlp(text)
                example = Example.from_dict(doc, annotations)
                dev_examples.append(example)
            
            scorer = Scorer()
            scores = scorer.score(dev_examples)
            
            print(f"Epoch {epoch:2d}: Loss = {losses['ner']:.2f}, Dev F1 = {scores['ents_f']:.3f}")
    
    print("\nTraining complete!")
    return nlp


def evaluate_model(nlp, test_data):
    """
    Evaluate trained model on test set.
    
    Args:
        nlp: Trained spaCy model
        test_data: Test examples
        
    Returns:
        Dictionary of evaluation scores
    """
    print("\nEvaluating on test set...")
    print("=" * 60)
    
    # Create evaluation examples
    examples = []
    for text, annotations in test_data:
        doc = nlp(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)
    
    # Score model
    scorer = Scorer()
    scores = scorer.score(examples)
    
    # Print results
    print("\nOVERALL PERFORMANCE")
    print("-" * 60)
    print(f"Precision: {scores['ents_p']:.3f}")
    print(f"Recall:    {scores['ents_r']:.3f}")
    print(f"F1 Score:  {scores['ents_f']:.3f}")
    
    print("\nPER-ENTITY PERFORMANCE")
    print("-" * 60)
    print(f"{'Entity':<12} {'Precision':<10} {'Recall':<10} {'F1 Score':<10}")
    print("-" * 60)
    
    labels = ["DISH", "INGREDIENT", "TECHNIQUE", "FLAVOR", "TEXTURE", "CUISINE", "CHEF_NAME"]
    
    if 'ents_per_type' in scores:
        for label in labels:
            if label in scores['ents_per_type']:
                entity_scores = scores['ents_per_type'][label]
                p = entity_scores['p']
                r = entity_scores['r']
                f = entity_scores['f']
                print(f"{label:<12} {p:<10.3f} {r:<10.3f} {f:<10.3f}")
            else:
                print(f"{label:<12} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
    
    return scores


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train CulinaryNER model")
    parser.add_argument("--data", required=True, help="Path to Label Studio JSON export")
    parser.add_argument("--output", required=True, help="Output directory for trained model")
    parser.add_argument("--epochs", type=int, default=30, help="Number of training epochs")
    parser.add_argument("--seed", type=int, default=45, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    # Set random seed
    random.seed(args.seed)
    
    # Load and prepare data
    train_data, dev_data, test_data = load_and_prepare_data(args.data)
    
    # Train model
    nlp = train_ner_model(train_data, dev_data, n_epochs=args.epochs)
    
    # Evaluate
    scores = evaluate_model(nlp, test_data)
    
    # Save model
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_path)
    print(f"\nModel saved to: {output_path}")
    
    # Save performance metrics
    metrics = {
        "overall": {
            "precision": float(scores['ents_p']),
            "recall": float(scores['ents_r']),
            "f1": float(scores['ents_f'])
        },
        "per_entity": {}
    }
    
    if 'ents_per_type' in scores:
        for label, entity_scores in scores['ents_per_type'].items():
            metrics["per_entity"][label] = {
                "precision": float(entity_scores['p']),
                "recall": float(entity_scores['r']),
                "f1": float(entity_scores['f'])
            }
    
    metrics_path = output_path / "performance.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Performance metrics saved to: {metrics_path}")
    print("\n" + "=" * 60)
    print(f"FINAL F1 SCORE: {scores['ents_f']:.3f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
