-- BigQuery table creation for D&D Monsters
-- This schema matches the specification with all required fields

CREATE TABLE `${PROJECT_ID}.${DATASET_ID}.monsters` (
  name STRING NOT NULL,
  type STRING,
  size STRING,
  armor_class INT64,
  hit_points INT64,
  speed STRING,
  challenge_rating STRING,
  abilities STRING,
  skills STRING,
  damage_resistances STRING,
  damage_immunities STRING,
  condition_immunities STRING,
  senses STRING,
  languages STRING,
  special_abilities STRING,
  actions STRING,
  legendary_actions STRING,
  source STRING
)
PARTITION BY 
  DATE(_PARTITIONTIME)
CLUSTER BY 
  challenge_rating, type, size
OPTIONS (
  description = "D&D 5e Monster statistics and abilities",
  require_partition_filter = false
); 