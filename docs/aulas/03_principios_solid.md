# Aula 03: Princípios SOLID na Clean Architecture

## 🎯 O que é SOLID?
SOLID é um acrônimo para cinco princípios de design orientado a objetos que ajudam a criar softwares fáceis de manter e evoluir. Na **Clean Architecture**, esses princípios são aplicados para garantir que as camadas permaneçam independentes.

---

## 1. S - Single Responsibility Principle (SRP)
> "Uma classe deve ter apenas um motivo para mudar."

**No nosso projeto:**
A entidade `User` é responsável apenas por validar os dados fundamentais do usuário. Se precisarmos mudar a forma como as senhas são criptografadas, não mudamos a entidade, mas sim um serviço externo ou o caso de uso.

---

## 2. O - Open/Closed Principle (OCP)
> "Aberto para extensão, mas fechado para modificação."

**Exemplo Prático:**
Se o sistema financeiro começar a aceitar diferentes moedas (BRL, USD, BTC), o código que calcula o saldo total não deve ter um `if/else` gigante para cada moeda. Devemos criar uma estrutura onde novas moedas possam ser adicionadas sem tocar no código de cálculo base.

---

## 3. L - Liskov Substitution Principle (LSP)
> "Subtipos devem ser substituíveis por seus tipos base."

**Exemplo Prático:**
Se tivermos uma classe base `Transaction`, todas as suas variações (`Income`, `Expense`, `Transfer`) devem se comportar de forma que o sistema não "quebre" ao tratá-las genericamente como uma transação.

---

## 4. I - Interface Segregation Principle (ISP)
> "Clientes não devem ser forçados a depender de interfaces que não utilizam."

**Exemplo Prático:**
No nosso `UserRepository`, não colocaremos métodos de "envio de e-mail de marketing", mesmo que o usuário seja o alvo. Separamos em interfaces distintas para que o banco de dados não dependa de regras de marketing.

---

## 5. D - Dependency Inversion Principle (DIP)
> "Dependa de abstrações, não de implementações."

**Este é o pilar da Clean Architecture:**
As regras de negócio (camada `core`) definem **Interfaces** (contratos). As camadas externas (camada `adapters`) implementam esses contratos. 
*Ex: O Domínio diz "eu preciso salvar um usuário", e o SQL Repository diz "eu sei salvar usuários em SQL".*

---

## 🛠️ Exercício de Reflexão:
Olhe para o seu método `__post_init__` na classe `User`. 
1. Ele viola o SRP se tiver muita lógica? 
2. Como a delegação para métodos como `_validate_email()` ajuda a manter o SRP vivo?

---
*Aula gerada por: Gemini CLI (Mentor Técnico)*
