# ETL Pipeline

### Some considerations
A significant strategic decision was the adoption of data denormalization. While this approach introduces redundancy, the impact was negligible due to the small dataframe size (~200 rows). This choice was primarily influenced by missing Core Ids from the source data, coupled with the intent to simplify the solution.

> "Simplicity is the ultimate sophistication in engineering."

## Folder Structure
```
spacex-data-engineering/
├── app/
│   ├── models/
│   │   ├── launches.py                  # Pydantic models for data validation
│   ├── processing/
│   │   ├── launches.py                  # ETL script
│   ├── services/
│   │   ├── requester.py                 # HTTP functionalities
│   │   ├── db.py                        # Database functionalities
│   │   ├── aws.py                       # Cloud functionalities
│   └── settings.py                      # Configure Env variables and secrets
```

## Services

The `services` directory contains files for handling various functionalities:

- `requester.py`: This file contains functions for making HTTP requests to fetch data from the SpaceX API.

- `db.py`: This file manages interactions with the database, including creating and reading tables (CRUD operations and other functionalities could be implemented as well).

- `aws.py`: This file handles AWS-specific functionality, such as interacting with S3 (MinIO in this case) and other AWS resources. It consists of writing and reading JSON and parquet files, as well as basic operations like listing files under a specific path and verifying if a file exists.

## Models

The `models` directory contains the `launches.py` file. This file defines Pydantic models which are used for data validation. These models ensure that the data adheres to a specific format and type before it is processed and loaded into the database.

## Processing

The `processing` directory contains the `launches.py` file. This is the main ETL script that orchestrates the entire pipeline. It leverages the services defined in the `services` directory to fetch data from the SpaceX API, transform the data according to the Pydantic models, and load the processed data into the database.