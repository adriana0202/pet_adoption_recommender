select * from paws.shelter_in_out;

-- clean the main table 
DELETE FROM shelter_in_out
WHERE size IS NULL;

-- check size column counts
select s.size, count(*) from paws.shelter_in_out s
group by 1;

-- create a new dimension table for the size dimension
create table if not exists paws.pet_size (
size_id int auto_increment,
size char(5),
primary key (size_id));

--  check if the table was created

select * from paws.pet_size;

-- lets populate the table by inserting the unique values for that dimension
INSERT INTO paws.pet_size (size)
SELECT DISTINCT size FROM paws.shelter_in_out;

-- check it has correctly populated
select * from paws.pet_size;

-- now lets adjust the original table so we will use this table
alter table paws.shelter_in_out add column size_id int after size;

-- lets set up the foreign key reference
alter table paws.shelter_in_out ADD CONSTRAINT size_fk FOREIGN KEY (size_id) REFERENCES paws.pet_size (size_id);

-- check the extra column has appeared
select * from paws.shelter_in_out limit 10;

-- populate the column using the dimension table we created
update paws.shelter_in_out s, paws.pet_size ps
set s.size_id = ps.size_id
where s.size = ps.size;

-- check it is populated
select * from paws.shelter_in_out limit 10;

-- lets drop the original column now
alter table paws.shelter_in_out drop column size;

-- check everything is as expected
select * from paws.shelter_in_out limit 10;
select ps.size, count(*) from paws.shelter_in_out s
inner join paws.pet_size ps on s.size_id = ps.size_id
group by 1;


		-- Now we create the type table --

-- check type column counts
select s.type, count(*) from paws.shelter_in_out s
group by 1;

create table if not exists paws.pet_type (
type_id int auto_increment,
type char(5),
primary key (type_id));

--  check if the table was created

select * from paws.pet_type;

-- lets populate the table by inserting the unique values for that dimension
INSERT INTO paws.pet_type (type)
SELECT DISTINCT type FROM paws.shelter_in_out;

-- check it has correctly populated
select * from paws.pet_type;

-- now lets adjust the original table so we will use this table
alter table paws.shelter_in_out add column type_id int after type;

-- lets set up the foreign key reference
alter table paws.shelter_in_out ADD CONSTRAINT type_fk FOREIGN KEY (type_id) REFERENCES paws.pet_type (type_id);

-- check the extra column has appeared
select * from paws.shelter_in_out limit 10;

-- populate the column using the dimension table we created
update paws.shelter_in_out s, paws.pet_type t
set s.type_id = t.type_id
where s.type = t.type;

-- check it is populated
select * from paws.shelter_in_out limit 10;

-- lets drop the original column now
alter table paws.shelter_in_out drop column type;

-- check everything is as expected
select * from paws.shelter_in_out limit 10;
select t.type, count(*) from paws.shelter_in_out s
inner join paws.pet_type t on s.type_id = t.type_id
group by 1;

		-- Now we create the type table --

-- check type column counts
select s.type, count(*) from paws.shelter_in_out s
group by 1;

create table if not exists paws.pet_type (
type_id int auto_increment,
type char(5),
primary key (type_id));

-- lets populate the table by inserting the unique values for that dimension
INSERT INTO paws.pet_type (type)
SELECT DISTINCT type FROM paws.shelter_in_out;

-- now lets adjust the original table so we will use this table
alter table paws.shelter_in_out add column type_id int after type;

-- lets set up the foreign key reference
alter table paws.shelter_in_out ADD CONSTRAINT type_fk FOREIGN KEY (type_id) REFERENCES paws.pet_type (type_id);

-- populate the column using the dimension table we created
update paws.shelter_in_out s, paws.pet_type t
set s.type_id = t.type_id
where s.type = t.type;

-- lets drop the original column now
alter table paws.shelter_in_out drop column type;

-- check everything is as expected
select t.type, count(*) from paws.shelter_in_out s
inner join paws.pet_type t on s.type_id = t.type_id
group by 1;

select * from paws.shelter_in_out limit 10;

		-- Now we create the intake_type table --

-- check type column counts
select s.intake_type, count(*) from paws.shelter_in_out s
group by 1;

create table if not exists paws.pet_intake (
intake_id int auto_increment,
type char(15),
primary key (intake_id));

-- lets populate the table by inserting the unique values for that dimension
INSERT INTO paws.pet_intake (type)
SELECT DISTINCT intake_type FROM paws.shelter_in_out;

-- check it has correctly populated
select * from paws.pet_intake;

-- now lets adjust the original table so we will use this table
alter table paws.shelter_in_out add column intake_id int after intake_type;

-- lets set up the foreign key reference
alter table paws.shelter_in_out ADD CONSTRAINT intake_fk FOREIGN KEY (intake_id) REFERENCES paws.pet_intake (intake_id);

-- check the extra column has appeared
select * from paws.shelter_in_out limit 10;

-- populate the column using the dimension table we created
update paws.shelter_in_out s, paws.pet_intake i
set s.intake_id = i.intake_id
where s.intake_type = i.type;

-- check it is populated
select * from paws.shelter_in_out limit 10;

-- lets drop the original column now
alter table paws.shelter_in_out drop column intake_type;

-- check everything is as expected
select * from paws.shelter_in_out limit 10;
select i.type, count(*) from paws.shelter_in_out s
inner join paws.pet_intake i on s.intake_id = i.intake_id
group by 1;


		-- Now we create the pet_sex table --

-- check type column counts
select s.sex, count(*) from paws.shelter_in_out s
group by 1;

create table if not exists paws.pet_sex (
sex_id int auto_increment,
sex char(10),
primary key (sex_id));

-- lets populate the table by inserting the unique values for that dimension
INSERT INTO paws.pet_sex (sex)
SELECT DISTINCT sex FROM paws.shelter_in_out;

-- check it has correctly populated
select * from paws.pet_sex;

-- now lets adjust the original table so we will use this table
alter table paws.shelter_in_out add column sex_id int after sex;

-- lets set up the foreign key reference
alter table paws.shelter_in_out ADD CONSTRAINT sex_fk FOREIGN KEY (sex_id) REFERENCES paws.pet_sex (sex_id);

-- check the extra column has appeared
select * from paws.shelter_in_out limit 10;

-- populate the column using the dimension table we created
update paws.shelter_in_out s, paws.pet_sex se
set s.sex_id = se.sex_id
where s.sex = se.sex;

-- check it is populated
select * from paws.shelter_in_out limit 10;


-- lets drop the original column now
alter table paws.shelter_in_out drop column sex;

-- check everything is as expected
select * from paws.shelter_in_out limit 10;
select se.sex, count(*) from paws.shelter_in_out s
inner join paws.pet_sex se on s.sex_id = se.sex_id
group by 1;

/*****************************************

We can now use from the menu, "database" -> "reverse engineer" in order to generate the ERM.

*****************************************/

select * from paws.shelter_in_out into outfile 'test.csv';
