# Foodgram "Product Assistant"

The Foodgram "Product Assistant" project includes an online service and an API for it. On this service, users will be able to publish recipes, subscribe to the publications of other users, add their favorite recipes to the "Favorites" list.

## A distinctive feature of this service is the ability to add recipes to the "Shopping List" and download a summarized list of products before going to the store.

### What technologies were used:
- PostgreSQL
- nginx
- Python 3.8.5
- Git (GitHub repository)
- Docker (Docker hub repository)
- All kinds of magic (more details in requirements.txt)
--- 

### Installation and launch - let's get started:
1. Clone the repository with the project
```bash
git clone https://github.com/Uforick/foodgram-project-react.git
```
2. On the project server, install `doker` and `docker-compose`
```bash 
sudo apt install docker.io 
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
3. Launch preparation:
Copy the prepared files `docker-compose.yaml` and `nginx/default.conf` from your project to the server in `home/<your_username>/docker-compose.yaml` and `home/<your_username>/nginx/default.conf ` respectively.
Create a `.env` file with your environment variables
Example:
```
DB_NAME=postgres
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=<your_password>
DB_HOST=db
DB_PORT=5432
```
4. launching `docker-compose`:
```bash
docker-compose up -d --build
docker-compose exec backend python manage.py makemigrations --noinput
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```
---
![example workflow](https://github.com/Uforick/foodgram-project-react/actions/workflows/Foodgram_workflow.yml/badge.svg)

Credit github.com/Uforick
---
