import pika

# 1. Sambungkan ke RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Input tujuan dan kumpulan angka
tujuan = input("Tujuan Queue (contoh: workQ): ")
channel.queue_declare(queue=tujuan, durable=True)

pesan = input("Masukkan angka dipisah koma (contoh: 5,3,4,6): ")

# 3. Kirim angka satu per satu
for angka in pesan.split(','):
    angka_bersih = angka.strip()
    channel.basic_publish(exchange='', routing_key=tujuan, body=angka_bersih)
    print(f" [v] Terkirim: {angka_bersih}")

connection.close()