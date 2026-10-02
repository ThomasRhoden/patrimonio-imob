create table status_imovel
(
	id integer not null auto_increment,
	nome varchar(50) not null,
	primary key(id),
	constraint uk_status_imovel_nome unique(nome)
);
