-- Схема 'content'
CREATE SCHEMA content;

-- Таблица 'Кинопроизведения'
CREATE TABLE IF NOT EXISTS content.film_work (
	id uuid PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT,
	creation_date DATE,
	rating FLOAT,
	type TEXT not null,
	created timestamp with time zone,
	modified timestamp with time zone);

-- Таблица 'Жанры'
CREATE TABLE IF NOT EXISTS content.genre (
	id uuid PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	created timestamp with time zone,
	modified timestamp with time zone);

-- 'Персонажи'
CREATE TABLE IF NOT EXISTS content.person (
	id uuid PRIMARY KEY,
	full_name TEXT NOT NULL,
	created timestamp with time zone,
	modified timestamp with time zone);

-- 'Персонажи фильма'
CREATE TABLE IF NOT EXISTS content.person_film_work (
	id uuid PRIMARY KEY,
	person_id uuid REFERENCES content.person (id),
	film_work_id uuid REFERENCES content.film_work (id),
	role TEXT NOT NULL,
	created timestamp with time zone);

-- 'Жанры фильма'
CREATE TABLE IF NOT EXISTS content.genre_film_work (
	id uuid PRIMARY KEY,
	genre_id uuid REFERENCES content.genre (id),
	film_work_id uuid REFERENCES content.film_work (id),
	created timestamp with time zone);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);
