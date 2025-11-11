import pika, json

def upload(f, fs, channel, access):
    # upload file to mongo  and create a rabbitmq message
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal error: cannot upload file", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],

    }

    try:
        channel.basic_publish(
            exchange='',
            routing_key='video',
            body=json.dumps(message),
            properties= pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    
    except:
        fs.delete(fid)
        return "internal error: cannot queue video for processing", 500
    
    