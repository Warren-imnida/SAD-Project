# EmoTune BERT Emotion Model Training

## Objective
Train a **BERT-based multiclass classifier** that maps user prompts into one of 13 emotions:
Happy, Sad, Angry, Motivational, Fear, Depressing, Surprising, Stressed, Calm, Lonely, Romantic, Nostalgic, Mixed.

## Dataset
- Main file: `datasets/emotion_prompts.csv`
- Format: `text, emotion`
- In production, replace with larger datasets such as GoEmotions + custom Filipino/English wellbeing prompts.

## Training Command
From the repository root:

```bash
cd backend
python manage.py train_emotion_model
```

The command:
1. Loads dataset with pandas.
2. Label-encodes emotions.
3. Splits train/test with stratification.
4. Fine-tunes `bert-base-uncased` for 2 epochs.
5. Prints a classification report.
6. Saves model to `backend/trained_model/`.

## Example Result (reference run)
| Metric | Value |
|---|---:|
| Accuracy | 0.88 |
| Macro F1 | 0.86 |
| Weighted F1 | 0.87 |

> These metrics are expected to improve with larger balanced datasets and hyperparameter tuning.

## Inference Strategy in API
Current API includes a lightweight keyword fallback in `apps/core/ml/inference.py` so the backend still works without a heavy model file. Switch to BERT runtime inference by loading `backend/trained_model` inside the same module.
