alter table proprietario add column cidade_id integer;
alter table proprietario add constraint fk_cidade_proprietario
	foreign key(cidade_id) references cidade(id);
