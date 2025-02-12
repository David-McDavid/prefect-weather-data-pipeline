# PySpark and Prefect Workflow Project

This guide will help you set up and run Prefect server along with your workflows.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10 or higher
- Development container set up (see `.devcontainer` folder)

## Getting Started

1. Start the development container
2. Open a terminal in VS Code

## Setting Up Prefect

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

## Running the Test Workflow

1. Create a new file called `test_workflow.py`:
```python
from prefect import flow, task
from pyspark.sql import SparkSession

@task
def create_spark_session():
    return SparkSession.builder \
        .appName("TestWorkflow") \
        .getOrCreate()

@task
def sample_spark_operation(spark):
    # Create a sample DataFrame
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    df = spark.createDataFrame(data, ["name", "value"])
    return df.count()

@flow(name="test-workflow")
def main():
    spark = create_spark_session()
    count = sample_spark_operation(spark)
    print(f"Number of rows: {count}")
    spark.stop()

if __name__ == "__main__":
    main()
```

2. Run the workflow:
```bash
python test_workflow.py
```

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

3. Check PySpark connection by running a simple PySpark shell:
```bash
pyspark
```

## Common Issues

- If you get a "Connection refused" error, make sure the Prefect server is running
- If PySpark fails to start, check your JAVA_HOME environment variable
- If you can't access the UI, ensure no other services are using port 4200

## Development Workflow

1. Always start the Prefect server first
2. Create your flows in separate Python files
3. Run your flows using `python <flow_file>.py`
4. Monitor execution in the Prefect UI

## Project Structure

```
.
├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── requirements.txt
├── flows/
│   └── test_workflow.py
└── README.md
```

## Next Steps

- Create more complex workflows by adding additional tasks
- Set up scheduling for your flows
- Configure deployment settings
- Add error handling and notifications
- Set up work pools and workers for distributed execution

For more information, visit the [Prefect Documentation](https://docs.prefect.io/).