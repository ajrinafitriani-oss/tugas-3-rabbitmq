import pika

# 1. Sambungkan ke RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Masukkan nama grup/exchange yang ingin diikuti
nama_exchange = input("Masukkan nama exchange untuk menerima pesan (contoh: A atau B): ")
channel.exchange_declare(exchange=nama_exchange, exchange_type='fanout')

# 3. Buat queue sementara yang otomatis terhapus saat program ditutup
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 4. Hubungkan (bind) queue sementara ini ke exchange pilihan
channel.queue_bind(exchange=nama_exchange, queue=queue_name)

print(f" [*] Menunggu pesan siaran di grup '{nama_exchange}'. Tekan Ctrl+C untuk keluar.")

def terima_pesan(ch, method, properties, body):
    print(f" [x] Pesan diterima: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=terima_pesan, auto_ack=True)
channel.start_consuming()