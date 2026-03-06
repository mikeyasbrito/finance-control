# Aula 04: A Grande Imagem - Clean Architecture + Vertical Slices

Entender a "Big Picture" (o quadro geral) é o que separa um programador que apenas escreve código de um Engenheiro de Software. 

O nosso projeto (`my-own-finance-system`) está construído sob dois grandes pilares de design: **Clean Architecture** (Arquitetura Limpa) cruzada com **Vertical Slices** (Fatias Verticais).

---

## 1. O Pilar das Fatias Verticais (Vertical Slices)

Em vez de organizar o código "horizontalmente" por tipo de arquivo (que é o jeito antigo em frameworks como Django ou Rails):
- 📁 `models/` (todos os models do sistema inteiro misturados)
- 📁 `controllers/` (todas as APIs de usuários, bancos, pagamentos misturadas)

Nós dividimos o sistema em fatias focadas no **Domínio da Aplicação**. No nosso código, isso fica na pasta `src/modules/`.
- 📁 `src/modules/users/` (Tudo sobre o usuário mora aqui. Rotas, banco, regras).
- 📁 `src/modules/transactions/` (Tudo sobre transações financeiras mora aqui).

**A vantagem:** Alta coesão. Se o módulo de Usuário quebrar ou precisar ser extraído, as Transações continuam existindo de forma independente. É um passo em direção a "Micro-serviços", mas dentro de um monólito (Modular Monolith).

---

## 2. O Pilar da Clean Architecture (A Cebola)

Dentro de cada "Fatia" (ex: `src/modules/users/`), o código não é uma maçaroca. Ele é protegido por **Camadas** (como uma cebola). A regra inquebrável aqui é:
**A camada de fora pode importar e chamar a de dentro, mas a de dentro NUNCA conhece a camada de fora.**

### 🎯 Camada 1: O Núcleo do Sistema (`core/`)
O coração blindado do seu domínio. 
- **O que tem aqui:** Suas Regras Absolutas de Negócio. `Entities` (Entidades como o Objeto `User`), `Value Objects` (como a `Password` e `Email`) e `Exceptions` de domínio (como `InvalidEmailException`).
- **Regra de Ouro:** O código daqui **NÃO PODE** importar bibliotecas web (FastAPI) e nem banco de dados (SQLAlchemy). O `core` tem que rodar rápido (em milissegundos) e de forma pura.

### 🧠 Camada 2: A Orquestração (`use_cases/`)
- **O que tem aqui:** As regras de aplicação (Os Gerentes). 
- **Exemplo de fluxo:** O roteiro diz: *"Pegue os DTOs -> Peça ao repositório para verificar unicidade -> Instancie a Entidade principal -> Mande o repositório salvar -> Envie um e-mail"*.
- **Como funciona:** O Use Case importa as Entidades do `core/` para validar as regras, mas ele ainda não importa o SQL. Ele depende apenas de *Abstrações/Interfaces* listadas no `core`.

### 🔌 Camada 3: Os Tradutores (`adapters/`)
- **O que tem aqui:** Controllers (Entrada) e Repositories (Saída).
- **O Problema que resolvem:** A web fala JSON HTTP. Seu `core` só fala Python Objects puros. O banco de dados fala comandos SQL. Os adaptadores traduzem os mundos.
- **Na prática:** O `UserController` pega o JSON que veio do FastAPI, converte para um DTO conhecido e joga pro `UseCase`. O `UserRepository` (do SQLAlchemy) recebe a ordem do `UseCase`, traduz a Entidade Python num comando `INSERT INTO` e salva no banco.

### 🌍 Camada 4: O Mundo Externo (`main/` root)
- **O que tem aqui:** O motor do carro. O início de tudo.
- É aqui que instanciamos as bibliotecas reais (`FastAPI`, `Streamlit`, conexões com o `PostgreSQL`) e as "injetamos" (Dependency Injection) nos nossos casos de uso através de rotas ou factories.

---

## 3. Desenhando a Árvore de Diretórios (O Mapa)

Juntando Slices + Clean Architecture, o projeto final se parece com isso:

```text
my-own-finance-system/
├── src/
│   ├── main/                       # Camada 4: Boot do Sistema 🌍
│   │   ├── api/                    # Rotas do FastAPI
│   │   ├── config/                 # Variáveis de Ambiente, Conexões DB
│   │   └── ui/                     # Interface Streamlit
│   │
│   └── modules/                    # As Fatias Verticais 🍰
│       ├── users/                  # Fatia 1: Domínio de Usuários
│       │   ├── core/               # Camada 1: Núcleo 🎯
│       │   │   ├── entities/       # User, e Value Objects (Email, Password)
│       │   │   ├── exceptions.py   # Erros puristas do negócio
│       │   │   ├── interfaces/     # Contratos (IUserRepository)
│       │   │   └── dtos/           # Transferência limpa de dados
│       │   │
│       │   ├── use_cases/          # Camada 2: Orquestradores 🧠
│       │   │   └── register_user.py
│       │   │
│       │   ├── adapters/           # Camada 3: Tradutores 🔌
│       │   │   ├── controllers/    # Recebe request HTTP e chama Use Case
│       │   │   └── repositories/   # Implementa a Interface em SQLAlchemy
│       │   │
│       │   └── routes.py           # Conecta os controllers ao FastAPI
│       │
│       └── transactions/           # Fatia 2: Domínio Financeiro
│           ├── core/               # ... Mesma estrutura recursivamente
│           └── use_cases/
│
├── tests/
│   ├── unit/                       # TDD Rápido (Foca no `core/`)
│   ├── integration/                # TDD Médio (Foca nos `adapters/`)
│   └── e2e/                        # TDD Lento (Foca na API inteira rodando)
│
└── pyproject.toml                  # Gerenciamento de dependências
```

---

## Conclusão: Por que todo esse trabalho?

**Para que o projeto seja à prova de bala e mutável no longo prazo.** 
Se amanhã você decidir trocar o banco de dados (de PostgreSQL para MongoDB), você altera apenas o arquivo dentro de `adapters/repositories/`. A camada `core/` das entidades e regras do usuário (senhas de 12 caracteres, emails válidos) permanece intocada, sem precisar reescrever nem testar de novo!
