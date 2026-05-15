# PetApp Backend

Sistema de gerenciamento de aulas de adestramento para pets. Aplicação desenvolvida para facilitar a comunicação entre tutores e profissionais de adestramento, permitindo agendamento, histórico de aulas e acompanhamento do desenvolvimento de cada pet.

---

## Visão Geral do Projeto

PetApp é um MVP (Produto Mínimo Viável) que resolve o problema de desorganização nas aulas de adestramento de animais de estimação. A plataforma permite que:

- **Tutores** criem perfis de seus pets, visualizem histórico de aulas e acompanhem o progresso
- **Profissionais** gerenciem contratos, agendem aulas e registrem dados sobre o comportamento e evolução dos animais

Este repositório contém o backend da aplicação, desenvolvido com tecnologias modernas de desenvolvimento web e banco de dados.

---

## Stack Tecnológico

### Backend

| Tecnologia | Versão | Função |
|------------|--------|--------|
| **Python** | 3.11 | Linguagem de programação |
| **FastAPI** | 0.109.0 | Framework web assíncrono |
| **SQLAlchemy** | 2.0.25 | ORM (Object-Relational Mapping) |
| **PostgreSQL** | 15 | Banco de dados relacional |
| **Pydantic** | 2.5.3 | Validação de dados e schemas |
| **Passlib** | 1.7.4 | Hashing e verificação de senhas |
| **python-jose** | 3.3.0 | Codificação e decodificação JWT |
| **Bcrypt** | 4.0.1 | Algoritmo de hash de senha |
| **psycopg2** | 2.9.9 | Driver PostgreSQL para Python |
| **Uvicorn** | 0.27.0 | Servidor ASGI |

### Infraestrutura

| Ferramenta | Versão | Propósito |
|-----------|--------|----------|
| **Docker** | Latest | Containerização da aplicação |
| **Docker Compose** | 3.8 | Orquestração de containers |

---

## Arquitetura

### Estrutura do Projeto

```
petapp-backend/
├── app/
│   ├── __init__.py          # Inicialização do pacote
│   ├── main.py              # Rotas principais e configuração da API
│   ├── models.py            # Modelos do banco de dados (ORM)
│   ├── schemas.py           # Schemas Pydantic para validação
│   ├── crud.py              # Operações de banco de dados
│   ├── auth.py              # Autenticação e JWT
│   └── database.py          # Configuração de conexão com BD
├── requirements.txt         # Dependências Python
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração de containers
└── README.md               # Documentação
```

### Padrão Arquitetural

A aplicação segue o padrão em camadas:

1. **Camada de Apresentação (main.py)**
   - Define as rotas HTTP
   - Trata requisições e respostas
   - Valida permissões através de dependências

2. **Camada de Validação (schemas.py)**
   - Define estruturas de dados esperadas (Pydantic)
   - Valida tipos, formatos e restrições
   - Gera documentação automática (OpenAPI)

3. **Camada de Lógica de Negócios (crud.py)**
   - Implementa operações CRUD
   - Contém regras de negócio
   - Gerencia transações

4. **Camada de Dados (models.py, database.py)**
   - Define modelos ORM (SQLAlchemy)
   - Gerencia conexão com banco
   - Mapeia entidades para tabelas

5. **Camada de Segurança (auth.py)**
   - Implementa autenticação JWT
   - Valida tokens
   - Controla autorização

---

## Modelo de Dados

### Entidades Principais

#### Usuario
```
- id: Identificador único
- nome: Nome completo
- email: Email único para login
- senha_hash: Hash da senha (bcrypt)
- telefone: Contato (opcional)
- tipo: TUTOR ou PROFISSIONAL
- criado_em: Data de criação
```

#### Pet
```
- id: Identificador único
- dono_id: Referência ao usuário tutor
- nome: Nome do pet
- raca: Raça (opcional)
- peso: Peso do animal (opcional)
- alergias: Informações sobre alergias (opcional)
- observacoes: Observações adicionais (opcional)
- foto_url: URL da foto do pet (opcional)
```

