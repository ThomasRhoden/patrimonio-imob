# 📋 Documento de requisitos do sistema Patrimônio Imob

## 1. Introdução

O sistema Patrimônio Imob tem como objetivo auxiliar o proprietário a registrar e analisar imóveis pessoais, com foco em valor estimado de mercado, IPTU e valorização. O projeto foi pensado como ferramenta de gestão imobiliária pessoal, sem depender de intermediários.

## 2. Objetivo do sistema

- cadastrar imóveis
- registrar dados básicos e financeiros
- calcular estimativas de venda
- estimar IPTU anual
- visualizar resumo consolidado do patrimônio
- apoiar decisões de gestão e análise de investimento

## 3. Stakeholders

- proprietário do patrimônio
- desenvolvedor / equipe acadêmica
- professor avaliador

## 4. Requisitos funcionais

### RF01 - Cadastro de imóveis
O sistema deve permitir cadastrar imóveis com dados como cidade, tipo, área total, área privativa, valor de compra, data de compra, cômodos, banheiros, vagas, status e observações.

### RF02 - Validação de dados
O sistema deve impedir cadastro com área total inválida, área privativa maior que total, valor de compra negativo ou outros dados inconsistentes.

### RF03 - Cálculo de valor estimado
O sistema deve calcular o valor estimado de venda com base na área e tabela de referência por cidade e tipo.

### RF04 - Cálculo de IPTU
O sistema deve estimar o IPTU anual com base na tabela de referência por cidade e tipo.

### RF05 - Dashboard
O sistema deve exibir indicadores consolidados, como quantidade de imóveis, valor estimado e valorização total.

### RF06 - Listagem
O sistema deve listar os imóveis cadastrados com dados resumidos.

### RF07 - Cadastro de proprietários e co-propriedade
O sistema deve permitir cadastrar proprietários e associá-los a um ou mais imóveis. Um imóvel pode ter mais de um proprietário, cada um com um percentual de participação.

### RF08 - Registro de avaliações
O sistema deve permitir registrar avaliações periódicas de valor estimado por imóvel, para acompanhar a evolução do valor ao longo do tempo.

### RF09 - Registro de despesas
O sistema deve permitir registrar despesas associadas a cada imóvel (manutenção, taxas, etc.).

### RF10 - Registro de movimentações financeiras
O sistema deve permitir registrar movimentações financeiras associadas a cada imóvel (ex.: recebimento de aluguel).

## 5. Requisitos não funcionais

- interface em Python com Tkinter
- estrutura orientada a objetos
- organização em camadas MVC + DAO
- compatibilidade com banco MySQL
- uso de variáveis de ambiente para credenciais
- código comentado para facilitar revisão acadêmica

## 6. Regras de negócio

- RN01: valor estimado = área privativa × valor médio do m² por cidade/tipo
- RN02: IPTU estimado = valor estimado × alíquota por cidade/tipo
- RN03: valorização = valor estimado − valor de compra
- RN04: imóvel pertence a uma cidade e um tipo específico; a posse é modelada como relação N:N com proprietário (permite co-propriedade)
- RN05: status permitido: Próprio, Alugado, À venda (cadastro configurável, não fixo em código)
- RN06: área total deve ser maior que zero
- RN07: área privativa não pode ultrapassar a área total
- RN08: valor de compra não pode ser negativo
- RN09: a soma dos percentuais de participação dos proprietários de um imóvel não pode superar 100%
