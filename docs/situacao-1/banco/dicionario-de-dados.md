# BodyTrack: Dicionário de Dados

**SGBD:** PostgreSQL  |  **Banco:** bodytrack

## Tabela `usuario`
Armazena as usuárias cadastradas.

| Campo | Tipo | Tamanho | Obrigatório | Restrições | Descrição |
|---|---|---|---|---|---|
| id | SERIAL | – | Sim | PK | Identificador da usuária |
| nome | VARCHAR | 100 | Sim | – | Nome completo |
| email | VARCHAR | 150 | Sim | UNIQUE | E-mail usado no login |
| senha_hash | VARCHAR | 255 | Sim | – | Hash da senha (nunca a senha em texto) |
| data_nascimento | DATE | – | Não | – | Data de nascimento |
| criado_em | TIMESTAMP | – | Sim | DEFAULT NOW() | Data e hora do cadastro |

## Tabela `registro`
Um registro corporal de uma usuária em uma data.

| Campo | Tipo | Tamanho | Obrigatório | Restrições | Descrição |
|---|---|---|---|---|---|
| id | SERIAL | – | Sim | PK | Identificador do registro |
| usuario_id | INT | – | Sim | FK → usuario(id), ON DELETE CASCADE | Dona do registro |
| data_registro | DATE | – | Sim | CHECK (não pode ser futura) | Data da medição |
| peso_kg | NUMERIC | (5,2) | Não | CHECK (20 a 400) | Peso em quilos |
| altura_cm | NUMERIC | (5,1) | Não | CHECK (80 a 250) | Altura em centímetros |
| observacoes | VARCHAR | 300 | Não | – | Anotações livres |

Restrição de tabela: `UNIQUE (usuario_id, data_registro)`, ou seja, um registro por data por usuária.

## Tabela `tipo_medida`
Lista fixa dos tipos de medida corporal.

| Campo | Tipo | Tamanho | Obrigatório | Restrições | Descrição |
|---|---|---|---|---|---|
| id | SERIAL | – | Sim | PK | Identificador do tipo |
| nome | VARCHAR | 50 | Sim | UNIQUE | Cintura, Quadril, Coxas, Panturrilhas, Braços, Peitoral |

## Tabela `medida`
Valor de uma medida corporal dentro de um registro.

| Campo | Tipo | Tamanho | Obrigatório | Restrições | Descrição |
|---|---|---|---|---|---|
| id | SERIAL | – | Sim | PK | Identificador da medida |
| registro_id | INT | – | Sim | FK → registro(id), ON DELETE CASCADE | Registro a que pertence |
| tipo_medida_id | INT | – | Sim | FK → tipo_medida(id) | Tipo da medida |
| valor_cm | NUMERIC | (5,1) | Sim | CHECK (10 a 250) | Valor em centímetros |

Restrição de tabela: `UNIQUE (registro_id, tipo_medida_id)`, ou seja, cada tipo de medida aparece uma vez por registro.

## Relacionamentos
- `usuario` 1 → N `registro`
- `registro` 1 → N `medida`
- `tipo_medida` 1 → N `medida`

## Regras tratadas fora do banco (validação no back-end)
- Um registro precisa ter o peso ou ao menos uma medida preenchida.
- A senha tem no mínimo 6 caracteres antes de virar hash.

## Justificativa de normalização (3FN)
- **1FN:** todos os campos guardam um valor único. As medidas não são colunas repetidas (cintura, quadril...), e sim linhas na tabela `medida`.
- **2FN:** todas as tabelas têm chave primária simples (`id`), então não há dependência parcial.
- **3FN:** nenhum atributo depende de outro atributo não chave. O nome da medida fica só em `tipo_medida`, e não repetido em cada `medida`.
