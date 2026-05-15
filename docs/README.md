# Documentação de Diagramas - PetApp Backend

Este diretório contém diagramas em PlantUML que documentam a arquitetura, fluxos e estrutura de dados do PetApp Backend.

## Diagramas Disponíveis

### 1. Fluxo Tutor (`sequence_tutor.plantuml`)

Diagrama de sequência detalhando todas as interações de um usuário Tutor:

- **Cadastro e Login**: Registro com validação e autenticação via JWT
- **Cadastro de Pets**: Adição de informações sobre cada animal
- **Visualização de Contratos**: Lista de contratos com profissionais
- **Acompanhamento de Aulas**: Visualização de aulas agendadas
- **Histórico**: Acesso a relatórios com resumos, notas e mídia

**Fluxo de Dados**:
```
Tutor → Aplicação → Backend API → PostgreSQL
                ↓
            Pydantic (validação)
            JWT (autenticação)
            SQLAlchemy (ORM)
```

### 2. Fluxo Profissional (`sequence_profissional.plantuml`)

Diagrama de sequência detalhando todas as interações de um usuário Profissional:

- **Cadastro**: Registro como profissional com verificação de tipo
- **Criação de Contratos**: Estabelecimento de acordos com tutores
- **Agendamento de Aulas**: Criação de aulas no contrato
- **Check-in/Check-out**: Registro de horários de chegada e saída
- **Relatório de Aula**: Adição de resumo, notas de comportamento e mídia
- **Decremento Automático**: Saldo é reduzido ao finalizar aula
- **Visualização de Histórico**: Acesso a todas as aulas realizadas

**Fluxos Críticos**:
- Validação de tipo PROFISSIONAL antes de criar contratos (403 Forbidden se TUTOR)
- Desconto automático do saldo ao fazer checkout
- Transações ACID para garantir consistência

### 3. Esquema de Banco de Dados (`database_schema.plantuml`)

Diagrama Entidade-Relacionamento (ER) mostrando:

#### Entidades

- **Usuario**: Usuários do sistema (TUTOR ou PROFISSIONAL)
  - Chaves: email (unique), senha_hash (bcrypt)
  
- **Pet**: Animais de estimação dos tutores
  - Relacionamento: Um tutor possui muitos pets
  
- **Contrato**: Acordo entre tutor e profissional
  - Rastreia total de aulas e saldo disponível
  - Relacionamento: Um tutor tem muitos contratos, Um profissional tem muitos contratos
  
- **Aula**: Sessões de adestramento
  - Status: AGENDADA, REALIZADA, CANCELADA
  - Relacionamento: Um contrato gera muitas aulas, Um pet participa de muitas aulas

#### Relacionamentos

```
Usuario (1) ---> (N) Pet (tutores)
Usuario (1) ---> (N) Contrato (como tutor)
Usuario (1) ---> (N) Contrato (como profissional)
Pet (1) ---> (N) Aula
Contrato (1) ---> (N) Aula
```

### 4. Arquitetura em Camadas (`architecture_layers.plantuml`)

Diagrama mostrando a organização em camadas do backend:

```
┌─────────────────┐
│  Flutter App    │ ← Cliente
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────────────────────┐
│   CAMADA 1: Rotas FastAPI       │ (main.py)
├─────────────────────────────────┤
│   CAMADA 2: Autenticação JWT    │ (auth.py)
├─────────────────────────────────┤
│   CAMADA 3: Validação Pydantic  │ (schemas.py)
├─────────────────────────────────┤
│   CAMADA 4: Lógica CRUD         │ (crud.py)
├─────────────────────────────────┤
│   CAMADA 5: ORM SQLAlchemy      │ (models.py)
├─────────────────────────────────┤
│   CAMADA 6: Conexão DB          │ (database.py)
└────────┬────────────────────────┘
         │ SQL
         ↓
    PostgreSQL 15
```

**Responsabilidades por Camada**:

