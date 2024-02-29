# Desafio Nodejs Moniari

## Descrição

Este projeto foi criado para testar seu conhecimento em tecnologias web de back-end, especificamente no python, APIs Rest e serviços desacoplados.

## Tarefa
O objetivo deste exercício é criar uma API simples usando python (Fastapi) para permitir que os usuários consultem cotações de ações.
O projeto consiste em dois serviços separados:

* Uma API voltada para o usuário que receberá solicitações de usuários registrados pedindo informações sobre cotações.
* Um serviço agregador de ações interno que consulta APIs externas para recuperar as informações de cotações solicitadas.

## Requisitos mínimos

### Serviço API

* Os endpoints no serviço API devem exigir autenticação (não devem ser permitidas solicitações anônimas). Cada solicitação deve ser autenticada via Basic Authentication (exemplo: `Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==` onde o token é o Base64 do username:senha).

* Quando um usuário faz uma solicitação para obter uma cotação de ação (chama o endpoint de ação no serviço de api), se uma ação for encontrada, ela deve logar no console o usuário que faz a solicitação e a ação solicitada.

* A resposta retornada pelo serviço API deve ser assim:
`GET /stock?q=aapl.us`
```
{
  "simbolo": "AAPL.US",
  "nome_da_empresa": "APPLE",
  "cotacao": 123
}
```
O valor da cotação deve ser obtido do campo `close` retornado pelo serviço de ações.

* Todas as respostas dos endpoints devem estar no formato JSON.

### Serviço de Ações

* Assuma que este é um serviço interno, então solicitações para endpoints neste serviço não precisam ser autenticadas.
* Quando uma solicitação de ação é recebida, este serviço deve consultar uma API externa para obter as informações da ação. Para este desafio, use esta API: `https://stooq.com/q/l/?s={codigo_da_acao}&f=sd2t2ohlcvn&h&e=csv`.
* Note que `{codigo_da_acao}` acima é um parâmetro que deve ser substituído pelo código da ação solicitada.
* Você pode ver uma lista de códigos de ações disponíveis aqui: https://stooq.com/t/?i=518

### Arquitetura
![Architecture Diagram](arquitetura.png)
1. Um usuário faz uma solicitação pedindo a cotação atual da ação da Apple: GET /stock?q=aapl.us
2. O serviço API chama o serviço de ações para recuperar as informações da ação solicitada
3. O serviço de ações delega a chamada para a API externa, analisa a resposta e retorna as informações de volta para o serviço API.
4. Os dados são formatados e retornados ao usuário.


