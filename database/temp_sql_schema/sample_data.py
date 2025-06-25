"""
Sample monster data for testing the BigQuery schema
Demonstrates the exact data structure and format expected
"""

from typing import List, Dict, Any

# Sample monster data matching the schema
SAMPLE_MONSTERS: List[Dict[str, Any]] = [
    {
        "name": "Adult Red Dragon",
        "type": "Dragon",
        "size": "Huge",
        "armor_class": 19,
        "hit_points": 256,
        "speed": "40 ft., climb 40 ft., fly 80 ft.",
        "challenge_rating": "17",
        "abilities": "STR 27 (+8), DEX 10 (+0), CON 25 (+7), INT 16 (+3), WIS 13 (+1), CHA 21 (+5)",
        "skills": "Perception +13, Stealth +6",
        "damage_resistances": None,
        "damage_immunities": "Fire",
        "condition_immunities": None,
        "senses": "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 23",
        "languages": "Common, Draconic",
        "special_abilities": "Legendary Resistance (3/Day), Fire Breath (Recharge 5–6)",
        "actions": "Multiattack, Bite, Claw, Tail, Fire Breath",
        "legendary_actions": "Detect, Tail Attack, Wing Attack (Costs 2 Actions)",
        "source": "Monster Manual"
    },
    {
        "name": "Goblin",
        "type": "Humanoid",
        "size": "Small",
        "armor_class": 15,
        "hit_points": 7,
        "speed": "30 ft.",
        "challenge_rating": "1/4",
        "abilities": "STR 8 (-1), DEX 14 (+2), CON 10 (+0), INT 10 (+0), WIS 8 (-1), CHA 8 (-1)",
        "skills": "Stealth +6",
        "damage_resistances": None,
        "damage_immunities": None,
        "condition_immunities": None,
        "senses": "Darkvision 60 ft., Passive Perception 9",
        "languages": "Common, Goblin",
        "special_abilities": "Nimble Escape",
        "actions": "Scimitar, Shortbow",
        "legendary_actions": None,
        "source": "Monster Manual"
    },
    {
        "name": "Beholder",
        "type": "Aberration",
        "size": "Large",
        "armor_class": 18,
        "hit_points": 180,
        "speed": "0 ft., fly 20 ft. (hover)",
        "challenge_rating": "13",
        "abilities": "STR 10 (+0), DEX 14 (+2), CON 18 (+4), INT 17 (+3), WIS 15 (+2), CHA 17 (+3)",
        "skills": "Perception +12",
        "damage_resistances": None,
        "damage_immunities": None,
        "condition_immunities": "Prone",
        "senses": "Darkvision 120 ft., Passive Perception 22",
        "languages": "Deep Speech, Undercommon",
        "special_abilities": "Antimagic Cone, Death Ray, Disintegration Ray, Fear Ray, Paralyzing Ray, Petrification Ray, Sleep Ray, Slowing Ray, Telekinetic Ray, Charm Ray, Eye Rays",
        "actions": "Bite, Eye Rays",
        "legendary_actions": "Eye Ray",
        "source": "Monster Manual"
    },
    {
        "name": "Owlbear",
        "type": "Monstrosity",
        "size": "Large",
        "armor_class": 13,
        "hit_points": 59,
        "speed": "40 ft.",
        "challenge_rating": "3",
        "abilities": "STR 20 (+5), DEX 12 (+1), CON 17 (+3), INT 3 (-4), WIS 12 (+1), CHA 7 (-2)",
        "skills": "Perception +3",
        "damage_resistances": None,
        "damage_immunities": None,
        "condition_immunities": None,
        "senses": "Darkvision 60 ft., Passive Perception 13",
        "languages": None,
        "special_abilities": "Keen Sight and Smell",
        "actions": "Multiattack, Beak, Claws",
        "legendary_actions": None,
        "source": "Monster Manual"
    },
    {
        "name": "Lich",
        "type": "Undead",
        "size": "Medium",
        "armor_class": 17,
        "hit_points": 135,
        "speed": "30 ft.",
        "challenge_rating": "21",
        "abilities": "STR 11 (+0), DEX 16 (+3), CON 16 (+3), INT 20 (+5), WIS 14 (+2), CHA 16 (+3)",
        "skills": "Arcana +18, History +12, Insight +9, Perception +9",
        "damage_resistances": "Cold, Lightning, Necrotic",
        "damage_immunities": "Poison; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks",
        "condition_immunities": "Charmed, Exhaustion, Frightened, Paralyzed, Poisoned",
        "senses": "Truesight 120 ft., Passive Perception 19",
        "languages": "Common plus up to five other languages",
        "special_abilities": "Legendary Resistance (3/Day), Rejuvenation, Spellcasting, Turn Resistance",
        "actions": "Paralyzing Touch, Spellcasting",
        "legendary_actions": "Cantrip, Paralyzing Touch (Costs 2 Actions), Frightening Gaze (Costs 2 Actions), Disrupt Life (Costs 3 Actions)",
        "source": "Monster Manual"
    }
]

