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
