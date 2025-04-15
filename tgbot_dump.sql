--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12
-- Dumped by pg_dump version 15.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO tgbot;

--
-- Name: channels; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.channels (
    channel_id bigint NOT NULL,
    channel_name character varying(100) NOT NULL,
    channel_link character varying(255),
    description text,
    creation_date timestamp without time zone,
    member_count integer,
    additional_info character varying(255),
    is_public boolean DEFAULT true,
    monthly_limit integer DEFAULT 1000,
    monthly_views_left integer DEFAULT 1000,
    admin_user_ids bigint[] DEFAULT '{}'::bigint[],
    posts_count integer DEFAULT 0,
    last_activity_date timestamp without time zone
);


ALTER TABLE public.channels OWNER TO tgbot;

--
-- Name: channels_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: tgbot
--

CREATE SEQUENCE public.channels_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.channels_channel_id_seq OWNER TO tgbot;

--
-- Name: channels_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tgbot
--

ALTER SEQUENCE public.channels_channel_id_seq OWNED BY public.channels.channel_id;


--
-- Name: interests; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.interests (
    interest_id integer NOT NULL,
    interest_name character varying(255) NOT NULL
);


ALTER TABLE public.interests OWNER TO tgbot;

--
-- Name: interests_interest_id_seq; Type: SEQUENCE; Schema: public; Owner: tgbot
--

CREATE SEQUENCE public.interests_interest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.interests_interest_id_seq OWNER TO tgbot;

--
-- Name: interests_interest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tgbot
--

ALTER SEQUENCE public.interests_interest_id_seq OWNED BY public.interests.interest_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    channel_id bigint,
    message_id integer,
    text text,
    date timestamp without time zone,
    channel_name text,
    interests text,
    views_count integer DEFAULT 0 NOT NULL,
    reactions_count integer DEFAULT 0 NOT NULL,
    clicks_count integer DEFAULT 0 NOT NULL,
    reactions_count_heart integer DEFAULT 0 NOT NULL,
    reactions_count_like integer DEFAULT 0 NOT NULL,
    reactions_count_dislike integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.posts OWNER TO tgbot;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: tgbot
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO tgbot;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tgbot
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: premium_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.premium_users (
    user_id bigint NOT NULL,
    premium_views integer DEFAULT 0,
    referral_bonus_views integer DEFAULT 0,
    activated_at timestamp without time zone DEFAULT now(),
    expires_at timestamp without time zone
);


ALTER TABLE public.premium_users OWNER TO postgres;

--
-- Name: user_activity; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.user_activity (
    activity_id integer NOT NULL,
    user_id integer,
    post_id integer,
    action_type character varying(50),
    action_timestamp timestamp without time zone NOT NULL
);


ALTER TABLE public.user_activity OWNER TO tgbot;

--
-- Name: user_activity_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: tgbot
--

CREATE SEQUENCE public.user_activity_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_activity_activity_id_seq OWNER TO tgbot;

--
-- Name: user_activity_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tgbot
--

ALTER SEQUENCE public.user_activity_activity_id_seq OWNED BY public.user_activity.activity_id;


--
-- Name: user_state; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.user_state (
    user_id bigint NOT NULL,
    last_read_post_id integer,
    unread_posts_count integer
);


ALTER TABLE public.user_state OWNER TO tgbot;

--
-- Name: users; Type: TABLE; Schema: public; Owner: tgbot
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    username character varying(50),
    first_name character varying(50),
    last_name character varying(50),
    language_code character varying(10),
    last_active timestamp without time zone,
    registration_date timestamp without time zone,
    interest_tags character varying(255),
    subscription_status character varying DEFAULT 'free'::character varying,
    user_state_id integer,
    interests text[],
    subscribed_channels bigint[] DEFAULT '{}'::bigint[],
    premium_views integer DEFAULT 0,
    free_views integer DEFAULT 1000,
    referral_bonus_views integer DEFAULT 0,
    referrer_id bigint,
    referrals_count integer DEFAULT 0,
    managed_channels bigint[] DEFAULT '{}'::bigint[]
);


ALTER TABLE public.users OWNER TO tgbot;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: tgbot
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO tgbot;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tgbot
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: channels channel_id; Type: DEFAULT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.channels ALTER COLUMN channel_id SET DEFAULT nextval('public.channels_channel_id_seq'::regclass);


