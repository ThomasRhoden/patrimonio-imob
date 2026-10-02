alter table imovel add column tipo_imovel_id integer not null;
alter table imovel add constraint fk_tipo_imovel_imovel
	foreign key(tipo_imovel_id) references tipo_imovel(id);
