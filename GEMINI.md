# Contexto do Projeto: My Own Finance System

## Visão Geral do Projeto
Este projeto, `my-own-finance-system`, tem como objetivo ser um sistema de gerenciamento financeiro pessoal.Este projeto tem íntuito de aprendizado, então sempre foque me me responder o por que de cada decisão técnica que você tomar, e sem que possível me deixe o mais a vontade de codar (evite auto-complete, apenas me diga o como fazer e linhas de raciocinio), e por fim, não se preocupe em me dar respostas prontas, apenas me guie, não se poupe de oferecer a melhor solução possível ou a melhor maneira de implementar algo, desde que seja explicado o motivo e a causa esta perfeito.

## Stack
- **Frontend:** Streamlit
- **virtual environment:** poetry
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Authorization:** RBAC
- **Testing:** Pytest
- **Linting:** Flake8
- **Formatting:** Black
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Deployment:** Vercel

## Arquitetura
Vamos desenvolver o sistema utilizando:
- **Clean Architecture**
- **Clean Code** (sempre me corrija caso eu fuja de algujma regra e sempre me explique as regras)
- **Test Driven Development**

# Estrutura de Pastas
meu_projeto/
├── src/
│   ├── core/                      # Camada Interna: Entidades e Regras Globais
│   │   ├── entities/              # Modelos de domínio puro (ex: Usuario, Pedido)
│   │   └── exceptions.py          # Exceções de negócio customizadas
│   │
│   ├── use_cases/                 # Camada de Casos de Uso (Orquestração)
│   │   ├── create_user.py
│   │   ├── process_data.py        # Lógica de transformação de dados
│   │   └── interfaces/            # Portas (Interfaces/Abstrações)
│   │       ├── repository.py      # Definição de como os dados são salvos
│   │       └── external_api.py    # Definição de como dados externos são buscados
│   │
│   ├── adapters/                  # Camada de Interface Adapters (Conversão)
│   │   ├── controllers/           # Recebe a entrada e chama o Use Case
│   │   ├── presenters/            # Formata a saída para a UI/API
│   │   └── repositories/          # Implementação real (SQLAlchemy, BigQuery, Mongo)
│   │       └── sql_repository.py
│   │
│   └── main/                      # Camada Externa (Frameworks & Drivers)
│       ├── api/                   # Rotas do FastAPI, Flask, etc.
│       ├── config/                # Variáveis de ambiente e setup
│       └── composition_root.py    # Onde a Injeção de Dependência acontece
│
├── tests/                         # Testes unitários, integração e E2E
│   ├── unit/
│   └── integration/
├── docker-compose.yml             # Infraestrutura como código
├── Dockerfile

Fique a vontade para me oferecer outras estruturas de pastas que sejam compatíveis e mais viáveis com o projeto.
## Construção e Execução (TODO)
Iremos utilizar o poetry para gerenciamento de dependências e o docker para gerenciamento de containers.

- **Instalação:** poetry install <nome-do-pacote> (sempre instale os pacotes dessa forma)
- **Execução:** docker compose -d up --build
- **Testes:** poetry run pytest --cov=<insira-nome-da-pasta-core> --cov-fail-under=85 (sempre execute os testes dessa forma)

## Convenções de Desenvolvimento
Regras e estilos de código a serem seguidos após a inicialização do projeto:

- **Estilo de Código:** Clean Code
- **Práticas de Teste:** Test Driven Development
- **Contribuição:** Documentar aqui o processo de pull requests e revisões.
- **documentação:** Sempre documente o código utilizando MkDocs, comentários quando necessário e sempre que criar uma nova funcionalidade, documente-a no arquivo README.md.

## Modo de agir
- **Sempre me ofereça raciocinio técnico balanceado com exemplos práticos e simples para que eu possa entender melhor:** Sempre que possível, me ofereça exemplos práticos e simples para que eu possa entender melhor o raciocinio técnico que você está oferecendo.
-**quando eu solicitar qualquer deixa de encerramento, você deve me oferecer para escrever o que foi feito e o que foi aprendido, e por fim, caso eu aceite você escreverá em formato markdown na pasta docs/historico**