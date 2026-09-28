"""Publisher do sistema publish-subscribe."""
import sys

import Pyro5.api


def conectar_intermediario():
    ns = Pyro5.api.locate_ns()
    return Pyro5.api.Proxy(ns.lookup("pubsub.intermediario"))


def publicar(intermediario, id_publisher, topico, mensagem):
    n_notificados = intermediario.publicar(id_publisher, topico, mensagem)
    print(f"[{id_publisher}] Publicado em '{topico}' -> {n_notificados} subscriber(es) notificado(s)")


def main():
    if len(sys.argv) < 2:
        print("Uso: python publisher.py <id_publisher> [topico mensagem]")
        sys.exit(1)

    id_publisher = sys.argv[1]
    intermediario = conectar_intermediario()

    if len(sys.argv) >= 4:
        topico = sys.argv[2]
        mensagem = " ".join(sys.argv[3:])
        publicar(intermediario, id_publisher, topico, mensagem)
        return

    print(f"[{id_publisher}] Modo interativo. Digite 'sair' para encerrar.")
    while True:
        topico = input("Tópico: ").strip()
        if topico.lower() == "sair":
            break
        if not topico:
            continue
        mensagem = input("Mensagem: ").strip()
        publicar(intermediario, id_publisher, topico, mensagem)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nEncerrando publisher.")
