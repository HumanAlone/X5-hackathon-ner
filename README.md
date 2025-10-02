## Доступ к сервису

Проект доступен по публичному IP

## Развёртывание сервиса в облаке

```bash
git clone https://github.com/HumanAlone/X5-hackathon-ner
cd X5-hackathon-ner

sudo docker build -t fastapi-app .
sudo docker run -d -p 8000:8000 --restart=always fastapi-app
sudo docker ps
```

## Структура проекта

```
X5-hackathon-ner/
├── app.py                  - FastAPI приложение
├── ner_model_v4_best/      - Папка с обученной моделью
├── utils/                  - Вспомогательные функции
├── requirements.txt        - Список зависимостей
├── Dockerfile              - Конфигурация для сборки Docker-образа
├── README.md               - Документация проекта
└── model_training.ipynb    - Jupyter Notebook для обучения модели
```

## API

### Request

```json
{ "input": "сгущенное молоко" }
```

### Response
```json
[
  { "start_index": 0, "end_index": 8, "entity": "B-TYPE" },
  { "start_index": 9, "end_index": 15, "entity": "I-TYPE" }
]
```
