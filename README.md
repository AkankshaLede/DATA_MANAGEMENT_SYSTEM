# FastAPI Dockerized Application

## Description
This project is a FastAPI-based web application that provides APIs for handling data. It is containerized using Docker for easy deployment and scalability.

## Features
- FastAPI for high-performance APIs
- Docker for containerization
- Docker Compose for multi-container setup
- Database integration
- `.env` support for configuration management
- Custom subnet configuration for networking

## Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Setup and Running the Application

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Build and run the container:
   ```sh
   docker-compose up --build
   ```

3. The application will be available at:
   ```sh
   http://localhost:8000/docs
   ```
   This opens the Swagger UI where you can test the APIs.

## Database Setup
The application uses PostgreSQL as the database. Follow these steps to set up the database:

### Create Database and Tables
1. Connect to PostgreSQL using:
   ```sh
   psql -U postgres
   ```
2. Create a new database:
   ```sql
   CREATE DATABASE fastapi_db;
   ```
3. Switch to the newly created database:
   ```sql
   \c fastapi_db;
   ```
4. Create a table (example):
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### Connecting PostgreSQL with Docker
If running PostgreSQL as a Docker container, update `docker-compose.yml` to include:
```yaml
services:
  db:
    image: postgres
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
    networks:
      - my_network
```
Ensure your FastAPI application reads the database credentials from the `.env` file and connects properly.

## Docker Networking and Subnet
The `docker-compose.yml` file includes a custom network configuration to ensure proper container communication. Below is an example of a subnet setup in Docker Compose:

```yaml
networks:
  my_network:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.1.0/24
```

### Explanation:
- **`driver: bridge`**: Creates an isolated network where containers can communicate.
- **`ipam` (IP Address Management)**: Defines IP settings for the network.
- **`subnet: 192.168.1.0/24`**: Specifies a subnet where containers will be assigned IP addresses within this range.

### Understanding Docker Networking:
Docker provides various networking modes:
1. **Bridge Network (Default Mode)**: Creates an internal network for communication between containers.
2. **Host Network**: Removes network isolation and allows containers to use the host’s networking stack.
3. **Overlay Network**: Used in swarm mode to allow communication across multiple Docker hosts.
4. **None Network**: Disables networking for a container.

Using a custom bridge network, as seen in this project, ensures better control over container communication and avoids IP conflicts. This setup is beneficial when multiple services (such as a database and API server) need to communicate securely within an isolated network.

## Docker Commands
Here are some useful Docker commands for managing the application:

- Build the image:
  ```sh
  docker build -t fastapi-app .
  ```
- Run the container:
  ```sh
  docker run -p 8000:8000 fastapi-app
  ```
- Stop running containers:
  ```sh
  docker-compose down
  ```
- Check running containers:
  ```sh
  docker ps
  ```
- View logs:
  ```sh
  docker logs <container-id>
  ```

## Environment Variables
The project uses a `.env` file for configuration. Ensure you update it before running the application.

## Contributing
If you wish to contribute, feel free to fork the repository and create a pull request.

## License
This project is licensed under the MIT License.

