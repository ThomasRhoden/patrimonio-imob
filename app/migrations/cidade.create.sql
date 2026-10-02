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
