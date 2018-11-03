# Dating App
Dating for social good.

# Table Of Contents
- [Overview](#overview)
- [Configuration](#configuration)
- [Development](#development)

# Overview
Dating for social good.

# Configuration
Set the following environment variables to configure the application:

- `MONGO_URI`: MongoDB connection URI

# Development
A Docker container is used to run the application.  

## Build Docker Container
First you must build the Docker container:  

```
make build
```

## Run Flask
Start Flask in the Docker container:

```
make run
```

## Command Prompt
To start a command prompt for development:

```
make shell
```
