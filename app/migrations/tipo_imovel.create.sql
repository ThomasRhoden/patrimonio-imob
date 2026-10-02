create table tipo_imovel
(
	id integer not null auto_increment,
	nome varchar(100) not null,
	primary key(id),
	constraint uk_tipo_imovel_nome unique(nome)
);
