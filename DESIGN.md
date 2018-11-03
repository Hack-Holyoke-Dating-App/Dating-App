# Design
Dating app design.

# Table Of Contents
- [Models](#models)
    - [User](#user)
    - [Meme](#meme)
    - [Meme Rating](#meme-rating)
    - [Conversation](#conversation)
    - [Message](#message)
    - [User Topic](#user-topic)
- [API](#api)
    - [User Endpoints](#user-endpoints)
    - [Meme Endpoints](#meme-endpoints)
    - [Meme Rating Endpoints](#meme-rating-endpoints)
    - [Conversation Endpoints](#conversation-endpoints)
    - [Message Endpoints](#message-endpoints)

# Models
## User
Collection: `users`

- `_id` (String)
- `name` (String)
- `Age` (Integer)
- `location` (String)

## Meme
Collection: `memes`

- `_id` (String)

## Meme Rating
Collection `memes_rating`

- `_id` (String)
- `meme_id` (String)
- `user_id` (String)
- `liked` (Boolean)

## Conversation
Collection: `conversations`

- `_id` (String)
- `user_a_id` (String)
- `user_b_id` (String)

## Message
Collection: `messages`

- `_id` (String)
- `sending_user_id` (String)
- `time` (Time)
- `text` (String)

## User Topic
Collection: `user_topics`

- `_id` (String)
- `user_id` (String)
- `topic` (String)
- `frequency` (Integer)

# API
## User Endpoints
### Create User
POST `/api/users`

Request:

- `user`: User to create

Response:

- `user`: Created user

### Get User
GET `/api/users/<user id>`

Request: None

Response:

- `user`: Requested user

## Meme Endpoints
### Get Memes
GET `/api/memes`

Request: None

Response:

- `memes`: Array of memes

## Meme Rating Endpoints
### Rate Meme
POST `/api/memes/<meme id>`

Request:

- `meme_rating`: Meme rating

Response: None

## Conversation Endpoints
### Create Conversation
POST `/api/conversations`

Request: 

- `conversation`: Conversation to create

Response:

- `conversation`: Created conversation

## Message Endpoints
### Send Message
POST `/api/conversations/<coversation id>/messages`

Request:

- `message`: Message to send

Response: None

### Get Messages
GET `/api/conversations/<conversation id>/messages`

Request: None

Response:

- `messages`: Array of messages in conversation


