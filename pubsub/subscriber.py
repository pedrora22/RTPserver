"""Subscriber do sistema publish-subscribe."""
import sys

import Pyro5.api


@Pyro5.api.expose
class SubscriberCallback:
    """Objeto remoto usado pelo intermediário para entregar mensagens."""

    def __init__(self, id_subscriber):
        self.id_subscriber = id_subscriber

    def receber_mensagem(self, topico, id_publisher, mensagem):
        print(f"[Mensagem recebida] Tópico: {topico} | Publisher: {id_publisher} | Mensagem: {mensagem}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python subscriber.py <id_subscriber> <topico1> [topico2 ...]")
        sys.exit(1)

    id_subscriber = sys.argv[1]
    topicos = sys.argv[2:]

    daemon = Pyro5.api.Daemon()
    callback = SubscriberCallback(id_subscriber)
    uri_callback = daemon.register(callback)

    ns = Pyro5.api.locate_ns()
    intermediario = Pyro5.api.Proxy(ns.lookup("pubsub.intermediario"))

    intermediario.registrar_subscriber(id_subscriber, str(uri_callback))
    for topico in topicos:
        intermediario.inscrever(id_subscriber, topico)
        print(f"[{id_subscriber}] Inscrito no tópico: {topico}")

    print(f"[{id_subscriber}] Aguardando mensagens... (CTRL+C para sair)")
    daemon.requestLoop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando subscriber.")
