-- =====================================
-- Question 1 : les trois sinistres les plus chers de chaque region
-- =====================================


 
WITH classement AS (
    SELECT 
        fsm.region_sinistre, 
        fsm.sinistre_id, 
        fsm.type_sinistre, 
        fsm.montant_estime,
        ROW_NUMBER() OVER (
            PARTITION BY fsm.region_sinistre 
            ORDER BY fsm.montant_estime DESC
        ) AS rang
    FROM fact_sinistre_meteo fsm
)
SELECT 
    region_sinistre, 
    sinistre_id, 
    type_sinistre, 
    montant_estime,
    rang
FROM classement
WHERE rang <= 3
ORDER BY region_sinistre ASC, rang ASC;


-- la colonne type_sinistre affiche le meme sinistre incendie dans les differentes regions
-- Il y a 12 régions multiplié par trois 3. Chaque région ayant 3 sinistres classé par ordre decroissant.



WITH classement AS (
    SELECT 
        fsm.region_sinistre, 
        fsm.sinistre_id, 
        fsm.type_sinistre, 
        fsm.montant_estime,
        ROW_NUMBER() OVER (
            PARTITION BY fsm.region_sinistre 
            ORDER BY fsm.montant_estime DESC
        ) AS rang
    FROM fact_sinistre_meteo fsm
)
SELECT 
    region_sinistre, 
    sinistre_id, 
    type_sinistre, 
    montant_estime,
    rang
FROM classement
WHERE rang <= 5
ORDER BY region_sinistre ASC, rang ASC;
 


select count(distinct fsm.region_sinistre )
from fact_sinistre_meteo fsm ;


--==========================================================
-- Question 2 Ecart entre sinistre et la moyenne de son type
--==========================================================


SELECT sinistre_id, type_sinistre, montant_estime,
round(avg(montant_estime) over(partition by type_sinistre ),2) as moyenne,
round(montant_estime - avg(montant_estime) over(partition by type_sinistre ),2) as ecart,
case
	when montant_estime > round(avg(montant_estime) over(partition by type_sinistre ),2) then 'au-dessus'
	when montant_estime < round(avg(montant_estime) over(partition by type_sinistre ),2) then 'en dessous'
	else 'egal'
end as situation
from fact_sinistre_meteo
order by sinistre_id asc;


--==========================================================
--Question 3 La part de chaque region dans le total
--==========================================================

--select region_sinistre,sinistre_id as nb_sinistre,count(*),ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct


	
with part_sinistre as(
select 
	region_sinistre,
	count(*) as nb
	from fact_sinistre_meteo
	group by region_sinistre
)
select 
region_sinistre,
nb,
round((nb::numeric/sum(nb) over ()) *100,1) as pct
from part_sinistre 
order by nb desc ;

-- avec cumul

select 
	region_sinistre,
	nb,
	pct,
	sum(pct) over (order by region_sinistre ASC) as pct_cumule
from (
select region_sinistre,
count(*) as nb,
ROUND((COUNT(*)::numeric / SUM(COUNT(*)) OVER ()) * 100, 1) AS pct
from fact_sinistre_meteo fsm 
group by fsm.region_sinistre
)
as avant_cumul
order by region_sinistre  asc;

--==================================================================
--Question 4 Le type de sinistre le plus frequent dans chaque ville
--==================================================================


WITH compte AS (
SELECT ville_sinistre , type_sinistre , COUNT(*) AS nb
FROM fact_sinistre_meteo
GROUP BY ville_sinistre , type_sinistre ),

classement AS (
SELECT ville_sinistre , type_sinistre , nb,
ROW_NUMBER() OVER (PARTITION BY ville_sinistre  ORDER BY nb  DESC) AS rang
FROM compte
)
SELECT ville_sinistre,type_sinistre, nb
FROM classement
WHERE rang = 1
ORDER BY nb DESC;

--le type de sinistre qui arrive en premier, est le meme pour chaque ville : Dégât des eaux

-- verification
select count(distinct ville_sinistre) from fact_sinistre_meteo fsm ;

--nombre de sinistre par mois,du premier au dernier mois

SELECT 
    TO_CHAR(DATE_TRUNC('month', date_survenance), 'YYYY-MM') AS mois,
    COUNT(*) AS nombre_sinistres
FROM fact_sinistre_meteo
WHERE date_survenance IS NOT NULL
GROUP BY DATE_TRUNC('month', date_survenance)
ORDER BY DATE_TRUNC('month', date_survenance) DESC;


'
WITH compte AS (
SELECT ville_sinistre, type_sinistre, COUNT(*) AS nb
FROM public.fact_sinistre_meteo
GROUP BY ville_sinistre, type_sinistre
),
parts AS (
SELECT ville_sinistre, type_sinistre, nb,
ROUND(100.0 * nb / SUM(nb) OVER (PARTITION BY ville_sinistre), 1) AS pct,
ROW_NUMBER() OVER (PARTITION BY ville_sinistre ORDER BY nb DESC) AS rang
FROM compte
)
SELECT
ville_sinistre,
MAX(CASE WHEN rang = 1 THEN pct END) AS pct_1er,
MAX(CASE WHEN rang = 2 THEN type_sinistre END) AS type_2e,
MAX(CASE WHEN rang = 2 THEN pct END) AS pct_2e
FROM parts
GROUP BY ville_sinistre
ORDER BY pct_1er DESC;
	