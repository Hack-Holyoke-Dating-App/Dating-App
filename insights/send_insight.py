def send_insight(socketio, conversation_id, user_id, name, data):
    topic = "/conversations/{}/user/{}/new_insight".format(conversation_id,
                                                           user_id)
    print("SENDING INSIGHT: type: {}, data: {}".format(name, data))

    socketio.emit(topic, {
        'type': name,
        'data': data,
     }, broadcast=True)