1. **Rotas HTTP**: Defina endpoints, receba requisições, retorne respostas
2. **Segurança**: Valide JWT, gerencie autorização, proteja dados
3. **Validação**: Garanta tipos corretos, formatos válidos, dados sanitizados
4. **Lógica**: Implemente regras de negócio, operações CRUD, cálculos
5. **ORM**: Mapeie objetos para tabelas, gerencie relacionamentos
6. **Conexão**: Mantenha pool de conexões, execute queries SQL

### 5. Fluxo de Requisições HTTP (`api_flow.plantuml`)

Diagrama de sequência mostrando o fluxo interno de uma requisição:

**Exemplo: POST /usuarios/**
```
Cliente
  ↓
FastAPI Router (validação básica)
  ↓
Pydantic Schemas (valida tipos, formatos, restrições)
  ↓
CRUD Operations (lógica: hash de senha, negócio)
  ↓
SQLAlchemy ORM (mapping para tabelas)
  ↓
PostgreSQL (executa INSERT)
  ↓
Response serialization (JSON)
  ↓
Cliente (201 Created)
```

---

## Como Visualizar os Diagramas

### Online (Recomendado)

1. Acesse http://www.plantuml.com/plantuml/uml/
2. Cole o conteúdo de qualquer arquivo `.plantuml`
3. O diagrama será gerado automaticamente

### VS Code

1. Instale a extensão "PlantUML" (jgraph.plantuml-visual)
2. Abra qualquer arquivo `.plantuml`
3. Clique no ícone de visualização ou pressione `Alt+D`

### Exportar para PNG/SVG

**Usando PlantUML Online**:
1. Gere o diagrama
2. Clique em "Descargar PNG" ou "Descargar SVG"

**Usando CLI** (se PlantUML instalado localmente):
```bash
plantuml docs/sequence_tutor.plantuml -o ../images/
plantuml docs/database_schema.plantuml -tsvg
```

---

## Convenções Usadas

### Cores e Estilos

- **Ator (Actor)**: Usuário/Cliente
- **Participant**: Sistema, API, Banco
- **Component**: Módulo/Arquivo Python
- **Entity**: Tabela do banco de dados
- **Database**: PostgreSQL

### Setas

- `→` ou `->`: Requisição/chamada normal
- `←` ou `<--`: Retorno/resposta
- `●`: Mensagem com ativação
- `∥`: Chamada assíncrona
- `⊗`: Fim de ativação

### Anotações

- `note` com `left/right/top/bottom`: Explicações adicionais
- `==` e `== Seção ==`: Separadores de seções
- `...`: Continuação/omissão de passos

---

## Manutenção dos Diagramas

Quando o código-fonte muda:

1. **Novo Endpoint**: Adicione na `sequence_*` correspondente
2. **Novo Campo**: Atualize `database_schema.plantuml`
3. **Nova Camada**: Modifique `architecture_layers.plantuml`
4. **Mudança de Fluxo**: Atualize `api_flow.plantuml`

Todos os diagramas devem ser sincronizados com:
- `app/main.py` (rotas)
- `app/models.py` (entidades)
- `app/schemas.py` (validação)
- `app/crud.py` (operações)
- `app/auth.py` (autenticação)

---

## Referências

- [PlantUML Docs](https://plantuml.com/pt/)
- [PlantUML Sequence Diagram](https://plantuml.com/pt/sequence-diagram)
- [PlantUML Entity Relationship](https://plantuml.com/pt/ie-diagram)
- [PlantUML Component Diagram](https://plantuml.com/pt/component-diagram)

---

## Próximas Iterações

Diagramas que podem ser adicionados no futuro:

- Diagrama de Estados das Aulas (AGENDADA → REALIZADA → CANCELADA)
- Fluxo de Erros (tratamento de exceções)
- Diagrama de Deployment (produção)
- Diagrama de Permissões (RBAC)
- Performance & Escalabilidade
