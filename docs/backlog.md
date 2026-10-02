# 🗒️ Backlog — Patrimônio Imob

Épicos e histórias de usuário do sistema, conferidos no código atual. Os ids RF/RN são os do `requisitos.md`. O usuário é sempre a pessoa dona do patrimônio (não há tipos de usuário).

---

## Épico 1 — Acesso e Segurança

**Descrição:** Como dono do patrimônio, eu quero entrar no sistema com login e senha para que só eu (ou quem eu autorizar) veja meus imóveis e os dados dos proprietários.

**Critérios de aceitação:**
- O sistema abre na tela de login e só mostra o menu depois de um login válido.
- A senha nunca é gravada em texto puro, só o hash com salt.
- As credenciais do banco ficam no arquivo `.env`, fora do código.

### US01 — Fazer login (RNF segurança)
Como usuário, eu quero informar login e senha para que eu acesse o sistema com segurança.
- Login e senha corretos abrem o menu e o dashboard.
- Campo vazio mostra "Informe login e senha.".
- Login inexistente ou senha errada mostra a mesma mensagem: "Login ou senha inválidos.".

### US02 — Criar o primeiro acesso (implantação)
Como quem instala o sistema, eu quero criar o primeiro acesso pelo terminal para que eu consiga fazer o primeiro login.
- `python seed_inicial.py` pede o login (Enter aceita `admin`) e a senha duas vezes, sem mostrar na tela.
- Login com espaço ou senhas diferentes são recusados e o script pede de novo.
- Se o login já existe, o script avisa e não altera nada.

### US03 — Manter acessos (extra)
Como usuário, eu quero cadastrar outro acesso ou trocar minha senha para que eu controle quem entra no sistema.
- A tela *Usuários* tem só login, nome e senha, e aparece para todo usuário logado.
- O login é obrigatório, único, sem espaços e com até 50 caracteres.
- Alterar com a senha em branco mantém a senha atual.
- Não é possível excluir o próprio acesso.

---

## Épico 2 — Cadastros de Base

**Descrição:** Como dono do patrimônio, eu quero cadastrar estados, cidades, tipos e status de imóvel para que os imóveis usem sempre valores padronizados.

**Critérios de aceitação:**
- Cada cadastro tem Novo, Salvar, Alterar, Excluir e Fechar, com lista (tabela) na mesma tela.
- Registro repetido mostra "Já existe um registro com esses dados.".
- Excluir um registro em uso mostra "Não é possível excluir: existem registros vinculados.".

### US04 — Manter estados (RN04)
Como usuário, eu quero cadastrar estados com nome e sigla para que as cidades fiquem ligadas a um estado.
- Nome é obrigatório e a sigla tem exatamente 2 letras.
- A sigla não pode se repetir.

### US05 — Manter cidades (RN04)
Como usuário, eu quero cadastrar cidades ligadas a um estado para que cada imóvel tenha uma localização válida.
- Nome e estado são obrigatórios.
- A mesma cidade não pode se repetir no mesmo estado.

### US06 — Manter tipos e status de imóvel (RN04, RN05)
Como usuário, eu quero cadastrar tipos (ex.: Apartamento) e status (Próprio, Alugado, À venda) para que eu possa ajustar essas listas sem mexer no código.
- O nome é obrigatório e único.
- Os tipos e status cadastrados aparecem nas comboboxes da tela de imóveis.

---

## Épico 3 — Proprietários e Imóveis

**Descrição:** Como dono do patrimônio, eu quero cadastrar meus imóveis e quem é dono de cada um para que eu tenha a lista completa do patrimônio, inclusive os imóveis divididos.

**Critérios de aceitação:**
- Dados inválidos não são gravados e aparecem como "Erro: " + mensagem.
- Um imóvel pode ter vários proprietários (N:N) e a soma dos percentuais não passa de 100%.

### US07 — Manter proprietários (RF07)
Como usuário, eu quero cadastrar os proprietários para que eu possa ligá-los aos imóveis.
- Só o nome é obrigatório; CPF, e-mail, telefone e cidade são opcionais (LGPD: minimização).
- A cidade é escolhida depois do estado (cascata).

### US08 — Manter imóveis (RF01, RF02, RF06, RN06, RN07, RN08)
Como usuário, eu quero cadastrar e listar meus imóveis para que eu saiba o que tenho, onde fica e quanto paguei.
- Cidade, tipo, status e data de compra são obrigatórios; ao escolher o estado, só aparecem as cidades dele.
- Área total maior que zero; área privativa não maior que a total; valor de compra não negativo.
- Datas no formato DD/MM/AAAA; texto em campo numérico mostra mensagem amigável.
- A lista mostra os imóveis cadastrados com os dados resumidos.

