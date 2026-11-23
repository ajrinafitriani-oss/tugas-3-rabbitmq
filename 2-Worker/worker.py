import pika, time

# 1. Sambungkan ke RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Tanya nama saluran (queue)
nama_queue = input("Masukkan nama queue (contoh: workQ): ")
channel.queue_declare(queue=nama_queue, durable=True)
channel.basic_qos(prefetch_count=1)

print(f" [*] Menunggu tugas di '{nama_queue}'. Tekan Ctrl+C untuk berhenti.")

# 3. Fungsi hitung mundur saat angka diterima
def kerjakan_tugas(ch, method, properties, body):
    angka = int(body.decode())
    print(f" [x] Menerima angka: {angka}")

    for i in range(angka, 0, -1):
        print(i, end=" ", flush=True)
        time.sleep(1)
    print("\nDone Computing!")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=nama_queue, on_message_callback=kerjakan_tugas)
channel.start_consuming()