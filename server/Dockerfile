FROM node:20-alpine AS frontend
WORKDIR /ui
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend /ui/build ./frontend/build
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py shell -c 'from djangoapp.populate import initiate; initiate()' && python manage.py runserver 0.0.0.0:8000 --noreload"]