### US09 — Definir os proprietários do imóvel (RF07, RN04, RN09)
Como usuário, eu quero informar os donos de um imóvel e o percentual de cada um para que a co-propriedade fique registrada.
- O percentual de cada dono fica entre 0 e 100.
- Se a soma passar de 100%, a tela mostra "A soma dos percentuais não pode passar de 100%." e não grava.
- No banco, cada vínculo é gravado pela procedure `SP_ADICIONAR_PROPRIETARIO`, que também barra a soma acima de 100%.

---

## Épico 4 — Histórico do Imóvel

**Descrição:** Como dono do patrimônio, eu quero registrar avaliações, despesas e movimentações de cada imóvel para que eu acompanhe quanto ele vale, quanto gasta e quanto rende.

**Critérios de aceitação:**
- Os registros são abertos a partir de um imóvel selecionado na tela *Imóveis*.
- Data é obrigatória (DD/MM/AAAA) e valores não aceitam texto.

### US10 — Registrar avaliações (RF08, RN03)
Como usuário, eu quero registrar o valor estimado do imóvel em uma data para que eu veja a evolução do valor.
- Valor estimado não pode ser negativo.
- A lista mostra a data, o valor e a valorização (valor − compra).
- A última avaliação passa a ser o valor estimado do imóvel no dashboard.

### US11 — Registrar despesas (RF09)
Como usuário, eu quero lançar despesas do imóvel (condomínio, manutenção, taxas) para que eu saiba quanto gasto com ele.
- Descrição e data são obrigatórias; o valor não pode ser negativo.

### US12 — Registrar movimentações (RF10)
Como usuário, eu quero lançar movimentações financeiras (ex.: aluguel recebido) para que eu acompanhe o que o imóvel rende.
- Tipo (`entrada_aluguel`, `saida_manutencao` ou `outro`) e data são obrigatórios.
- Não guarda dados do inquilino, só tipo, valor, data e observação.

---

## Épico 5 — Dashboard e IPTU

**Descrição:** Como dono do patrimônio, eu quero ver um resumo com valor estimado, valorização e IPTU para que eu entenda a situação do patrimônio sem fazer contas em planilha.

**Critérios de aceitação:**
- O dashboard abre logo depois do login e é recalculado ao clicar em **Atualizar**.
- Os valores aparecem em reais (R$ 1.234,56).

### US13 — Manter referências de m² e IPTU (RF03, RF04, RN01, RN02)
Como usuário, eu quero cadastrar o valor do m² e a alíquota de IPTU por cidade e tipo para que o sistema calcule as estimativas.
- Uma referência por cidade + tipo; valor do m² e alíquota não negativos.
- A alíquota é digitada como fração (0.01 = 1%).

### US14 — Ver o dashboard (RF05, RN01, RN02, RN03)
Como usuário, eu quero ver os totais do patrimônio para que eu saiba quanto ele vale e quanto valorizou.
- Mostra quantidade de imóveis, valor de compra total, valor estimado total, valorização total e IPTU estimado anual.
- Valor estimado = última avaliação; sem avaliação, área privativa × m² da referência; sem referência, o valor de compra.
- IPTU estimado = valor estimado × alíquota da referência (sem referência, R$ 0,00).

### US15 — Ver resumos por cidade, estado, imóvel e proprietário (RF05, RF07)
Como usuário, eu quero ver o patrimônio separado por cidade, por estado, por imóvel e por proprietário para que eu compare onde está meu dinheiro e quanto é de cada dono.
- A aba *Resumo por cidade* vem da view `VW_PATRIMONIO_POR_CIDADE`.
- A aba *Por imóvel* mostra valor estimado, valorização e IPTU de cada imóvel.
- A aba *Por proprietário* vem da view `VW_RESUMO_POR_PROPRIETARIO`: cada valor × percentual do dono; a parte sem dono (imóvel com menos de 100%) não entra.

---

## Épico 6 — Idioma

**Descrição:** Como usuário, eu quero usar o sistema em português ou inglês para que outras pessoas também consigam usar e avaliar o sistema.

**Critérios de aceitação:**
- Todos os textos de interface (menus, telas, botões, mensagens) existem em PT e EN.
- Os dados cadastrados não são traduzidos.

### US16 — Trocar o idioma (extra)
Como usuário, eu quero trocar o idioma pelo menu para que a interface mude na hora.
- *Idioma → English* / *Português* refaz o menu, o dashboard e as janelas abertas no idioma escolhido.
- A tela de login também tem o menu *Idioma*.
