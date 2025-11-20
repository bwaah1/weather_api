# Weather API Backend

A FastAPI-based weather service application built with Clean Architecture principles.

## Architecture

This project follows **Clean Architecture** principles, which allows for easy component replacement and testing:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: External dependencies (API clients, storage, cache, logging)
- **Presentation Layer**: API endpoints and request/response models

### Easy Component Replacement

Thanks to the Clean Architecture approach, you can easily swap implementations:

- **Storage**: Switch between local file storage and AWS S3
- **Cache**: Replace memory cache with Redis or other solutions
- **Logging**: Change from local file logging to cloud logging services
- **External APIs**: Replace weather API client with different providers

## Storage Types

The application supports two storage types:

1. **Local Storage** (`local`): Stores weather data in local filesystem (`data/` directory)
2. **S3 Storage** (`s3`): Stores weather data in AWS S3 bucket

Configure storage type via `APP_STORAGE_TYPE` environment variable.

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Quick Start

1. Copy `.env.example` to `.env` and configure your settings
2. Set `APP_OPENWEATHER_API_KEY` with your OpenWeather API key
3. Run with Docker:

```bash
docker-compose up -d
```

## Environment Variables

See `.env.example` for all available configuration options.
