import asyncio
from concurrent.futures import ThreadPoolExecutor

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForTokenClassification, AutoTokenizer

from utils import EntityResponse, convert_model_output

app = FastAPI(title="X5-hack")

model_executor = ThreadPoolExecutor(max_workers=4)

tokenizer = None
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


label_list = [
    "O",
    "B-TYPE",
    "I-TYPE",
    "B-BRAND",
    "I-BRAND",
    "B-VOLUME",
    "I-VOLUME",
    "B-PERCENT",
    "I-PERCENT",
]

# Создаем mapping
label_to_id = {label: i for i, label in enumerate(label_list)}
id_to_label = {i: label for i, label in enumerate(label_list)}


class PredictionRequest(BaseModel):
    input: str


def load_model(model_path: str):
    """
    Загружает модель и токенайзер из папки
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForTokenClassification.from_pretrained(model_path)
        model.eval()
        model.to(device)
        return tokenizer, model
    except Exception as e:
        raise Exception(f"Ошибка загрузки модели: {str(e)}")


@app.on_event("startup")
async def load_models():
    global tokenizer, model
    try:
        model_path = "ner_model_v4_best"
        tokenizer, model = load_model(model_path)
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")


def predict_annotations(text):
    if tokenizer is None or model is None:
        raise Exception("Модель не загружена.")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        return_offsets_mapping=True,
    )
    offset_mapping = inputs.pop("offset_mapping")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)[0].cpu().numpy()

    return predictions_to_annotations(text, predictions, offset_mapping[0])


def predictions_to_annotations(text, predictions, offset_mapping):
    annotations = []

    i = 0
    while i < len(offset_mapping):
        start, end = offset_mapping[i]
        if start == end == 0:
            i += 1
            continue

        word_label = id_to_label[predictions[i]]

        j = i + 1
        while j < len(offset_mapping):
            next_start, next_end = offset_mapping[j]
            if next_start == end:
                end = next_end
                j += 1
            else:
                break

        annotations.append((start.item(), end.item(), word_label))
        i = j

    return annotations


@app.post("/api/predict", response_model=list[EntityResponse])
async def predict(request: PredictionRequest):
    if not request.input:
        return []

    loop = asyncio.get_event_loop()
    annotations = await loop.run_in_executor(
        model_executor, predict_annotations, request.input
    )

    raw_model_output = f"{request.input};{annotations}"

    return convert_model_output(raw_model_output)


@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}
