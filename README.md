# CulinaryNER

**Named Entity Recognition for Culinary Text - Trained spaCy model for granular restaurant review analysis**


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)



A trained spaCy model for extracting dishes, ingredients, cooking techniques, flavors, and more from restaurant reviews.

---

## Overview

CulinaryNER is a specialized NER model for culinary text analysis, addressing a critical gap in domain-specific NLP tools for the food and hospitality industry.

**Model Features:**
- **7 entity types**: Dish, Ingredient, Technique, Flavor, Texture, Cuisine, Chef Name
- **UK restaurant focus**: Trained on UK culinary terminology and dining contexts

**Training Data:**
- 8,000+ annotated UK restaurant reviews
- 5 major cuisines (British, Italian, Indian, Chinese, Japanese)
- Manual annotations following professional methodology (see [annotation guidelines](docs/annotation_guidelines.md))

---

## Quick Start

### Installation

```bash
pip install spacy
python -m spacy download en_core_web_sm

# Clone this repository
git clone https://github.com/siddhant-savant/CulinaryNER.git
cd CulinaryNER
```

### Basic Usage

```python
import spacy

# Load the CulinaryNER model
nlp = spacy.load("models/spacy_baseline/model-best")

# Process a restaurant review
text = "The slow-roasted duck with crispy skin was divine. Chef Marco's signature dish."

doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text:20} → {ent.label_}")

# Output:
# slow-roasted         → TECHNIQUE
# duck                 → DISH
# crispy               → TEXTURE
# skin                 → INGREDIENT
# divine               → FLAVOR
# Chef Marco           → CHEF_NAME
# signature dish       → DISH
```

See [`examples/basic_usage.py`](examples/basic_usage.py) for more examples.

---

## Model Performance

**spaCy Baseline Model (Released):**
- **Overall F1:** 0.711
- **Precision:** 0.725
- **Recall:** 0.698

**Per-Entity Performance:**

| Entity | Precision | Recall | F1 |
|--------|-----------|--------|-----|
| DISH | 0.762 | 0.734 | **0.748** |
| INGREDIENT | 0.629 | 0.632 | 0.631 |
| TECHNIQUE | 0.641 | 0.549 | 0.592 |
| FLAVOR | 0.791 | 0.486 | 0.603 |
| TEXTURE | 0.773 | 0.826 | **0.799** |
| CUISINE | 0.776 | 0.898  | **0.832** |
| CHEF_NAME | 0.882 | 0.714 | 0.789 |

See [`models/spacy_baseline/performance.json`](models/spacy_baseline/performance.json) for full metrics.

---

## Entity Types

| Label | Description | Examples |
|-------|-------------|----------|
| `DISH` | Complete dish names | "beef wellington", "pasta carbonara" |
| `INGREDIENT` | Food components | "basil", "truffle oil", "parmesan" |
| `TECHNIQUE` | Cooking methods | "slow-roasted", "pan-fried", "sous vide" |
| `FLAVOR` | Taste descriptors | "umami", "tangy", "smoky" |
| `TEXTURE` | Texture descriptors | "crispy", "tender", "al dente" |
| `CUISINE` | Cuisine types | "Italian", "French", "Japanese" |
| `CHEF_NAME` | Chef names | "Chef Ramsay", "Chef Oliver" |

---

## Use Cases

### 1. Restaurant Analytics
- Track menu item performance from review text
- Identify trending dishes and techniques
- Analyze chef mentions and reputation

### 2. Menu Optimization
- Understand which flavor/texture combinations resonate
- Identify successful ingredient pairings
- Competitive analysis across restaurants

### 3. Chef Recognition
- Extract chef mentions from reviews
- Build portable professional reputation systems
- Connect diners with individual culinary creators

### 4. Research & Development
- Domain-specific NLP model development
- Culinary vocabulary analysis
- Cross-cuisine comparison studies

---

## Documentation

### Annotation Methodology

This model was trained on professionally annotated data following rigorous guidelines:

- **[Complete Annotation Guidelines](docs/annotation_guidelines.md)** - Detailed entity definitions and rules
- **Annotation time**: ~560 hours of manual annotation

