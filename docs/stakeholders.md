# 👤 Stakeholders — Patrimônio Imob

Documento da UC1 (Requisitos) — SENAC, Técnico em Desenvolvimento de Sistemas, módulo 1.
Base: `docs/requisitos.md` (seção 3), o código do projeto e o script `app/migrations/patrimonio_imob_full.sql`.

## 1. Tabela de stakeholders

| Stakeholder | Papel no projeto | Principal interesse | Influência |
|-------------|------------------|---------------------|------------|
| **Proprietário do patrimônio** (usuário principal) | Usa o sistema para cadastrar e acompanhar os próprios imóveis | Saber quanto vale o patrimônio, quanto valorizou e quanto gasta/recebe com cada imóvel | **Alta**: é para ele que o sistema existe |
| **Quem instala o sistema** (pode ser o próprio proprietário) | Prepara o sistema: roda os scripts do banco e cria o primeiro acesso (`seed_inicial.py`) | Deixar o sistema pronto para o primeiro login | **Média**: só atua na instalação (ver nota 1) |
| **Coproprietários** (titulares de dados) | Não usam o sistema, mas seus dados ficam guardados na tabela `proprietario` | Ter os dados pessoais (CPF, e-mail, telefone) tratados com segurança e só para essa finalidade | **Baixa** no projeto, **alta** do ponto de vista legal (LGPD) |
| **Desenvolvedor / equipe acadêmica** (Thomas) | Levanta requisitos, modela o banco, programa (MVC + DAO) e documenta | Entregar um sistema que funcione e cumpra os critérios do curso | **Alta**: decide escopo e implementação |
| **Professor avaliador** (SENAC) | Avalia documentação, código e apresentação | Ver requisitos, regras de negócio, casos de uso, LGPD e boas práticas aplicados corretamente | **Alta**: define critérios e nota |

> **Nota 1 — sem tipos de usuário:** o sistema é pessoal e offline. O login existe só para proteger os dados com senha, então **não há perfis** (nem admin × proprietário): cada registro da tabela `usuario` é apenas uma conta de acesso (`login` + senha). Todo usuário logado vê as mesmas telas, inclusive *Usuários*, onde troca a senha ou cria outro acesso. Os proprietários dos imóveis são **dados** (tabela `proprietario`), não usuários do sistema.

## 2. Personas do usuário principal

> **Persona fictícia**, criada para orientar os requisitos (não representa uma pessoa real).

| Campo | Descrição |
|-------|-----------|
| Nome | Marina, 42 anos |
| Onde mora | Porto Alegre (RS) |
| Situação | Tem um apartamento onde mora, um apartamento alugado e divide com o irmão (50% / 50%) uma casa de praia em Santa Catarina |
| Hoje faz | Controla tudo em planilhas soltas e não sabe dizer quanto o patrimônio vale hoje |
| Objetivos | Ver em uma tela o total investido, o valor estimado e a valorização; registrar avaliações, despesas (condomínio, manutenção) e aluguel recebido |
| Dores | Esquece quanto pagou em cada imóvel e quando; não sabe a parte de cada dono no imóvel dividido |
| Como o sistema ajuda | Dashboard (RF05), cadastro de imóveis (RF01), co-propriedade com percentual (RF07/RN09), avaliações (RF08), despesas (RF09) e movimentações (RF10) |

**Persona 2 (fictícia):**

| Campo | Descrição |
|-------|-----------|
| Nome | Roberto, 63 anos, aposentado |
| Onde mora | Caxias do Sul (RS) |
| Situação | Tem uma casa e uma sala comercial alugada; herdou com duas irmãs um terreno em Pelotas |
| Objetivos | Ter uma ideia do IPTU anual, registrar o aluguel da sala e os gastos de manutenção, deixar claro o percentual de cada herdeiro |
| Dores | Usa pouco o computador e não quer cadastro online |
| Como o sistema ajuda | IPTU estimado (RF04/RN02), movimentações (RF10), despesas (RF09), co-propriedade (RF07/RN09), login com senha no próprio computador |

## 3. LGPD — dados pessoais tratados

### 3.1 Quais dados pessoais existem no banco

