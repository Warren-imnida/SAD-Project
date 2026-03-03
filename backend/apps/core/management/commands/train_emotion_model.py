from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)
import torch
from torch.utils.data import Dataset


class EmotionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=96)
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item


class Command(BaseCommand):
    help = 'Train BERT model for EmoTune mood classification'

    def handle(self, *args, **options):
        root = Path(__file__).resolve().parents[5]
        data_path = root / 'datasets' / 'emotion_prompts.csv'
        model_out = root / 'backend' / 'trained_model'
        model_out.mkdir(exist_ok=True)

        df = pd.read_csv(data_path)
        le = LabelEncoder()
        y = le.fit_transform(df['emotion'])

        train_x, test_x, train_y, test_y = train_test_split(
            df['text'].tolist(), y, test_size=0.2, random_state=42, stratify=y
        )

        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        model = AutoModelForSequenceClassification.from_pretrained(
            'bert-base-uncased', num_labels=len(le.classes_)
        )

        train_ds = EmotionDataset(train_x, train_y, tokenizer)
        test_ds = EmotionDataset(test_x, test_y, tokenizer)

        args = TrainingArguments(
            output_dir=str(model_out),
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=2,
            learning_rate=2e-5,
            eval_strategy='epoch',
            save_strategy='no',
            logging_steps=25,
            report_to=[],
        )

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=test_ds,
        )
        trainer.train()

        preds = trainer.predict(test_ds).predictions.argmax(axis=1)
        report = classification_report(test_y, preds, target_names=le.classes_, digits=3)
        self.stdout.write(report)

        model.save_pretrained(model_out)
        tokenizer.save_pretrained(model_out)
        (model_out / 'labels.txt').write_text('\n'.join(le.classes_))
        self.stdout.write(self.style.SUCCESS(f'Model saved to {model_out}'))
