# Projeto Dev Web 2, Back-end com FastAPI e MongoDB

## Inicialização Rápida

```bash
docker-compose up
```

Este comando inicia o banco de dados e a API web.

## Testando a API

Acesse o Swagger UI: http://localhost:8000/docs

Aqui você pode visualizar e testar todos os endpoints da API.

## Encerrando

Pressione `Ctrl+C` no terminal ou execute:

```bash
docker-compose down
```

## Notas

- Portas utilizadas: 8000 (API) e 27017 (MongoDB)
- Para reconstruir após mudanças: `docker-compose up --build`