| Tabela | Dados pessoais | Obrigatório? | Observação |
|--------|----------------|--------------|------------|
| `proprietario` | nome, CPF, e-mail, telefone, cidade | Só o **nome** é `not null`. CPF, e-mail, telefone e cidade podem ficar vazios | Na tela, campo vazio é gravado como `NULL` |
| `usuario` | nome, login, senha | Todos obrigatórios | Não guarda e-mail nem CPF: o login é um apelido livre (ex.: `admin`). A senha **não** é guardada em texto puro, só o hash (`senha_hash`) |

Nenhum dado **sensível** no sentido do art. 5º, II da LGPD (saúde, religião, origem racial etc.) é coletado. O CPF é um dado pessoal comum, mas identifica a pessoa diretamente e por isso merece cuidado.

### 3.2 Finalidade e base legal (proposta)

- **Finalidade:** identificar quem é dono de cada imóvel e qual o percentual de cada um (RF07 / RN09), e permitir o login de quem usa o sistema.
- **Base legal sugerida:**
  - Se o sistema é usado pela própria pessoa, só para organizar o **patrimônio pessoal**, sem fins econômicos, o art. 4º, I da LGPD diz que a lei não se aplica a esse uso.
  - Se for usado por terceiros (ex.: alguém que administra imóveis de outras pessoas), as bases mais adequadas seriam:
    - **execução de contrato** (art. 7º, V), pela compra ou co-propriedade do imóvel;
    - ou **legítimo interesse** (art. 7º, IX), pela gestão do patrimônio, sempre informando o titular.
  - A base legal é uma **decisão do responsável pelo sistema**. O código não registra consentimento nem base legal.

### 3.3 Minimização (art. 6º, III)

O que o projeto **já faz**:
- Só guarda o necessário: para o proprietário, o único campo obrigatório é o **nome**. CPF, e-mail, telefone e cidade são opcionais no banco e na tela.
- Não guarda dados do inquilino. A movimentação "entrada_aluguel" registra só tipo, valor, data e observação.
- A tabela `usuario` não tem ligação com `proprietario` e pede só login, nome e senha (sem e-mail), então quem faz login não precisa informar nenhum dado de contato.

Recomendações (ainda **não implementadas**):
- Só preencher o CPF quando for realmente necessário.
- Evitar colocar dados pessoais no campo livre "observações".
- Usar dados **fictícios** na apresentação e nos testes.

### 3.4 Segurança (art. 46)

O que **já existe** no código:
- **Senha com hash e salt:** `app/core/senha_utils.py` gera um salt aleatório (`secrets.token_hex(16)`) e guarda `salt$sha256(salt + senha)`. O login (`Login_Controller`) compara hashes, nunca a senha em texto.
- **Credenciais do banco fora do código:** ficam no arquivo `.env` (lido por `python-dotenv`), que está no `.gitignore` e não vai para o repositório.
- **Campo de senha mascarado** na tela de login (`show="*"`).

Limitações (honestas):
- **Sem perfis:** qualquer usuário logado vê todos os proprietários e CPFs e pode criar outros acessos (ver nota 1). Faz sentido num sistema pessoal; num uso por terceiros seria preciso controle por perfil.
- **CPF guardado e exibido em texto puro:** aparece na listagem de proprietários. Não há validação de formato.
- **Primeiro acesso:** `seed_inicial.py` pede o login (sugere `admin`) e a senha com `getpass` (com confirmação) e grava só o hash; não existe senha padrão.
- **Algoritmo de hash:** SHA-256 com salt é melhor que texto puro, mas para senhas o recomendado são algoritmos lentos (bcrypt, PBKDF2 ou Argon2). Fica como melhoria futura.
- **Sem política de senha** (tamanho mínimo) e sem bloqueio após várias tentativas erradas.

### 3.5 Direitos do titular (art. 18)

- **Correção:** possível pela tela *Proprietários* → **Alterar**.
- **Exclusão:** possível pela tela *Proprietários* → **Excluir**. Se o proprietário estiver ligado a um imóvel, o banco bloqueia a exclusão (FK sem cascade). Antes é preciso tirá-lo do imóvel no popup *Proprietários* da tela de imóveis.
- **Acesso / portabilidade:** não há exportação de dados. Hoje só dá para consultar pela tela.
