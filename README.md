# Eventex

Sistema de eventos encomendado pela Morena.

## Como desenvolver?

1. Clone o repositório.
2. Crie o virtualenwrapper com o python 3.x
3. Instale as dependências.
4. Configure a instância com o .env
5. Execute os testes.

```console
git clone  git@github.com:alessandroanjos/eventex.git wttd
cd wttd
mkvirtualenv wttd
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test 
```

## Como fazer o deploy?

1. Crie uma instância no heroku.
2. Envie as configuracoes para o heroku.
3. Defina uma SECRE_KEY segura para a instancia.
4. Defina DEBUG=False
5. Configure o servico de e-mail
6. Envie o código para o Heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# configuro o e-mail
git push heroku master --force
```