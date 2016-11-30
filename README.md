# SansanoBot

Bot para Telegram implementado en *python3*. Para poder usarlo, se debe solicitar un token con [BotFather](telegram.me/BotFather), y guardarlo en `secret_token.py`, junto a la id del creador para avisar las fallas del bot:
```python
token = "bot123456:ABCDeFGHiJKLMNOpQRSTuVWXYZ"
owner_id = "123456"
```

Actualmente el bot soporta los siguientes comandos:
* `/minuta [normal|vegetariano|dieta] [hoy]`: Retorna la minuta de la universidad.
* `/clima [hoy]`: Retorna la máxima y la mínima de los *n* días siguientes.
