"""Intermediário (broker) do sistema publish-subscribe."""
import threading

import Pyro5.api


@Pyro5.api.expose
class Intermediario:
    def __init__(self):
        self._lock = threading.RLock()
        self.topicos = {}       # nome_topico -> set(id_subscriber)
        self.subscribers = {}   # id_subscriber -> uri (str) do callback

    def criar_topico(self, nome):
        with self._lock:
            if nome not in self.topicos:
                self.topicos[nome] = set()
                print(f"[Intermediário] Tópico criado: {nome}")
        return True

    def registrar_subscriber(self, id_subscriber, uri_callback):
        with self._lock:
            self.subscribers[id_subscriber] = uri_callback
        print(f"[Intermediário] Subscriber registrado: {id_subscriber}")
        return True

    def inscrever(self, id_subscriber, topico):
        with self._lock:
            if id_subscriber not in self.subscribers:
                raise ValueError(f"Subscriber '{id_subscriber}' não registrado.")
            self.criar_topico(topico)
            self.topicos[topico].add(id_subscriber)
        print(f"[Intermediário] {id_subscriber} inscrito no tópico '{topico}'")
        return True

    def publicar(self, id_publisher, topico, mensagem):
        with self._lock:
            self.criar_topico(topico)
            destinatarios = {
                sid: self.subscribers[sid]
                for sid in self.topicos[topico]
                if sid in self.subscribers
            }

        print(f"[Intermediário] Publisher: {id_publisher} | Tópico: {topico} | Mensagem: {mensagem}")

        for id_subscriber, uri in destinatarios.items():
            self._encaminhar(id_subscriber, uri, topico, id_publisher, mensagem)

        return len(destinatarios)

    def _encaminhar(self, id_subscriber, uri, topico, id_publisher, mensagem):
        try:
            with Pyro5.api.Proxy(uri) as callback:
                callback.receber_mensagem(topico, id_publisher, mensagem)
        except Exception as erro:
            print(f"[Intermediário] Falha ao encaminhar mensagem para {id_subscriber}: {erro}")
            with self._lock:
                self.subscribers.pop(id_subscriber, None)


def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()

    intermediario = Intermediario()
    uri = daemon.register(intermediario)
    ns.register("pubsub.intermediario", uri)

    print("[Intermediário] Pronto e registrado no Name Server como 'pubsub.intermediario'")
    print(f"[Intermediário] URI: {uri}")

    daemon.requestLoop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Intermediário] Encerrando.")
