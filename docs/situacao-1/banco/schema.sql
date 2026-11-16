-- BodyTrack - Projeto físico do banco de dados (PostgreSQL)

CREATE TABLE usuario (
  id              SERIAL PRIMARY KEY,
  nome            VARCHAR(100) NOT NULL,
  email           VARCHAR(150) NOT NULL UNIQUE,
  senha_hash      VARCHAR(255) NOT NULL,
  data_nascimento DATE,
  criado_em       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE registro (
  id            SERIAL PRIMARY KEY,
  usuario_id    INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
  data_registro DATE NOT NULL CHECK (data_registro <= CURRENT_DATE),
  peso_kg       NUMERIC(5,2) CHECK (peso_kg BETWEEN 20 AND 400),
  altura_cm     NUMERIC(5,1) CHECK (altura_cm BETWEEN 80 AND 250),
  observacoes   VARCHAR(300),
  UNIQUE (usuario_id, data_registro)
);

CREATE TABLE tipo_medida (
  id   SERIAL PRIMARY KEY,
  nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE medida (
  id             SERIAL PRIMARY KEY,
  registro_id    INT NOT NULL REFERENCES registro(id) ON DELETE CASCADE,
  tipo_medida_id INT NOT NULL REFERENCES tipo_medida(id),
  valor_cm       NUMERIC(5,1) NOT NULL CHECK (valor_cm BETWEEN 10 AND 250),
  UNIQUE (registro_id, tipo_medida_id)
);

INSERT INTO tipo_medida (nome) VALUES
  ('Cintura'), ('Quadril'), ('Coxas'), ('Panturrilhas'), ('Braços'), ('Peitoral');
