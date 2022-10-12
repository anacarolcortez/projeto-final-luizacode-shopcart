<h1>PROJETO FINAL LUIZA < CODE > 5ª EDIÇÃO CARRINHO DE COMPRAS </h1> 
​
<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white"/>


> Status do Projeto: Finalizado :heavy_check_mark:

### Tópicos 

:small_blue_diamond: [Descrição do projeto](#descrição-do-projeto)
​
:small_blue_diamond: [Funcionalidades](#funcionalidades-snake)
​
:small_blue_diamond: [Pré-requisitos](#pré-requisitos)
​
:small_blue_diamond: [Como rodar a aplicação](#como-rodar-a-aplicação-arrow_forward)
​
:small_blue_diamond: [Deploy](#deploy-cloud)
​
:small_blue_diamond: [Segurança](#segurança-lock)
​
:small_blue_diamond: [Equipe](#desenvolvedoras-octocat)
 

## Descrição do projeto 

<p align="justify">
  Desenvolvimento de APIs Rest em Python de um carrinho de compras, utilizando o framework FastAPI e MongoDB para banco de dados. Para disponibilizar a aplicação utilizamos servidor Uvicorn e Heroku.
</p>

## Funcionalidades :snake:

:heavy_check_mark: Cadastro de clientes 

:heavy_check_mark: Gerenciamento de clientes

:heavy_check_mark: Cadastro de produtos

:heavy_check_mark: Gerenciamento de produtos  

:heavy_check_mark: Carrinho de compras  


### Detalhamento das features :scroll:
​
Acesse a Wiki do projeto para obter mais informações sobre as funcionalidades criadas: 
​
 [ Wiki do Projeto](https://bit.ly/3Vp6Lw7)


## Pré-requisitos

:warning: [Python](https://www.python.org/downloads/)

:warning: [Mongodb](https://www.mongodb.com/try/download/community)

:warning: [FastApi](https://fastapi.tiangolo.com/)

:warning: [Uvicorn](https://www.uvicorn.org/)

:warning: [Motor](https://motor.readthedocs.io/en/stable/)


## Como rodar a aplicação :arrow_forward:

### Variável de ambiente:
| name_env | value |
|------------|------------|
|DATABASE_URI|connection string Atlas|

### Instalação
* Create venv
    ```
    $ virtualenv venv --python=3.10
    ```
    Linux
    ```
    $ source venv/bin/activate
   ```
   Windows
    ```
    $ .\venv\Scripts\activate
   ```
* Instalar bibliotecas
     ```
     $ pip install -r requirements.txt
     ```
### Execução
  ```
  $ python main.py
   ```
## Deploy :cloud:

O Heroku foi utilizado como provedor web para o deploy da aplicação. Desta forma, é possível conferir e testar as rotas criadas por meio do OpenAPI (Swagger) diretamente no link:
​
[ https://luizacode5-shoppingcart.herokuapp.com/docs](https://luizacode5-shoppingcart.herokuapp.com/docs#/)


## Segurança :lock:
​
Algumas rotas da API foram protegidas com autenticação básica.
Para criar um usuário e acessar as APIs restritas a clientes, acesse, pelo Swagger, o método POST do endpoint "/clients" e insira as informações solicitadas. Em seguida, faça login no botão "Authorize", utilizando o e-mail e a senha criados.

## Linguagens, dependencias e libs utilizadas :books:
​
* [motor](https://motor.readthedocs.io/en/stable/) 

* [pydantic](https://pydantic-docs.helpmanual.io/)

* [pymongo](https://pymongo.readthedocs.io/en/stable/)

* [uvicorn](https://www.uvicorn.org/)

* [fastapi](https://fastapi.tiangolo.com/)



## Desenvolvedoras :octocat:

Time responsável pelo desenvolvimento do projeto

| [<img src="https://avatars.githubusercontent.com/u/111924977?v=4" width=115><br><sub>Aline Freitas</sub>](https://github.com/aline-freitas) |  [<img src="https://avatars.githubusercontent.com/u/56210395?v=4" width=115><br><sub>Ana Cortez</sub>](https://github.com/anacarolcortez) | [<img src="https://avatars.githubusercontent.com/u/75764138?v=4" width=115><br><sub>Laís Rodrigues</sub>](https://github.com/lais-ches) |  [<img src="https://avatars.githubusercontent.com/u/97643806?v=4" width=115><br><sub>Lilian Cândido</sub>](https://github.com/aguilar-lc) |  [<img src="https://avatars.githubusercontent.com/u/111457321?v=4" width=115><br><sub>Mayara Barbosa</sub>](https://github.com/MayBarbosa) |
| :---: | :---: | :---: | :---: | :---: |
| [<sub>Linkedin</sub>](https://www.linkedin.com/in/aline-cristina-garcia-de-freitas-720161181/) | [<sub>Linkedin</sub>](https://www.linkedin.com/in/ana-c-447047192/) | [<sub>Linkedin</sub>](https://www.linkedin.com/in/la%C3%ADs-rodrigues-70a18b14a/) | [<sub>Linkedin</sub>](https://www.linkedin.com/in/liliancandido/) | [<sub>Linkedin</sub>](https://www.linkedin.com/in/mayara-pereira-barbosa-b98a0163/) |

--------------------------------------------------------------------------------------------------------------------------------------------------------------
Copyright :copyright: 2022 - Projeto Final Shopping Cart Magalu
