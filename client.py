import rpyc

HOST = "localhost"
PORT = 18861


# Conecta ao servidor
conn = rpyc.connect(HOST, PORT)
service = conn.root

while True:
    print("\n--- Mapa de Assentos ---")
    for assento, status in service.exposed_listar_assentos().items():
        print(f"  {assento}: {status}")


    assento = input("\nAssento desejado (ex: A1): ").strip().upper()
    if assento == "SAIR":
        break
    nome = input("Nome do cliente: ").strip()
    print("  =>", service.exposed_reservar_assento(nome, assento))

conn.close()
print("Cliente encerrado.")


