# Project Setup and Running Instructions

## Requirements
- Docker Engine 19.03.0+
- Docker Compose 1.27.0+
- At least 2GB free RAM
- Microsoft API credentials

## Environment Setup
1. Ensure Docker and Docker Compose are installed on your system
2. Clone the project repository
3. Create a `.env` file with the following Microsoft credentials:
   ```
   MS_API_KEY=your_api_key
   MS_CLIENT_ID=your_client_id 
   MS_CLIENT_SECRET=your_client_secret
   MS_TENANT_ID=your_tenant_id
   ```

## Build and Start Services
1. Open terminal in project root directory
2. Run the following commands:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
   This will start:
   - Web API service on port 5000
   - Redis service on port 6379 
   - Celery worker

## API Endpoints

### Microsoft Data Collection