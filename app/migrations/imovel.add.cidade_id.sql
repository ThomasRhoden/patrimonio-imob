alter table imovel add column cidade_id integer not null;
alter table imovel add constraint fk_cidade_imovel
	foreign key(cidade_id) references cidade(id);