def format_for_insert() -> List[Dict[str, Any]]:
    """
    Format sample data for BigQuery insertion.
    Ensures all fields are present and properly typed.
    """
    formatted_monsters = []
    
    for monster in SAMPLE_MONSTERS:
        # Ensure all schema fields are present
        formatted_monster = {
            "name": monster["name"],
            "type": monster.get("type"),
            "size": monster.get("size"),
            "armor_class": monster.get("armor_class"),
            "hit_points": monster.get("hit_points"),
            "speed": monster.get("speed"),
            "challenge_rating": monster.get("challenge_rating"),
            "abilities": monster.get("abilities"),
            "skills": monster.get("skills"),
            "damage_resistances": monster.get("damage_resistances"),
            "damage_immunities": monster.get("damage_immunities"),
            "condition_immunities": monster.get("condition_immunities"),
            "senses": monster.get("senses"),
            "languages": monster.get("languages"),
            "special_abilities": monster.get("special_abilities"),
            "actions": monster.get("actions"),
            "legendary_actions": monster.get("legendary_actions"),
            "source": monster.get("source")
        }
        formatted_monsters.append(formatted_monster)
    
    return formatted_monsters

# Example queries for the schema
EXAMPLE_QUERIES = [
    {
        "description": "Find all dragons",
        "sql": "SELECT name, challenge_rating, hit_points FROM `{project}.{dataset}.monsters` WHERE type = 'Dragon'"
    },
    {
        "description": "High CR monsters (CR 10+)",
        "sql": """
        SELECT name, type, challenge_rating, armor_class 
        FROM `{project}.{dataset}.monsters` 
        WHERE SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\d+)') AS INT64) >= 10
        ORDER BY SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\d+)') AS INT64) DESC
        """
    },
    {
        "description": "Monsters with fire immunity",
        "sql": "SELECT name, type, damage_immunities FROM `{project}.{dataset}.monsters` WHERE damage_immunities LIKE '%Fire%'"
    },
    {
        "description": "Large or larger monsters",
        "sql": "SELECT name, size, hit_points FROM `{project}.{dataset}.monsters` WHERE size IN ('Large', 'Huge', 'Gargantuan')"
    },
    {
        "description": "Monsters with legendary actions",
        "sql": "SELECT name, challenge_rating, legendary_actions FROM `{project}.{dataset}.monsters` WHERE legendary_actions IS NOT NULL"
    }
]

if __name__ == "__main__":
    # Print sample data structure
    print("Sample Monster Data Structure:")
    print("=" * 50)
    
    for i, monster in enumerate(SAMPLE_MONSTERS[:2], 1):
        print(f"\nMonster {i}: {monster['name']}")
        print("-" * 30)
        for key, value in monster.items():
            print(f"{key:20}: {value}")
    
    print(f"\nTotal sample monsters: {len(SAMPLE_MONSTERS)}")
    
    # Print example queries
    print("\nExample Queries:")
    print("=" * 50)
    for query in EXAMPLE_QUERIES:
        print(f"\n{query['description']}:")
        print(query['sql']) 