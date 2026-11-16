# BodyTrack

Aplicativo web para acompanhar peso, altura e medidas corporais (cintura, quadril, coxas, panturrilhas, braços e peitoral), com histórico por data e gráficos de evolução.

Projeto Integrador Transdisciplinar II.

## Tecnologias
- Front-end: HTML, CSS e JavaScript
- Back-end: Python 3 + Flask (padrão MVC)
- Banco de dados: PostgreSQL
- Testes: pytest

## Como instalar e rodar
1. Clone o repositório e entre na pasta:
   ```
   git clone https://github.com/lucianamoura9/bodytrack
   cd bodytrack
   ```
2. Crie e ative o ambiente virtual (Windows PowerShell):
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. No PostgreSQL (pgAdmin), crie o banco `bodytrack` e rode o arquivo `docs/situacao-1/banco/schema.sql`.
4. Crie um arquivo `.env` na raiz com:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=bodytrack
   DB_USER=postgres
   DB_PASSWORD=SUA_SENHA
   SECRET_KEY=uma-chave-longa-e-aleatoria
   ```
5. Rode o app e abra http://127.0.0.1:5000:
   ```
   python app.py
   ```

## Testes
```
pytest
```

## Estrutura
```
app/models/        acesso ao banco (Model)
app/controllers/   rotas e validações (Controller)
app/templates/     página HTML (View)
app/static/        CSS e JavaScript
database/ e docs/  banco, UML, IHC, manual e testes
tests/             testes automatizados
```

## Documentação
- `docs/situacao-1/`: escopo, UML, IHC e banco de dados
- `docs/situacao-2/`: manual de uso
- `docs/situacao-3/`: casos de teste e avaliação dos testadores