### Training Approach

**Transfer Learning Strategy:**
1. Initial training on diverse restaurant review corpus for foundational culinary vocabulary
2. Specialization on UK-curated data for market-specific terminology
3. Focus on UK culinary contexts (e.g., "chips" vs "fries", UK dining terminology)

**Why UK-Specific Matters:**
UK culinary language differs from other markets. This model captures nuances like British dessert terminology ("pudding"), regional dishes, and UK chef mentions.

---

## Training Your Own Model

While we're releasing the trained model, you can also train your own using the provided scripts:

```bash
# Train on your own annotated data
python scripts/train.py \
  --data your_annotations.json \
  --output models/my_model \
  --epochs 30

# Evaluate
python scripts/evaluate.py \
  --model models/my_model \
  --data your_test_data.json

# Run inference
python scripts/inference.py \
  --model models/my_model \
  --text "The truffle risotto was creamy and umami-rich."
```

**Note:** Training scripts expect Label Studio JSON format. See [annotation guidelines](docs/annotation_guidelines.md) for entity definitions.

---

## Real-World Application

CulinaryNER aims to power **[Compliments to the Chef](https://complimentstothechef.co.uk)**, a QR code-based platform creating portable professional reputations for individual chefs.

---

## Contributing

We welcome contributions! Areas for improvement:

- **Model enhancements**: BERT/transformer implementations, ensemble methods
- **Additional cuisines**: French, Thai, Mexican, Mediterranean
- **New entity types**: DIETARY_RESTRICTION, COOKING_TIME, PRESENTATION
- **Multi-language support**: French, Spanish, Italian restaurant reviews
- **Error analysis**: Edge cases and challenging examples

Please open an issue to discuss contributions before submitting pull requests.

---

## Citation

If you use CulinaryNER in your research or application, please cite:

```bibtex
@software{culinaryner2026,
  title={CulinaryNER: Named Entity Recognition for Culinary Text},
  author={Sawant, Siddhant and Poojari, Akshatha},
  year={2026},
  publisher={GitHub},
  url={https://github.com/siddhant-savant/CulinaryNER},
  note={Trained spaCy model for culinary entity extraction}
}
```

---

## License

This model and code are released under the **MIT License**.

You are free to:
- Use commercially
- Modify and distribute
- Use privately

Attribution is appreciated but not required. See [LICENSE](LICENSE) for details.

---

## Authors

**Siddhant Sawant** - Model Development & Training
[LinkedIn](https://linkedin.com/in/siddhant-sawant-343324180) | [GitHub](https://github.com/siddhant-savant)

**Akshatha Poojari** - Data Engineering & Documentation 
[LinkedIn](https://www.linkedin.com/in/akshatha-poojari-32ab12198/) | [GitHub](https://github.com/Akshatha-25)

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for detailed contributions.

---

## Related Work

- **Compliments to the Chef** - Restaurant review platform using CulinaryNER ([complimentstothechef.co.uk](https://complimentstothechef.co.uk))
- Part of Morze Tech's mission to modernize hospitality technology through AI

---

## Note on Commercial Models

This repository contains our **baseline spaCy model** (F1: 0.711) as an open-source contribution.

We also maintain a **proprietary BERT-based model** (F1: 0.758) meant to be used in commercial  platforms. The enhanced model is not included in this release.

For commercial licensing or custom model training: siddhantsavant7@gmail.com, akshatha.poojari01@gmail.com

---

## Contact

**Questions? Feedback? Collaborations?**

- Email: siddhantsavant7@gmail.com, akshatha.poojari01@gmail.com
- Open an issue on GitHub
- Connect on [LinkedIn](https://linkedin.com/in/siddhant-sawant-343324180)- **Siddhant Sawant**
- Connect on [LinkedIn](https://linkedin.com/in/akshatha-poojari-32ab12198)- **Akshatha Poojari**

---

**Star this repo if you find it useful!**

---

*CulinaryNER - Teaching AI to understand food, one review at a time.*
