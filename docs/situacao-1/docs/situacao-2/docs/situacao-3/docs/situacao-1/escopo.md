# BodyTrack: Documento de Escopo

**Autor(a):** Zaira Luciana Moura Lobato
**Data:** 01/11/2026

## 1. O que é
O BodyTrack é um aplicativo web para usuarios registrarem seu peso, altura e medidas corporais e acompanhar sua evolução por meio de histórico e gráficos.

## 2. Objetivo
Permitir que os usuarios registrem, consultem e visualizem a evolução do seu corpo de forma simples.

## 3. Módulos
1. **Usuários:** cadastro, login, logout e edição de perfil.
2. **Peso:** registro de peso, data e observações opcionais.
3. **Medidas:** cintura, quadril, coxas, panturrilhas, braços e peitoral.
4. **Histórico e evolução:** consulta por data, gráficos e comparação de datas.

## 4. Requisitos funcionais
| Código | Requisito |
|---|---|
| RF01 | Permitir cadastro de usuários |
| RF02 | Permitir autenticação e logout |
| RF03 | Permitir edição do perfil |
| RF04 | Registrar peso e data |
| RF05 | Registrar medidas corporais |
| RF06 | Consultar histórico de peso |
| RF07 | Consultar histórico de medidas |
| RF08 | Editar registros existentes |
| RF09 | Excluir registros |
| RF10 | Exibir gráficos de evolução |

## 5. Requisitos não funcionais
| Código | Requisito |
|---|---|
| RNF01 | Interface responsiva |
| RNF02 | Senhas armazenadas com hash seguro |
| RNF03 | Acesso restrito aos dados do próprio usuário |
| RNF04 | Validação dos campos |
| RNF05 | Banco de dados relacional |
| RNF06 | Mensagens claras de erro e sucesso |

## 6. Regras de negócio
- O e-mail de cada usuária deve ser único.
- Cada usuária pode ter apenas um registro por data.
- A data do registro não pode ser futura.
- Peso entre 20 e 400 kg, altura entre 80 e 250 cm e medidas entre 10 e 250 cm.
- Cada usuária só vê, edita e exclui os próprios registros.

## 7. Fora do escopo
- Fotos de progresso.
- Inteligência artificial.
- Integração com relógios.
- Recomendações nutricionais.

## 8. Tecnologias
- **Front-end:** HTML, CSS e JavaScript.
- **Back-end:** Python com Flask (padrão MVC).
- **Banco de dados:** PostgreSQL.
- **Testes:** pytest.
- **Versionamento:** Git e GitHub.