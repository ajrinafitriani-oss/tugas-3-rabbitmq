import pika

# 1. Sambungkan ke RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

print("=== APLIKASI BROADCASTER ===")
print("Ketik 'exit' pada Tujuan Broadcast jika ingin selesai.\n")

while True:
    # 2. Masukkan nama grup/exchange (misal: A atau B)
    tujuan = input("Tujuan Broadcast / Nama Exchange (contoh: A atau B): ")
    if tujuan.lower() == 'exit':
        break

    # Deklarasikan exchange bertipe 'fanout'
    channel.exchange_declare(exchange=tujuan, exchange_type='fanout')

    # 3. Masukkan pesan teks yang ingin disiarkan
    pesan = input("Pesan yang akan disiarkan: ")

    # 4. Kirim pesan ke exchange (routing_key dikosongkan)
    channel.basic_publish(exchange=tujuan, routing_key='', body=pesan)
    print(f" [v] Berhasil siaran ke grup '{tujuan}': {pesan}\n")

connection.close()
print("Koneksi diputus (Disconnected).")