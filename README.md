# Prefect Workflow Project

This guide will help you set up and run Prefect server along with your workflows.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10 or higher
- Development container set up (see `.devcontainer` folder)

## Getting Started

1. Start the development container
2. Open a terminal in VS Code

## Setting Up Prefect

### Using PostgreSQL as the Prefect Database

**Note:** SQLite is not concurrent friendly and PostgreSQL is recommended. If you wish to use the built-in SQLite, you should limit the flow to not run concurrently.

To use PostgreSQL instead of SQLite for Prefect, run the following command:
```bash
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://{user}:{pass}@{url}:{port}/{database}"
```
Replace `{user}`, `{pass}`, `{url}`, `{port}`, and `{database}` with your PostgreSQL credentials and connection details.

1. Start the Prefect server:
```bash
prefect server start
```

This will start the Prefect server locally. By default, it will be available at:
- UI Dashboard: http://127.0.0.1:4200
- API: http://127.0.0.1:4200/api

2. In a new terminal, set up your Prefect configuration:
```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

3. Run the test workflow:
```bash
python test_workflow.py
```

## Fetching Current Weather Data

1. Ensure you have the assets/cities.json file in your project directory. This file should contain a list of cities for which you want to fetch weather data. Example format:

```
[
  {"city": "New York", "country": "US"},
  {"city": "London", "country": "GB"}
]
```

2. To fetch the current weather data based on the cities in the assets/cities.json file, run:

```
python main.py
```
This script will fetch the weather data for the cities listed in assets/cities.json using the OpenWeatherMap API.

## Setting Up SQLAlchemy Database

1. Install the required Python packages for SQLAlchemy and your database:
```
pip install sqlalchemy psycopg2  # For PostgreSQL
```
2. Run the following command to set up the database tables:

```
python ./database/main.py
```
This will create the necessary database tables defined in the SQLAlchemy models.

## Monitoring Your Workflow

1. Open your browser and navigate to http://127.0.0.1:4200
2. Click on "Flows" in the left sidebar
3. You should see your "test-workflow" listed
4. Click on the flow to see its run history and details

## Troubleshooting

If you encounter any issues:

1. Check if Prefect server is running:
```bash
prefect server status
```

2. Verify your API URL configuration:
```bash
prefect config view
```

## Common Issues

- If you get a "Connection refused" error, make sure the Prefect server is running
- If you can't access the UI, ensure no other services are using port 4200

