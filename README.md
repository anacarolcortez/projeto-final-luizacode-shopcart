## [ETAPA 2]

<p>Exercício utilizando MongoDB para integração de dados aos microsserviços web de uma magazine, com Python e FastAPI. O projeto está sendo desenvolvido durante a 5ª edição do LuizaCode, bootcamp promovido pelo Luizalabs, da Magazine Luiza.</p>
<p>Nesta segunda entrega, em 25/set/22, foram criados CRUD (criação, consulta, atualização e exclusão de dados) para clientes, endereços, produtos e carrinho de compras.</p>
<p>Nas próximas entregas, haverá tratamento apropriado de exceções, inclusão de testes unitários e de camada de segurança, com token JWT. Também serão feita refatorações necessárias em conformidade com as boas práticas de arquitetura de software</p>

## Variável de ambiente:
| name_env | value |
|------------|------------|
|DATABASE_URI|connection string Atlas|

## Instalação
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
## Execução
  ```
  $ python main.py
   ```