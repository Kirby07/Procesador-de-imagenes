from celer import Celery
# Configura Celery para usar RabbitMQ como broker

app = Celery('tasks',broker='amqp://guest@localhost//')

    # Opcional: Configuraciones de Celery adicionales

app.conf.update(

result_expires=3600,

)

if __name__ == '__main__':

    app.start()