# Sistema Publish-Subscribe (Pyro5)

Sistema com três processos independentes que se comunicam via Pyro5:

- `intermediario.py` — gerencia tópicos, inscrições e encaminha mensagens.
- `publisher.py` — publica mensagens em um tópico.
- `subscriber.py` — inscreve-se em tópicos e recebe mensagens via callback remoto.

A comunicação entre publishers e subscribers ocorre exclusivamente através do intermediário.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

Em terminais separados, nesta ordem:

1. Name Server do Pyro5:

```bash
python -m Pyro5.nameserver
```

2. Intermediário:

```bash
python intermediario.py
```

3. Um ou mais subscribers (id + tópicos de interesse):

```bash
python subscriber.py S1 noticias
python subscriber.py S2 noticias esportes
```

4. Um ou mais publishers:

```bash
# publicação única
python publisher.py P1 noticias "Nova aula disponível."

# ou modo interativo (digite o tópico e a mensagem quando solicitado; "sair" para encerrar)
python publisher.py P1
```

## Fluxo

1. O intermediário sobe e se registra no Name Server como `pubsub.intermediario`.
2. Cada subscriber sobe seu próprio daemon Pyro5, registra-se no intermediário informando a URI do seu callback e se inscreve nos tópicos desejados.
3. Um publisher localiza o intermediário e chama `publicar(id_publisher, topico, mensagem)`.
4. O intermediário encaminha a mensagem, via callback remoto, a todos os subscribers inscritos no tópico:

```
[Mensagem recebida] Tópico: noticias | Publisher: P1 | Mensagem: Nova aula disponível.
```

O publisher nunca conhece os subscribers, e os subscribers nunca conhecem os publishers — toda a comunicação passa pelo intermediário.
