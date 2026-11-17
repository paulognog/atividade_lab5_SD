import threading

import rpyc
from rpyc.utils.server import ThreadedServer


class ReservationService(rpyc.Service):
    """Servico exposto ao cliente via RPyC.

    Mantém o estado compartilhado (assentos) na memoria do
    servidor, protegido por um lock de threading para controle
    de concorrencia.
    """

    def __init__(self):
        self._seats = {f"A{i}": "Livre" for i in range(1, 11)}
        self._lock = threading.Lock()

    def exposed_listar_assentos(self):
        """Retorna uma copia do status atual de cada assento."""
        with self._lock:
            return dict(self._seats)

    def exposed_reservar_assento(self, nome_cliente, assento):
        """Tenta reservar o assento. Sob o lock: apenas um cliente
        ganha se 2 pedirem o mesmo assento ao mesmo tempo."""
        with self._lock:
            if self._seats.get(assento) == "Reservado":
                return "Assento ja ocupado"
            self._seats[assento] = "Reservado"
            return f"Assento {assento} reservado para {nome_cliente}!"


if __name__ == "__main__":
    server = ThreadedServer(
        ReservationService(),
        port=18861,
        protocol_config={"allow_public_attrs": True},
    )
    print("Servidor RPyC ativo na porta 18861")
    server.start()


    
