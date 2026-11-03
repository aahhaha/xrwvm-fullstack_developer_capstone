# fullstack_developer_capstone

Repository: xrwvm-fullstack_developer_capstone

Best Cars is a full-stack dealership review application. React provides the
dealership directory, state filtering, account registration, and review forms.
Django handles authentication and car inventory in SQLite. A Node/Express service
stores dealership and review data in MongoDB, and a Flask service analyzes review
sentiment using VADER.

## Run
From `server`, run `docker compose up --build`. Open http://localhost:8000.
Create an admin with `docker compose exec web python manage.py createsuperuser`.
The initial inventory and sample dealership/review records come from the course
starter dataset. New reviews persist in MongoDB across service restarts.

## API
- POST `/djangoapp/registration`, POST `/djangoapp/login`, GET `/djangoapp/logout`
- GET `/djangoapp/get_dealers`, GET `/djangoapp/get_dealers/Kansas`
- GET `/djangoapp/dealer/1`, GET `/djangoapp/reviews/dealer/1`
- GET `/djangoapp/get_cars`, POST `/djangoapp/add_review`
- Sentiment service: GET `/analyze/Fantastic%20services`
