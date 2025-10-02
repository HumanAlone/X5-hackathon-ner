## Развёртывание сервиса в облаке


# Развёртывание сервиса в облаке

```bash
git clone https://github.com/HumanAlone/X5-hackathon-ner
cd X5-hackathon-ner

sudo docker build -t fastapi-app .
sudo docker run -d -p 8000:8000 --restart=always fastapi-app
sudo docker ps
```


## Структура проекта

X5-hackathon-ner/
├── app.py                 # FastAPI приложение  
├── ner_model_v4_best/     # Папка с моделью  
├── utils/                 # Вспомогательные функции  
├── requirements.txt       # Зависимости  
├── Dockerfile             # Конфигурация Docker  
├── README.MD              # Документация  
└── model_training.ipynb   # Обучение модели  

