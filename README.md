# Hikehub project

This is a project the main target of it is to help tourists to organize trips.

The project uses Python 3 as a main language. Backend framework that is used is Flask. Frontend framework is Vue.js.

## Building the project

To build the project you first need to build a frontend and then run a docker-compose

```powershell
cd web
npm install
npm run build

cd ..
docker compose up -d
```

## Running the frontend

Frontend uses Vite as a packaging framework.

```powershell
cd web
npm install
npm run dev
```

## Running the backend

To run the backend in debug mode do the following.

```powershell
cd app

py -m venv .venv
.venv/Scripts/Activate.ps1

pip install -r requirements.txt

$ENV:FLASK_APP="organizer"
$ENV:FLASK_ENV="development"

flask run
```
