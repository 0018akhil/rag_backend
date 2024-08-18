# Chat with Any Document API Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
   - [Authentication](#authentication-endpoints)
   - [Documents](#document-endpoints)
   - [Chat](#chat-endpoints)
5. [Models](#models)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Changelog](#changelog)

## Introduction

Welcome to the Chat with Any Document API. This API allows users to upload documents, process them, and engage in chat conversations based on the content of these documents. It uses advanced natural language processing techniques to provide intelligent responses to user queries.

## Base URL

All API requests should be made to:

```
https://documentchat-xi.vercel.app
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to include the JWT token in the Authorization header of your HTTP requests.

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication Endpoints

#### Sign Up

Create a new user account.

- **URL:** `/signup`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Success Response:** `201 Created`
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "user@example.com",
    "is_active": true
  }
  ```

#### Login

Authenticate a user and receive a JWT token.

- **URL:** `/token`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "user@example.com",
    "password": "string"
  }
  ```
- **Success Response:** `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### Document Endpoints

#### Upload Document

Upload a new document to the system.

- **URL:** `/documents/`
- **Method:** `POST`
- **Authentication:** Required
- **Request Body:** `multipart/form-data`
  - `title`: string
  - `file`: file
- **Success Response:** `201 Created`
  ```json
  {
    "id": 1,
    "title": "My Document",
    "index_name": "uuid4-generated-key",
    "upload_date": "2023-08-18T12:34:56Z",
    "owner_id": 1
  }
  ```

#### Get User's Documents

Retrieve a list of documents uploaded by the authenticated user.

- **URL:** `/documents/`
- **Method:** `GET`
- **Authentication:** Required
- **Query Parameters:**
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)
- **Success Response:** `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "My Document",
      "index_name": "uuid4-generated-key",
      "upload_date": "2023-08-18T12:34:56Z",
      "owner_id": 1
    },
    ...
  ]
  ```

### Chat Endpoints

#### Chat with Document

Send a message to chat with a specific document.

- **URL:** `/chat`
- **Method:** `POST`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "document_id": 1,
    "message": "What is the main topic of this document?"
  }
  ```
- **Success Response:** `200 OK`
  ```json
  {
    "reply": "The main topic of this document is..."
  }
  ```

## Models

### User

```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true
}
```

### Document

```json
{
  "id": 1,
  "title": "string",
  "index_name": "string",
  "upload_date": "2023-08-18T12:34:56Z",
  "owner_id": 1
}
```

### ChatMessage

```json
{
  "document_id": 1,
  "message": "string"
}
```

## Error Handling

The API uses conventional HTTP response codes to indicate the success or failure of an API request. In general:

- 2xx range indicate success
- 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, etc.)
- 5xx range indicate an error with our servers

## Rate Limiting

To prevent abuse, the API implements rate limiting. The current limit is 100 requests per hour per user. If you exceed this limit, you'll receive a 429 Too Many Requests response.

## Changelog

### Version 1.0.0 (August 18, 2023)
- Initial release of the API