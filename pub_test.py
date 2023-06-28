import pika
import ssl

rabbit_opts = {
    'host': 'localhost',
    'port': 15671,
    'user': 'test',
    'password': 'test',
}

rabbit_queue_opts = {
    'queue': 'python_ssl',
    'message': 'Hello SSL World :)'
}

context = ssl.create_default_context(cafile="./certificates/ca_certificate.pem")
context.load_cert_chain("./certificates/client_localhost.localdomain_certificate.pem",
                        "./certificates/client_localhost.localdomain_key.pem")
ssl_options = pika.SSLOptions(context, "localhost")

parameters = pika.ConnectionParameters(host=rabbit_opts['host'],
                                       port=rabbit_opts['port'],
                                       credentials=pika.PlainCredentials(rabbit_opts['user'], rabbit_opts['password']),
                                       ssl_options=ssl_options)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue_opts['queue'])

    channel.basic_publish(exchange='',
                          routing_key=rabbit_queue_opts['queue'],
                          body=rabbit_queue_opts['message'])

    print(" [x] Sent '" + rabbit_queue_opts['message'] + "!'")

    connection.close()
except BaseException as e:
    print(str(e), e.__class__.__name__)

