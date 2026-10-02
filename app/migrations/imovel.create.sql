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
