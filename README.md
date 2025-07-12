# MP4 to MP3 Converter Microservice

A scalable microservice architecture for converting MP4 video files to MP3 audio files, built with Python, Flask, and deployed on Kubernetes.

## Architecture Overview

This project consists of four main microservices:

- **Gateway Service**: Entry point for all API requests, handles routing and authentication
- **Authentication Service**: Manages user authentication and JWT token generation
- **Converter Service**: Processes MP4 to MP3 conversion using MoviePy
- **Notification Service**: Sends email notifications when conversion is complete

### System Components

- **RabbitMQ**: Message broker for asynchronous processing
- **MongoDB**: Document database for storing video and audio files (GridFS)
- **MySQL**: Relational database for user management
- **Kubernetes**: Container orchestration platform

## Features

- **JWT Authentication**: Secure user authentication with token-based access
- **Asynchronous Processing**: Queue-based video processing for scalability
- **File Storage**: GridFS for efficient large file storage
- **Email Notifications**: Automatic notifications when conversion is complete
- **Scalable Architecture**: Kubernetes deployment with auto-scaling capabilities
- **Admin Control**: Admin-only upload and download permissions

## Project Structure

```
src/
├── auth/                    # Authentication Service
│   ├── Dockerfile
│   ├── server.py
│   ├── init.sql
│   └── manifests/
│       ├── configmap.yaml
│       ├── deploy.yaml
│       └── service.yaml
├── converter/               # Video Conversion Service
│   ├── Dockerfile
│   ├── consumer.py
│   ├── requirements.txt
│   ├── convert/
│   │   └── to_mp3.py
│   └── manifests/
│       ├── configmap.yaml
│       └── converter-deploy.yaml
├── gateway/                 # API Gateway Service
│   ├── Dockerfile
│   ├── server.py
│   ├── requirements.txt
│   ├── auth_svc/
│   ├── storage/
│   └── manifests/
│       ├── configmap.yaml
│       ├── deploy.yaml
│       ├── service.yaml
│       └── ingress.yaml
├── notification/            # Email Notification Service
│   ├── Dockerfile
│   ├── consumer.py
│   ├── requirements.txt
│   ├── send/
│   │   └── email.py
│   └── manifests/
│       ├── configmap.yaml
│       └── notification-deploy.yaml
└── rabbitmq/               # Message Queue Configuration
    └── manifests/
        ├── configmap.yaml
        ├── service.yaml
        ├── statefulset.yaml
        ├── pvc.yaml
        └── ingress.yaml
```

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube for local development)
- kubectl configured
- MySQL database
- MongoDB database
- SMTP email service (Gmail recommended)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mp4-to-mp3-converter
```

### 2. Environment Variables

Create the following Kubernetes secrets:

#### Auth Service Secret
```bash
kubectl create secret generic auth-secret \
  --from-literal=MYSQL_PASSWORD=your_mysql_password \
  --from-literal=JWT_SECRET=your_jwt_secret
```

#### Gateway Service Secret
```bash
kubectl create secret generic gateway-secret \
  --from-literal=MONGO_USERNAME=your_mongo_username \
  --from-literal=MONGO_PASSWORD=your_mongo_password
```

#### Converter Service Secret
```bash
kubectl create secret generic converter-secret \
  --from-literal=MONGO_USERNAME=your_mongo_username \
  --from-literal=MONGO_PASSWORD=your_mongo_password
```

#### Notification Service Secret
```bash
kubectl create secret generic notification-secret \
  --from-literal=EMAIL_ADDRESS=your_email@gmail.com \
  --from-literal=EMAIL_PASSWORD=your_app_password
```

#### RabbitMQ Secret
```bash
kubectl create secret generic rabbitmq-secret \
  --from-literal=RABBITMQ_DEFAULT_USER=admin \
  --from-literal=RABBITMQ_DEFAULT_PASS=admin123
```

### 3. Database Setup

#### MySQL Database
Run the initialization script:
```bash
mysql -u root -p < src/auth/init.sql
```

#### MongoDB
Ensure MongoDB is running and accessible. The application will create necessary collections automatically.

### 4. Build Docker Images

```bash
# Build Auth Service
cd src/auth
docker build -t rahul226/auth:latest .

# Build Gateway Service
cd ../gateway
docker build -t rahul226/gateway:latest .

# Build Converter Service
cd ../converter
docker build -t rahul226/converter:latest .

# Build Notification Service
cd ../notification
docker build -t rahul226/notification:latest .
```

### 5. Deploy to Kubernetes

```bash
# Deploy RabbitMQ
kubectl apply -f src/rabbitmq/manifests/

# Deploy Auth Service
kubectl apply -f src/auth/manifests/

# Deploy Gateway Service
kubectl apply -f src/gateway/manifests/

# Deploy Converter Service
kubectl apply -f src/converter/manifests/

# Deploy Notification Service
kubectl apply -f src/notification/manifests/
```

### 6. Configure Ingress

Add the following to your `/etc/hosts` file:
```
<minikube-ip> mp3converter.com
<minikube-ip> rabbitmq-manager.com
```

## API Documentation

### Authentication

#### Login
```http
POST /login
Authorization: Basic <base64(email:password)>
```

**Response:**
```json
{
  "token": "jwt_token_here"
}
```

### File Operations

#### Upload Video
```http
POST /upload
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

file: <mp4_file>
```

**Response:**
```json
{
  "message": "Success"
}
```

#### Download MP3
```http
GET /download?fid=<file_id>
Authorization: Bearer <jwt_token>
```

**Response:** MP3 file download

## Workflow

1. **User Authentication**: User logs in with credentials
2. **File Upload**: Admin uploads MP4 file via gateway
3. **Queue Processing**: File metadata sent to RabbitMQ video queue
4. **Conversion**: Converter service processes MP4 to MP3
5. **Storage**: Converted MP3 stored in MongoDB GridFS
6. **Notification**: Email sent to user with file ID
7. **Download**: User downloads MP3 using file ID

## Docker Images

The project uses the following Docker images:

- `rahul226/auth:latest` - Authentication service
- `rahul226/gateway:latest` - API Gateway
- `rahul226/converter:latest` - Video converter
- `rahul226/notification:latest` - Email notification service
- `rabbitmq:3-management` - RabbitMQ with management UI

## Configuration

### ConfigMaps

Each service has its own ConfigMap for environment-specific configuration:

- **auth-configmap**: Database connection settings
- **gateway-configmap**: Service addresses
- **converter-configmap**: Queue names
- **notification-configmap**: Queue configuration

### Scaling

The deployment configurations support horizontal scaling:

- **Auth Service**: 3 replicas
- **Gateway Service**: 3 replicas
- **Converter Service**: 4 replicas
- **Notification Service**: 4 replicas
- **RabbitMQ**: 3 replicas (StatefulSet)

## Monitoring

### RabbitMQ Management UI
Access the RabbitMQ management interface at:
```
http://rabbitmq-manager.com
```

### Application Logs
View service logs:
```bash
kubectl logs -f deployment/auth-deployment
kubectl logs -f deployment/gateway-deployment
kubectl logs -f deployment/converter-deployment
kubectl logs -f deployment/notification-deployment
```
