import pika
import json


connection =pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel =  connection.channel()

queue = channel.queue_declare('order_report')
print(queue)
queue_name = queue.method.queue
print(queue_name,"................")

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report'
)

def callback(ch,method,properties,body):
    payload = json.loads(body)
    print('[x] Genarating report')
    print('[x] Done')
    print(
        f"""
        ID: {payload['id']}
        user_email: {payload['user_email']}
        Product : {payload['product']}
        quantity: {payload['quantity']}
        """
    )
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(on_message_callback=callback,queue=queue_name)
print('[*] Waiting for Report message. To exit press Ctrl+z')
channel.start_consuming()