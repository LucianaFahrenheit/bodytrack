# BodyTrack: Casos de Teste

Preencha as colunas **Resultado obtido** e **Status** (Passou / Falhou) depois de executar cada teste. Registre as falhas, mesmo as pequenas.

| ID | Requisito | Descrição | Passos | Resultado esperado | Resultado obtido | Status |
|---|---|---|---|---|---|---|
| CT01 | RF01 | Cadastro válido | Criar conta com dados corretos | Conta criada e tela Início aberta | | |
| CT02 | RF01 | E-mail duplicado | Cadastrar um e-mail já existente | Mensagem "Este e-mail já está cadastrado." | | |
| CT03 | RNF04 | Senha curta | Cadastrar com senha de 3 caracteres | Mensagem de senha curta | | |
| CT04 | RNF04 | Senhas diferentes | Confirmação diferente da senha | Mensagem "As senhas não coincidem." | | |
| CT05 | RF02 | Login válido | Entrar com e-mail e senha corretos | Tela Início aberta | | |
| CT06 | RF02 | Login inválido | Entrar com senha errada | Mensagem "E-mail ou senha incorretos." | | |
| CT07 | RF02 | Logout | Clicar em Sair | Volta para a tela de login | | |
| CT08 | RF03 | Editar perfil | Alterar nome e salvar | Mensagem "Perfil atualizado." | | |
| CT09 | RF03 | E-mail em uso | Trocar para o e-mail de outra conta | Mensagem "Este e-mail já está em uso." | | |
| CT10 | RF04 | Registrar peso | Salvar registro só com peso | Registro aparece no histórico | | |
| CT11 | RF05 | Registrar medidas | Salvar as 6 medidas | Medidas aparecem no histórico | | |
| CT12 | RNF04 | Peso fora do limite | Peso 500 | Mensagem de valor entre 20 e 400 | | |
| CT13 | RNF04 | Data futura | Escolher data futura | Mensagem de data inválida | | |
| CT14 | RNF04 | Registro vazio | Salvar sem peso nem medidas | Mensagem pedindo peso ou medida | | |
| CT15 | RN03 | Data repetida | Salvar duas vezes na mesma data | Mensagem "Já existe um registro nesta data." | | |
| CT16 | RF06/RF07 | Consultar histórico | Abrir a aba Histórico | Registros listados por data | | |
| CT17 | RF06 | Filtro por período | Usar De e Até | Só os registros do período | | |
| CT18 | RF08 | Editar registro | Alterar o peso de um registro | Valor atualizado no histórico | | |
| CT19 | RF09 | Excluir registro | Excluir e confirmar | Registro some do histórico | | |
| CT20 | RF10 | Gráfico | Abrir Evolução com 2+ registros | Gráfico exibido | | |
| CT21 | RF10 | Comparar datas | Escolher duas datas | Tabela com as diferenças | | |
| CT22 | RNF03 | Isolamento | Entrar com outra conta | Não aparecem registros da primeira | | |
| CT23 | RNF01 | Responsividade | Abrir no celular | Menu embaixo e histórico em cartões | | |
| CT24 | RNF02 | Hash de senha | Consultar a tabela usuario | senha_hash embaralhada | | |
| CT25 | RNF03 | Acesso sem login | Abrir /api/registros sem logar | Resposta de erro 401 | | |

Testes automatizados: `pytest` (arquivo `tests/test_basico.py`). Anexe o print do resultado.
