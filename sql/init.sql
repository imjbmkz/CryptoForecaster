-- Table: public.coins_list
CREATE TABLE IF NOT EXISTS public.coins_list
(
    id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    symbol character varying(100) COLLATE pg_catalog."default" NOT NULL,
    insertion_date timestamp without time zone NOT NULL,
    CONSTRAINT coins_list_pkey PRIMARY KEY (id)
);

-- Table: public.market_chart
CREATE TABLE IF NOT EXISTS public.market_chart
(
    id SERIAL NOT NULL,
    coin_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    vs_currency character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    price numeric(18,4) NOT NULL,
    market_cap numeric(22,4) NOT NULL,
    total_volume numeric(22,4) NOT NULL,
    insertion_date timestamp without time zone NOT NULL,
    CONSTRAINT market_chart_pkey PRIMARY KEY (id)
);