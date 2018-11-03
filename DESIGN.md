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
- [WebSocket](#websocket)
    - [Conversation Topics](#conversation-topics)
    - [Message Topics](#message-topics)
    - [Insight Topics](#insight-topics)

# Models
## User
Collection: `users`

- `_id` (String)
- `username` (String)
- `name` (String)
- `profile_picture_path` (String)
- `age` (Integer)
- `location` (String)

## Meme
Collection: `memes`

- `_id` (String)
- `image_path` (String)

## Meme Rating
Collection `meme_ratings`

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

Status: Written

Request:

- `user`: User to create

Response:

- `user`: Created user

### Get User
GET `/api/users/<user id>`

Status: written

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

Status: Written

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


# WebSocket
## Conversation Topics
### New Conversation Topic
Topic: `/users/<user id>/new_conversations`

Description: Receives a message when a new conversation is started with the user.

Who Subscribes: A single user

Payload:

- `conversation`: New conversation

## Message Topics
### New Message Topic
Topic: `/conversations/<conversation id>/new_message`

Description: Receives a message when a new message is sent in a conversation.

Who Subscribes: Both users in a conversation

Payload:

- `message`: New message

## Insight Topics
### New Insight Topic
Topic: `/conversations/<conversation id>/user/<user id>/new_insight`

Description: Receives a message when the server finds an insight for a user in a conversation.

Who Subscribes: Each user in the conversation subscribes to their own topic

Payload:

- `insight`: Insight, schema TBD
