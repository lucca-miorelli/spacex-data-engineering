## Setup & Run Application

Here is a step-by-step guide to help you set up and run the application.

#### Prerequisites
Ensure that you have

* Python 3.10.12
* Poetry 1.8.2
* Docker
* Docker-Compose 

installed on your system.

#### Get the Code
Clone the repository to your local machine using the command:

```
git clone https://github.com/lucca-miorelli/spacex-data-engineering.git
```

#### Set Up Virtual Environment
Create and activate a virtual environment using `Poetry`. 
To do this, simply run `poetry shell`.

#### Configure the Environment
Copy the example environment variable file and create your own `.env` file with: 

```bash
cp .env.example .env
```

Open the newly created `.env` file and replace the values as needed (you can run with the default values, it will work as well).

#### Install Dependencies
Once with the virtualenv actived, install all the necessary dependencies for the project by running 

```bash
poetry install
```

#### Start Services
Build and start the services using Docker Compose. This can be done using the following command: 

```bash
docker-compose up -d --build
```

#### Run Data Processing
On your terminal and run 
```bash
python app/processing/launches.py
```

This command requires that both MinIO bucket and Postgres database are up and running on your containers (configured on the previous step).

After running the python script, you can connect to the database to check your `launches` table.

#### Shut Down the Application
When you're done, you can shut down the application by running

```bash
docker-compose down
```

This stops and removes containers, networks, and volumes defined in the `docker-compose.yml` file.