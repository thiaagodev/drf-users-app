# App de Usuários

Esse é um app de usuários personalizado feito em Django REST Framework, nele eu modifiquei o model padrão de users do Django, adicionando campos como CPF, data de nascimento e outros. Também exclui o campo username, deixando o sistema de login com email e senha, criei funcionalidades relacionadas a conta do usuário, como criar, ativar conta, visualizar, atualizar e deletar dados, com envio de emails para ativar a conta e redefinir a senha usando Celery e RabbitMQ(Message Broker), e todas as funcionalidades com testes automatizados. O login é feito com a lib simple-jwt. 

### O que tem na API?

- Modelo de usuário personalizado 
- Login com email e senha usando JWT
- Funcionalidades da conta do usuário 
- CRUD de endereços do usuário 
- Testes automatizados para todas funcionalidades

### Arquivo ENV necessário para rodar o projeto
Se você desejar clonar esse repositório e rodar na sua máquina para testar, terá de adicionar um arquivo .env na pasta raiz com as seguintes variáveis:

<strong>OBS:</strong> Sugiro que crie uma venv para evitar problemas.

SECRET_KEY=< Secret Key do projeto (pode ser a que o django mesmo gera) >
<br>
EMAIL_HOST=< Host de email (Eu usei o mailtrap para testes) > 
<br>
EMAIL_HOST_USER= < Usuário da conta de email >
<br>
EMAIL_HOST_PASSWORD=< Senha do email >
<br>
EMAIL_PORT=< Porta do provedor >

### E como rodar o projeto?

Depois de clonar o repositório, criar e ativar a venv e configurar devidamente as variáveis ambientes, siga os passos para rodar e testar o projeto:

- pip install -r requirements.txt (Para instalar as libs necessárias)
- python manage.py migrate (Para rodar as migrações do banco de dados)
- python manage.py runserver 

<strong>Pronto! o projeto já deve estar no ar e funcionando corretamente.</strong>