#### Contrato
```
- id: Identificador único
- tutor_id: Referência ao usuário tutor
- profissional_id: Referência ao usuário profissional
- total_aulas: Total de aulas contratadas
- saldo_aulas: Aulas ainda disponíveis
- ativo: Status do contrato
- criado_em: Data de criação
```

#### Aula
```
- id: Identificador único
- contrato_id: Referência ao contrato
- pet_id: Referência ao pet (opcional)
- data_agendada: Data e hora agendada
- status: AGENDADA, REALIZADA ou CANCELADA
- checkin_hora: Horário de chegada (opcional)
- checkout_hora: Horário de saída (opcional)
- resumo_texto: Relatório da aula (opcional)
- nota_comportamento: Avaliação 1-5 (opcional)
- midia_url: Link para foto/vídeo (opcional)
```

### Relacionamentos

```
Usuario (1) ---> (N) Pet (tutores)
Usuario (1) ---> (N) Contrato (como tutor)
Usuario (1) ---> (N) Contrato (como profissional)
Pet (1) ---> (N) Aula
Contrato (1) ---> (N) Aula
```

---

## Autenticação e Autorização

### Fluxo de Autenticação

1. **Registro**: Usuário cria conta fornecendo nome, email, senha e tipo de perfil
2. **Login**: Usuario fornece email e senha
3. **Validação**: Senha é verificada contra hash bcrypt
4. **Token JWT**: Se válido, recebe um token com duração de 30 minutos
5. **Requisições Autenticadas**: Token é enviado no header `Authorization: Bearer <token>`

### Controle de Acesso

- Rotas públicas: Registro e login
- Rotas protegidas: Requerem token JWT válido
- Controle por tipo de usuário: Alguns endpoints verificam se o usuário é PROFISSIONAL

### Segurança

- Senhas com hash bcrypt (irreversível)
- Tokens JWT com expiração
- Secret key configurável por variável de ambiente
- Algoritmo HS256 para assinatura de tokens

---

## Rotas da API

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/token` | Realiza login e retorna JWT |

### Usuarios

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/usuarios/` | Cria novo usuário | Não |

### Pets

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/pets/` | Cria novo pet | Sim |
| GET | `/pets/` | Lista pets do usuário | Sim |

### Contratos

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/contratos/` | Cria novo contrato (profissional) | Sim |
| GET | `/contratos/` | Lista contratos do usuário | Sim |

### Aulas

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/aulas/` | Agenda nova aula | Sim |
| GET | `/aulas/` | Lista aulas do usuário | Sim |
| POST | `/aulas/{id}/checkin` | Registra chegada | Sim |
| POST | `/aulas/{id}/checkout` | Registra saída e relatório | Sim |

---

## Configuração e Instalação

### Pré-requisitos

- Docker e Docker Compose instalados
- ou Python 3.11+ e PostgreSQL 15+

### Com Docker Compose (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/yurikomuta/petapp-backend.git
cd petapp-backend
```

2. Inicie os containers:
```bash
docker-compose up
```

A API estará disponível em `http://localhost:8000`

