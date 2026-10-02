-- =====================================================
-- BANCO: patrimonio_imob
-- Script único para execução direta no MySQL Workbench
-- (File > Open SQL Script > raio Execute)
-- Gerado a partir das migrations em app/migrations/
-- =====================================================

DROP DATABASE IF EXISTS patrimonio_imob;
CREATE DATABASE patrimonio_imob;
USE patrimonio_imob;

-- ===== estado.create.sql =====
create table estado
(
	id integer not null auto_increment,
	nome varchar(100) not null,
	sigla char(2) not null,
	primary key(id),
	constraint uk_estado_sigla unique(sigla)
);

-- ===== tipo_imovel.create.sql =====
create table tipo_imovel
(
	id integer not null auto_increment,
	nome varchar(100) not null,
	primary key(id),
	constraint uk_tipo_imovel_nome unique(nome)
);

-- ===== status_imovel.create.sql =====
create table status_imovel
(
	id integer not null auto_increment,
	nome varchar(50) not null,
	primary key(id),
	constraint uk_status_imovel_nome unique(nome)
);

-- ===== usuario.create.sql =====
create table usuario
(
	id integer not null auto_increment,
	nome varchar(150) not null,
	login varchar(50) not null,
	senha_hash varchar(255) not null,
	primary key(id),
	constraint uk_usuario_login unique(login)
);

-- ===== cidade.create.sql =====
create table cidade
(
	id integer not null auto_increment,
	nome varchar(150) not null,
	estado_id integer not null,
	primary key(id),
	constraint fk_estado_cidade
		foreign key(estado_id)
		references estado(id),
	constraint uk_cidade_estado unique(nome, estado_id)
);

-- ===== proprietario.create.sql =====
create table proprietario
(
	id integer not null auto_increment,
	nome varchar(150) not null,
	cpf varchar(14),
	email varchar(180),
	telefone varchar(30),
	primary key(id)
);

-- ===== proprietario.add.cidade_id.sql =====
alter table proprietario add column cidade_id integer;
alter table proprietario add constraint fk_cidade_proprietario
	foreign key(cidade_id) references cidade(id);

-- ===== imovel.create.sql =====
create table imovel
(
	id integer not null auto_increment,
	area_total decimal(10,2) not null,
	area_privativa decimal(10,2) not null,
	valor_compra decimal(12,2) not null,
	data_compra date not null,
	comodos integer not null,
	banheiros integer not null,
	vagas_garagem integer not null,
	observacoes text,
	primary key(id)
);

-- ===== imovel.add.cidade_id.sql =====
alter table imovel add column cidade_id integer not null;
alter table imovel add constraint fk_cidade_imovel
	foreign key(cidade_id) references cidade(id);

-- ===== imovel.add.tipo_imovel_id.sql =====
alter table imovel add column tipo_imovel_id integer not null;
alter table imovel add constraint fk_tipo_imovel_imovel
	foreign key(tipo_imovel_id) references tipo_imovel(id);

-- ===== imovel.add.status_id.sql =====
alter table imovel add column status_id integer not null;
alter table imovel add constraint fk_status_imovel_imovel
	foreign key(status_id) references status_imovel(id);

-- ===== imovel_proprietario.create.sql =====
create table imovel_proprietario
(
	imovel_id integer not null,
	proprietario_id integer not null,
	percentual_participacao decimal(5,2) not null default 100.00,
	primary key(imovel_id, proprietario_id),
	constraint fk_imovel_imovel_proprietario
		foreign key(imovel_id)
		references imovel(id),
	constraint fk_proprietario_imovel_proprietario
		foreign key(proprietario_id)
		references proprietario(id)
);

-- ===== referencia_m2.create.sql =====
create table referencia_m2
(
	id integer not null auto_increment,
	cidade_id integer not null,
	tipo_imovel_id integer not null,
	valor_m2 decimal(12,2) not null,
	primary key(id),
	constraint fk_cidade_referencia_m2
		foreign key(cidade_id) references cidade(id),
	constraint fk_tipo_imovel_referencia_m2
		foreign key(tipo_imovel_id) references tipo_imovel(id),
	constraint uk_referencia_m2 unique(cidade_id, tipo_imovel_id)
);

-- ===== referencia_iptu.create.sql =====
create table referencia_iptu
(
	id integer not null auto_increment,
	cidade_id integer not null,
	tipo_imovel_id integer not null,
	aliquota decimal(8,6) not null,
	primary key(id),
	constraint fk_cidade_referencia_iptu
		foreign key(cidade_id) references cidade(id),
	constraint fk_tipo_imovel_referencia_iptu
		foreign key(tipo_imovel_id) references tipo_imovel(id),
	constraint uk_referencia_iptu unique(cidade_id, tipo_imovel_id)
);

-- ===== avaliacao.create.sql =====
create table avaliacao
(
	id integer not null auto_increment,
	imovel_id integer not null,
	data_avaliacao date not null,
	valor_estimado decimal(12,2) not null,
	observacao text,
	primary key(id),
	constraint fk_imovel_avaliacao
		foreign key(imovel_id) references imovel(id)
);

-- ===== despesa.create.sql =====
create table despesa
(
	id integer not null auto_increment,
	imovel_id integer not null,
	descricao varchar(255) not null,
	valor decimal(12,2) not null,
	data_despesa date not null,
	primary key(id),
	constraint fk_imovel_despesa
		foreign key(imovel_id) references imovel(id)
);

-- ===== movimentacao.create.sql =====
create table movimentacao
(
	id integer not null auto_increment,
	imovel_id integer not null,
	tipo varchar(50) not null,
	valor decimal(12,2),
	data_movimentacao date not null,
	observacao text,
	primary key(id),
	constraint fk_imovel_movimentacao
		foreign key(imovel_id) references imovel(id)
);

