import pika
import ssl

rabbit_opts = {
    'host': '127.0.0.1',
    'port': 15671,
    'user': 'test',
    'password': 'test',
}

rabbit_queue_opts = {
    'queue': 'python_ssl'
}

context = ssl.create_default_context(cafile="./certificates/ca_certificate.pem")
context.load_cert_chain("./certificates/client_localhost.localdomain_certificate.pem",
                        "./certificates/client_localhost.localdomain_key.pem")
ssl_opts = pika.SSLOptions(context, "localhost")
parameters = pika.ConnectionParameters(host=rabbit_opts['host'],
                                       port=rabbit_opts['port'],
                                       credentials=pika.PlainCredentials(rabbit_opts['user'], rabbit_opts['password']),
                                       # ssl=True,
                                       ssl_options=ssl_opts)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=rabbit_queue_opts['queue'])

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


    channel.basic_consume(rabbit_queue_opts['queue'],
                          callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

except BaseException as e:
    print(str(e), e.__class__.__name__)