A documentação interativa (Swagger) em `http://localhost:8000/docs`

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/yurikomuta/petapp-backend.git
cd petapp-backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
export DATABASE_URL="postgresql://petadmin:petsecret@localhost/petapp_db"
```

5. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

---

## Conceitos e Tecnologias Aplicadas

### FastAPI

Framework web assíncrono e de alto desempenho que oferece:
- Validação automática com Pydantic
- Documentação OpenAPI automática (Swagger)
- Type hints nativos em Python
- Suporte a operações assíncronas

**Aplicação**: Endpoints RESTful com validação automática de requisições e respostas.

### SQLAlchemy (ORM)

Object-Relational Mapping que abstrai as operações de banco de dados:
- Define modelos como classes Python
- Abstrai SQL complexo
- Suporta migrations e versionamento
- Relacionamentos automáticos entre entidades

**Aplicação**: Modelos de Usuario, Pet, Contrato e Aula mapeados para tabelas PostgreSQL.

### Pydantic

Biblioteca para validação de dados e serialização:
- Valida tipos de dados em tempo de requisição
- Gera schemas automáticos
- Suporta validações customizadas
- Converte dados para/de JSON

**Aplicação**: Schemas como `UsuarioCreate`, `PetResponse` garantem dados válidos.

### JWT (JSON Web Tokens)

Padrão para autenticação stateless:
- Token contém payload com informações do usuário
- Assinado com secret key (HS256)
- Pode ser verificado sem consultar banco
- Suporta expiração

**Aplicação**: Usuarios recebem token após login válido, usado em requisições autenticadas.

### Bcrypt

Algoritmo criptográfico para hashing de senhas:
- Irreversível (não há decrypt)
- Adaptativo (fica mais lento com tempo)
- Com salt automático
- Resistente a força bruta

**Aplicação**: Senhas de usuarios são hashadas com bcrypt e nunca armazenadas em texto plano.

### PostgreSQL

Banco de dados relacional robusto e confiável:
- Suporta tipos complexos
- Transações ACID
- Índices para performance
- Relacionamentos integridade referencial

**Aplicação**: Armazena dados de usuarios, pets, contratos e aulas com segurança.

### Docker

Containerização para garantir consistência:
- Ambiente idêntico em desenvolvimento e produção
- Isolamento de dependências
- Fácil distribuição
- Suporte a múltiplos containers

**Aplicação**: Backend (Python/FastAPI) e banco de dados (PostgreSQL) em containers.

---

## Fluxos de Negócio Principais

### Fluxo 1: Cadastro e Login de Usuário

1. Novo usuário acessa a aplicação
2. Fornece email, senha e tipo (TUTOR ou PROFISSIONAL)
3. Backend valida e cria conta com senha hasheada
4. Usuario faz login fornecendo email e senha
5. Backend valida e retorna JWT válido por 30 min
6. Usuário usa token para requisições autenticadas

### Fluxo 2: Cadastro de Pet

1. Tutor autenticado solicita criar novo pet
2. Fornece dados: nome, raça, peso, alergias, etc
3. Backend valida e associa pet ao tutor
4. Pet fica disponível para agendamento de aulas

### Fluxo 3: Contratação de Aulas

1. Profissional autenticado cria contrato
2. Especifica tutor e número de aulas (ex: 10 aulas)
3. Backend cria contrato com saldo igual ao total
4. Tutor pode visualizar contratos ativos
5. Aulas podem ser agendadas contra este contrato

### Fluxo 4: Execução e Registro de Aula

1. Aula é agendada com data e hora específica
2. No dia da aula, profissional faz check-in (registra chegada)
3. Durante a aula, o profissional registra dados do pet
4. Profissional faz check-out informando:
   - Resumo da aula
   - Nota de comportamento (1-5)
   - Foto/video (opcional)
5. Status muda para REALIZADA
6. Saldo de aulas do contrato é decrementado
7. Tutor pode visualizar histórico completo

---

## Extensões Futuras

### Curto Prazo

1. Upload de mídia (fotos e vídeos)
2. Notificações em tempo real
3. Sistema de pagamento integrado
4. Relatórios PDF de progresso

### Médio Prazo

1. Agendamento automático com disponibilidade
2. Sistema de reviews e avaliações
3. Dashboard de analytics
4. Integração com calendar (Google Calendar, Outlook)

### Longo Prazo

1. Marketplace de profissionais
2. Cursos/conteúdo educacional
3. Comunidade e fórum
4. Aplicativo mobile robusto (Flutter)

---

## Tratamento de Erros

A API segue padrões HTTP para retorno de erros:

- **400 Bad Request**: Dados inválidos na requisição
- **401 Unauthorized**: Token ausente ou inválido
- **403 Forbidden**: Usuário sem permissão para ação
- **404 Not Found**: Recurso não encontrado
- **409 Conflict**: Email já cadastrado
- **500 Internal Server Error**: Erro no servidor

Todas as respostas de erro incluem mensagem descritiva para facilitar debug.

---

## Contribuição

Para contribuir com o projeto:

1. Crie uma branch a partir de `main`
2. Realize as alterações necessárias
3. Teste localmente com `docker-compose up`
4. Envie um Pull Request com descrição clara das mudanças

---

## Contato

Desenvolvido para o projeto de adestramento do Rogérin.

Para dúvidas sobre a arquitetura ou implementação, consulte os comentários no código ou abra uma issue no repositório.
