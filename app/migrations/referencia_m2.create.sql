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
