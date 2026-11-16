# BodyTrack: Casos de Teste

| ID | Requisito | Descrição | Passos | Resultado esperado | Resultado obtido | Status |
|---|---|---|---|---|---|---|
| CT01 | RF01 | Cadastro válido | Criar conta com dados corretos | Conta criada e tela Início aberta | Conta criada e a tela Início abriu | Passou |
| CT02 | RF01 | E-mail duplicado | Cadastrar um e-mail já existente | Mensagem "Este e-mail já está cadastrado." | Exibiu "Este e-mail já está cadastrado." | Passou |
| CT03 | RNF04 | Senha curta | Cadastrar com senha de 3 caracteres | Mensagem de senha curta | Exibiu a mensagem de senha com no mínimo 6 caracteres | Passou |
| CT04 | RNF04 | Senhas diferentes | Confirmação diferente da senha | Mensagem "As senhas não coincidem." | Exibiu "As senhas não coincidem." | Passou |
| CT05 | RF02 | Login válido | Entrar com e-mail e senha corretos | Tela Início aberta | Entrou e a tela Início abriu | Passou |
| CT06 | RF02 | Login inválido | Entrar com senha errada | Mensagem "E-mail ou senha incorretos." | Exibiu "E-mail ou senha incorretos." | Passou |
| CT07 | RF02 | Logout | Clicar em Sair | Volta para a tela de login | Voltou para a tela de login | Passou |
| CT08 | RF03 | Editar perfil | Alterar nome e salvar | Mensagem "Perfil atualizado." | Exibiu "Perfil atualizado." e o novo nome foi mantido | Passou |
| CT09 | RF03 | E-mail em uso | Trocar para o e-mail de outra conta | Mensagem "Este e-mail já está em uso." | Exibiu "Este e-mail já está em uso." | Passou |
| CT10 | RF04 | Registrar peso | Salvar registro só com peso | Registro aparece no histórico | O registro apareceu no histórico | Passou |
| CT11 | RF05 | Registrar medidas | Salvar as 6 medidas | Medidas aparecem no histórico | As 6 medidas apareceram no histórico | Passou |
| CT12 | RNF04 | Peso fora do limite | Peso 500 | Mensagem de valor entre 20 e 400 | Exibiu a mensagem de valor entre 20 e 400 | Passou |
| CT13 | RNF04 | Data futura | Escolher data futura | Mensagem de data inválida | Exibiu a mensagem de data não futura | Passou |
| CT14 | RNF04 | Registro vazio | Salvar sem peso nem medidas | Mensagem pedindo peso ou medida | Exibiu "Preencha o peso ou ao menos uma medida." | Passou |
| CT15 | RN03 | Data repetida | Salvar duas vezes na mesma data | Mensagem "Já existe um registro nesta data." | Exibiu "Já existe um registro nesta data." | Passou |
| CT16 | RF06/RF07 | Consultar histórico | Abrir a aba Histórico | Registros listados por data | Os registros apareceram listados por data | Passou |
| CT17 | RF06 | Filtro por período | Usar De e Até | Só os registros do período | Apareceram apenas os registros do período | Passou |
| CT18 | RF08 | Editar registro | Alterar o peso de um registro | Valor atualizado no histórico | O novo valor apareceu no histórico | Passou |
| CT19 | RF09 | Excluir registro | Excluir e confirmar | Registro some do histórico | O registro sumiu após a confirmação | Passou |
| CT20 | RF10 | Gráfico | Abrir Evolução com 2+ registros | Gráfico exibido | O gráfico foi exibido | Passou |
| CT21 | RF10 | Comparar datas | Escolher duas datas | Tabela com as diferenças | A tabela de diferenças foi exibida | Passou |
| CT22 | RNF03 | Isolamento | Entrar com outra conta | Não aparecem registros da primeira | A segunda conta não viu os registros da primeira | Passou |
| CT23 | RNF01 | Responsividade | Abrir no celular | Menu embaixo e histórico em cartões | O menu ficou embaixo e o histórico em cartões | Passou |
| CT24 | RNF02 | Hash de senha | Consultar a tabela usuario | senha_hash embaralhada | A senha apareceu embaralhada (hash) no banco | Passou |
| CT25 | RNF03 | Acesso sem login | Abrir /api/registros sem logar | Resposta de erro 401 | Retornou "Faça login para continuar." (erro 401) | Passou |

## Testes automatizados
Comando: `pytest`. Resultado: 15 testes executados, 15 aprovados (arquivo `tests/test_basico.py`). Print em `pytest.png`.

## Resumo
25 casos executados: 25 aprovados, 0 reprovados.