--
-- Name: interests interest_id; Type: DEFAULT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.interests ALTER COLUMN interest_id SET DEFAULT nextval('public.interests_interest_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: user_activity activity_id; Type: DEFAULT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_activity ALTER COLUMN activity_id SET DEFAULT nextval('public.user_activity_activity_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: channels; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.channels (channel_id, channel_name, channel_link, description, creation_date, member_count, additional_info, is_public, monthly_limit, monthly_views_left, admin_user_ids, posts_count, last_activity_date) FROM stdin;
-1002691053050	тест канал 2	Ссылка отсутствует	\N	\N	\N	\N	t	1000	1000	{}	0	\N
-1002638223590	TG Лента премиум	Ссылка отсутствует	\N	\N	\N	\N	t	1000	1000	{}	0	\N
-1002527431044	Тест канал	https://t.me/dsfbjhvsdf	\N	\N	\N	\N	t	1000	895	{}	0	\N
\.


--
-- Data for Name: interests; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.interests (interest_id, interest_name) FROM stdin;
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.posts (id, channel_id, message_id, text, date, channel_name, interests, views_count, reactions_count, clicks_count, reactions_count_heart, reactions_count_like, reactions_count_dislike) FROM stdin;
84	-1002527431044	202	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
86	-1002527431044	204	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
88	-1002527431044	206	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
90	-1002527431044	208	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
91	-1002527431044	209	\N	2025-04-14 19:50:32	\N	\N	0	0	0	0	0	0
93	-1002527431044	211	\N	2025-04-14 19:50:32	\N	\N	0	0	0	0	0	0
95	-1002527431044	213	\N	2025-04-14 19:50:32	\N	\N	0	0	0	0	0	0
102	-1002527431044	219	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	0	0
104	-1002527431044	222	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
106	-1002527431044	224	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
108	-1002527431044	226	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
110	-1002527431044	228	\N	2025-04-14 19:50:35	\N	\N	0	0	0	0	0	0
112	-1002527431044	230	\N	2025-04-14 19:50:35	\N	\N	0	0	0	0	0	0
97	-1002527431044	215	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	1	0
99	-1002527431044	217	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	2	0
85	-1002527431044	203	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
87	-1002527431044	205	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
89	-1002527431044	207	\N	2025-04-14 19:50:31	\N	\N	0	0	0	0	0	0
92	-1002527431044	210	\N	2025-04-14 19:50:32	\N	\N	0	0	0	0	0	0
94	-1002527431044	212	\N	2025-04-14 19:50:32	\N	\N	0	0	0	0	0	0
96	-1002527431044	214	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	0	0
98	-1002527431044	216	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	0	0
100	-1002527431044	218	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	0	0
101	-1002527431044	220	\N	2025-04-14 19:50:33	\N	\N	0	0	0	0	0	0
105	-1002527431044	223	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
107	-1002527431044	225	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
109	-1002527431044	227	\N	2025-04-14 19:50:34	\N	\N	0	0	0	0	0	0
111	-1002527431044	229	\N	2025-04-14 19:50:35	\N	\N	0	0	0	0	0	0
116	-1002691053050	48	\N	2025-04-14 21:17:58	\N	\N	0	0	0	0	0	0
103	-1002527431044	221	\N	2025-04-14 19:50:33	\N	\N	0	0	0	1	0	0
114	-1002527431044	232	\N	2025-04-14 20:16:33	\N	\N	0	0	0	0	0	0
\.


--
-- Data for Name: premium_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.premium_users (user_id, premium_views, referral_bonus_views, activated_at, expires_at) FROM stdin;
960349952	0	0	2025-04-15 10:23:24.551465	\N
\.


--
-- Data for Name: user_activity; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.user_activity (activity_id, user_id, post_id, action_type, action_timestamp) FROM stdin;
\.


--
-- Data for Name: user_state; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.user_state (user_id, last_read_post_id, unread_posts_count) FROM stdin;
960349952	\N	0
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tgbot
--

COPY public.users (user_id, username, first_name, last_name, language_code, last_active, registration_date, interest_tags, subscription_status, user_state_id, interests, subscribed_channels, premium_views, free_views, referral_bonus_views, referrer_id, referrals_count, managed_channels) FROM stdin;
5580462911	\N	\N	\N	\N	2025-04-14 21:16:23.326167	2025-04-14 21:16:23.326167	\N	free	\N	\N	{-1002527431044}	0	1000	0	\N	0	{}
960349952	Ads_digitall	👁‍🗨Daniil		ru	2025-04-14 18:11:05.038347	2025-04-07 11:06:23.435199		free	\N	\N	{-1002527431044}	0	1000	0	\N	0	{-1002691053050,-1002527431044}
\.


--
-- Name: channels_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tgbot
--

SELECT pg_catalog.setval('public.channels_channel_id_seq', 1, false);


--
-- Name: interests_interest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tgbot
--

SELECT pg_catalog.setval('public.interests_interest_id_seq', 1, false);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tgbot
--

SELECT pg_catalog.setval('public.posts_id_seq', 119, true);


--
-- Name: user_activity_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tgbot
--

SELECT pg_catalog.setval('public.user_activity_activity_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tgbot
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: channels channels_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (channel_id);


--
-- Name: interests interests_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.interests
    ADD CONSTRAINT interests_pkey PRIMARY KEY (interest_id);


--
-- Name: posts posts_channel_id_message_id_key; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_channel_id_message_id_key UNIQUE (channel_id, message_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: premium_users premium_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premium_users
    ADD CONSTRAINT premium_users_pkey PRIMARY KEY (user_id);


--
-- Name: user_activity user_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_pkey PRIMARY KEY (activity_id);


--
-- Name: user_state user_state_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_state
    ADD CONSTRAINT user_state_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: ix_channels_channel_id; Type: INDEX; Schema: public; Owner: tgbot
--

CREATE UNIQUE INDEX ix_channels_channel_id ON public.channels USING btree (channel_id);


--
-- Name: ix_users_user_id; Type: INDEX; Schema: public; Owner: tgbot
--

CREATE UNIQUE INDEX ix_users_user_id ON public.users USING btree (user_id);


--
-- Name: premium_users premium_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premium_users
    ADD CONSTRAINT premium_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_activity user_activity_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: user_activity user_activity_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_state user_state_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.user_state
    ADD CONSTRAINT user_state_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: users users_referrer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referrer_id_fkey FOREIGN KEY (referrer_id) REFERENCES public.users(user_id);


--
-- Name: users users_user_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tgbot
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_state_id_fkey FOREIGN KEY (user_state_id) REFERENCES public.user_state(user_id);


--
-- Name: TABLE premium_users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.premium_users TO tgbot;


--
-- PostgreSQL database dump complete
--

