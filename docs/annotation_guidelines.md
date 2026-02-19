# CulinaryNER Annotation Guidelines

## Overview

This document describes the methodology and rules used to create the CulinaryNER dataset. Annotations follow professional data annotation best practices adapted from industry experience.

## Entity Definitions

### DISH
Complete prepared food items as they would appear on a menu.

**Examples:**
- "miso black cod"
- "truffle risotto"
- "beef wellington"
- "fish and chips"

**Exclude:**
- Single ingredients without dish context ("beef", "chicken")
- Generic terms ("main course", "dessert", "entrée")

**Edge cases:**
- If consumed/ordered → DISH (e.g., "ribeye" as menu item)
- If used in preparation → INGREDIENT (e.g., "made with ribeye")

---

### INGREDIENT
Individual food components used in cooking.

**Examples:**
- "truffle oil"
- "aged parmesan"
- "wagyu beef"
- "free-range chicken"
- "fresh basil"

**Exclude:**
- When part of dish name ("basil" in "basil pesto pasta" = part of DISH)
- Generic categories ("vegetables", "protein", "meat")

---

### TECHNIQUE
Cooking or preparation methods.

**Examples:**
- "slow-roasted"
- "pan-fried"
- "sous vide"
- "glazed"
- "beer-battered"

**Exclude:**
- Generic verbs ("cooked", "made", "prepared")
- Non-cooking actions ("served", "presented", "plated")

**Beverage techniques (special rule):**
- Tag if part of food: "wine reduction sauce" → "wine" as INGREDIENT
- Tag technique: "beer-battered fish" → "beer-battered" as TECHNIQUE
- Don't tag if just drinking: "glass of wine" → skip entirely

---

### FLAVOR
Specific taste descriptors (not generic opinions).

**Examples:**
- Taste: "sweet", "salty", "sour", "bitter", "umami", "savory"
- Spice: "spicy", "hot", "mild", "fiery"
- Intensity: "bland", "overpowering", "subtle"
- Quality: "fresh", "stale", "tangy", "zesty", "rich"
- Seasoning: "well-seasoned", "undersalted", "peppery"

**Exclude (generic opinions):**
- "delicious", "amazing", "great", "terrible", "bad"
- These are sentiment, not flavor information

---

### TEXTURE
Mouthfeel and textural properties.

**Examples:**
- "crispy"
- "tender"
- "creamy"
- "al dente"
- "crunchy"
- "silky"

---

### CUISINE
Culinary styles and regional food traditions.

**Examples:**
- "Italian"
- "French"
- "Japanese"
- "Indian"
- "British"

**Edge case:**
- "Italian chef" → Tag as CUISINE (not CHEF_NAME unless specific person)

---

### CHEF_NAME
Named chefs mentioned in context.

**Examples:**
- "Chef Marco"
- "Chef Ramsay"
- "Chef Oliver"

**Only tag when:**
- Specific named individual
- In context of cooking/culinary work

---

## Critical Annotation Rules

### 1. No Overlapping Annotations
Each word belongs to ONE entity only. Do not annotate the same span twice.

### 2. No Misspellings
Skip misspelled words entirely:
- "pzza", "resturant", "chiken" → Do not annotate

### 3. Complete Words Only
- Select "pizza"
- Select "piz" or " pizza " (with spaces)

### 4. No Beverage Entities (Unless Ingredients)
**Tag beverages ONLY when used as ingredients:**
- "wine reduction sauce" → "wine" as INGREDIENT
- "whiskey-glazed ribs" → "whiskey-glazed" as TECHNIQUE
- "I ordered a glass of wine" → Skip entirely
- "The martini was excellent" → Skip entirely

### 5. Use Double-Click Selection
Avoid mouse dragging which can create selection errors.

### 6. Skip Unclear Sentences
When in doubt, skip the entire sentence rather than guess.
**Better to skip than annotate incorrectly.**

---

## Annotation Process

### Workflow

1. **Initial Annotation**
   - Primary annotator labels all entities
   - Focus on accuracy over speed
   - Skip unclear cases

2. **Quality Review**
   - Second annotator reviews annotations
   - Flags conflicts or errors
   - Suggests corrections

3. **Conflict Resolution**
   - Annotators discuss disagreements
   - Refer to guidelines
   - Make final decision

4. **Final Validation**
   - Systematic check for:
     - Overlapping entities
     - Misspelled words
     - Incomplete selections
     - Guideline violations

### Annotation Metrics

- **Average annotation time:** ~2 minutes per review
- **Total annotation hours:** ~560 hours

---

## Common Edge Cases

### Case 1: Compound Entities
"slow-roasted duck breast"
- Tag both: "slow-roasted" (TECHNIQUE) + "duck breast" (DISH)

### Case 2: Modified Ingredients
"aged parmesan cheese"
- Tag complete phrase: "aged parmesan" (INGREDIENT)

### Case 3: Dish with Technique
"pan-fried sea bass"
- Tag both: "pan-fried" (TECHNIQUE) + "sea bass" (DISH)

### Case 4: Flavor + Texture
"crispy and spicy chicken wings"
- Tag three: "crispy" (TEXTURE), "spicy" (FLAVOR), "chicken wings" (DISH)

---

## Tools Used

- **Annotation platform:** Label Studio
- **Format:** Character-offset based (start, end, label)
- **Export format:** JSON compatible with spaCy
- **Validation:** Automated checks for overlaps and conflicts

---

## Contact

For questions about annotation methodology:
- Siddhant Sawant: siddhantsavant7@gmail.com
- Akshatha Poojari: akshatha.poojari01@gmail.com
