#!/usr/bin/env python3
"""
Data Expansion Guide for Dungeon Master's Oracle
Load hundreds of D&D monsters from various sources
"""

import os
import sys
import pandas as pd
import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add sql_schema to path
sys.path.append('sql_schema')
from monsters_schema import insert_monster_data, validate_monster_data

load_dotenv()

def download_dnd_5e_api_monsters():
    """Download monsters from the D&D 5e API."""
    print("🐉 Downloading monsters from D&D 5e API...")
    
    try:
        # Get list of all monsters
        response = requests.get("https://www.dnd5eapi.co/api/monsters", timeout=10)
        monsters_list = response.json()['results']
        
        print(f"📋 Found {len(monsters_list)} monsters in API")
        
        detailed_monsters = []
        
        for i, monster_ref in enumerate(monsters_list[:50], 1):  # Limit to first 50 for now
            print(f"⏬ Downloading {i}/50: {monster_ref['name']}")
            
            try:
                detail_response = requests.get(f"https://www.dnd5eapi.co{monster_ref['url']}", timeout=5)
                monster_detail = detail_response.json()
                
                # Convert to our schema format
                formatted_monster = format_api_monster(monster_detail)
                if formatted_monster:
                    detailed_monsters.append(formatted_monster)
                    
            except Exception as e:
                print(f"⚠️  Failed to get details for {monster_ref['name']}: {e}")
                continue
        
        print(f"✅ Successfully processed {len(detailed_monsters)} monsters")
        return detailed_monsters
        
    except Exception as e:
        print(f"❌ Failed to download from D&D 5e API: {e}")
        return []

def format_api_monster(monster: Dict) -> Dict[str, Any]:
    """Convert D&D 5e API format to our BigQuery schema."""
    try:
        # Extract basic info
        name = monster.get('name', 'Unknown')
        size = monster.get('size', 'Medium')
        monster_type = monster.get('type', 'Unknown')
        
        # Handle alignment
        alignment_obj = monster.get('alignment', 'Neutral')
        if isinstance(alignment_obj, dict):
            alignment = alignment_obj.get('name', 'Neutral')
        else:
            alignment = str(alignment_obj)
        
        # Extract stats
        armor_class = None
        if monster.get('armor_class'):
            armor_class = monster['armor_class'][0].get('value', 10)
        
        hit_points = monster.get('hit_points', 1)
        
        # Handle speed
        speed_obj = monster.get('speed', {})
        if isinstance(speed_obj, dict):
            speed_parts = []
            for speed_type, value in speed_obj.items():
                if speed_type != 'hover':
                    speed_parts.append(f"{speed_type} {value}")
            speed = ", ".join(speed_parts) if speed_parts else "30 ft."
        else:
            speed = "30 ft."
        
        # Challenge rating
        cr = monster.get('challenge_rating', 0)
        if isinstance(cr, (int, float)):
            challenge_rating = str(cr)
        else:
            challenge_rating = "0"
        
        # Abilities
        abilities_obj = monster.get('ability_scores', {})
        if abilities_obj:
            abilities = f"STR {abilities_obj.get('strength', 10)} ({(abilities_obj.get('strength', 10)-10)//2:+d}), " \
                       f"DEX {abilities_obj.get('dexterity', 10)} ({(abilities_obj.get('dexterity', 10)-10)//2:+d}), " \
                       f"CON {abilities_obj.get('constitution', 10)} ({(abilities_obj.get('constitution', 10)-10)//2:+d}), " \
                       f"INT {abilities_obj.get('intelligence', 10)} ({(abilities_obj.get('intelligence', 10)-10)//2:+d}), " \
                       f"WIS {abilities_obj.get('wisdom', 10)} ({(abilities_obj.get('wisdom', 10)-10)//2:+d}), " \
                       f"CHA {abilities_obj.get('charisma', 10)} ({(abilities_obj.get('charisma', 10)-10)//2:+d})"
        else:
            abilities = "STR 10 (+0), DEX 10 (+0), CON 10 (+0), INT 10 (+0), WIS 10 (+0), CHA 10 (+0)"
        
        # Skills
        skills_list = monster.get('proficiencies', [])
        skills = ", ".join([f"{skill['proficiency']['name']}: +{skill['value']}" 
                           for skill in skills_list if 'Skill:' in skill['proficiency']['name']])
        
        # Damage resistances/immunities
        damage_resistances = ", ".join(monster.get('damage_resistances', []))
        damage_immunities = ", ".join(monster.get('damage_immunities', []))
        condition_immunities = ", ".join([ci['name'] for ci in monster.get('condition_immunities', [])])
        
        # Senses
        senses_obj = monster.get('senses', {})
        senses_parts = []
        for sense_type, value in senses_obj.items():
            if sense_type != 'passive_perception':
                senses_parts.append(f"{sense_type.replace('_', ' ').title()}: {value}")
        
        passive_perception = senses_obj.get('passive_perception', 10)
        senses_parts.append(f"Passive Perception: {passive_perception}")
        senses = ", ".join(senses_parts)
        
        # Languages
        languages = ", ".join(monster.get('languages', [])) or None
        
        # Special abilities
        special_abilities_list = monster.get('special_abilities', [])
        special_abilities = "; ".join([f"{sa['name']}: {sa.get('desc', '')}" 
                                     for sa in special_abilities_list])
        
        # Actions
        actions_list = monster.get('actions', [])
        actions = "; ".join([f"{action['name']}: {action.get('desc', '')}" 
                           for action in actions_list])
        
        # Legendary actions
        legendary_actions_list = monster.get('legendary_actions', [])
        legendary_actions = "; ".join([f"{la['name']}: {la.get('desc', '')}" 
                                     for la in legendary_actions_list]) if legendary_actions_list else None
        
        formatted_monster = {
            'name': name,
            'type': monster_type,
            'size': size,
            'armor_class': armor_class,
            'hit_points': hit_points,
            'speed': speed,
            'challenge_rating': challenge_rating,
            'abilities': abilities,
            'skills': skills if skills else None,
            'damage_resistances': damage_resistances if damage_resistances else None,
            'damage_immunities': damage_immunities if damage_immunities else None,
            'condition_immunities': condition_immunities if condition_immunities else None,
            'senses': senses,
            'languages': languages,
            'special_abilities': special_abilities if special_abilities else None,
            'actions': actions if actions else None,
            'legendary_actions': legendary_actions,
            'source': 'D&D 5e SRD'
        }
        
        return formatted_monster
        
    except Exception as e:
        print(f"⚠️  Error formatting monster {monster.get('name', 'Unknown')}: {e}")
        return None

def create_additional_monsters():
    """Create additional custom monsters to expand the database."""
    print("🎭 Creating additional custom monsters...")
    
    additional_monsters = [
        {
            'name': 'Dire Wolf',
            'type': 'Beast',
            'size': 'Large',
            'armor_class': 14,
            'hit_points': 37,
            'speed': '50 ft.',
            'challenge_rating': '1',
            'abilities': 'STR 17 (+3), DEX 15 (+2), CON 15 (+2), INT 3 (-4), WIS 12 (+1), CHA 7 (-2)',
            'skills': 'Perception +3, Stealth +4',
            'damage_resistances': None,
            'damage_immunities': None,
            'condition_immunities': None,
            'senses': 'Darkvision 60 ft., Passive Perception 13',
            'languages': None,
            'special_abilities': 'Keen Hearing and Smell, Pack Tactics',
            'actions': 'Bite: +5 to hit, 2d6+3 piercing damage, target prone if Large or smaller',
            'legendary_actions': None,
            'source': 'Monster Manual'
        },
        {
            'name': 'Troll',
            'type': 'Giant',
            'size': 'Large',
            'armor_class': 15,
            'hit_points': 84,
            'speed': '30 ft.',
            'challenge_rating': '5',
            'abilities': 'STR 18 (+4), DEX 13 (+1), CON 20 (+5), INT 7 (-2), WIS 9 (-1), CHA 7 (-2)',
            'skills': 'Perception +2',
            'damage_resistances': None,
            'damage_immunities': None,
            'condition_immunities': None,
            'senses': 'Darkvision 60 ft., Passive Perception 12',
            'languages': 'Giant',
            'special_abilities': 'Keen Smell, Regeneration (10 hp per turn unless fire/acid damage)',
            'actions': 'Multiattack, Bite (+7, 1d6+4), Claw (+7, 2d6+4)',
            'legendary_actions': None,
            'source': 'Monster Manual'
        },
        {
            'name': 'Mind Flayer',
            'type': 'Aberration',
            'size': 'Medium',
            'armor_class': 15,
            'hit_points': 71,
            'speed': '30 ft., fly 30 ft. (hover)',
            'challenge_rating': '7',
            'abilities': 'STR 11 (+0), DEX 12 (+1), CON 12 (+1), INT 19 (+4), WIS 17 (+3), CHA 17 (+3)',
            'skills': 'Arcana +7, Deception +6, Insight +6, Perception +6, Persuasion +6, Stealth +4',
            'damage_resistances': None,
            'damage_immunities': None,
            'condition_immunities': None,
            'senses': 'Darkvision 120 ft., Passive Perception 16',
            'languages': 'Deep Speech, Undercommon, telepathy 120 ft.',
            'special_abilities': 'Magic Resistance, Spellcasting',
            'actions': 'Tentacles, Extract Brain, Mind Blast (recharge 5-6)',
            'legendary_actions': None,
            'source': 'Monster Manual'
        }
    ]
    
    return additional_monsters

def load_monsters_to_bigquery(monsters: List[Dict]):
    """Load monsters into BigQuery."""
    print(f"📊 Loading {len(monsters)} monsters to BigQuery...")
    
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    
    try:
        # Validate all monsters first
        validated_monsters = []
        for monster in monsters:
            try:
                validated_monster = validate_monster_data(monster)
                validated_monsters.append(validated_monster)
            except Exception as e:
                print(f"⚠️  Validation failed for {monster.get('name', 'Unknown')}: {e}")
                continue
        
        print(f"✅ Validated {len(validated_monsters)} monsters")
        
        if validated_monsters:
            insert_monster_data(project_id, validated_monsters)
            print(f"🎉 Successfully loaded {len(validated_monsters)} monsters to BigQuery!")
            return True
        else:
            print("❌ No valid monsters to load")
            return False
            
    except Exception as e:
        print(f"❌ Failed to load monsters to BigQuery: {e}")
        return False

def main():
    """Main data expansion function."""
    print("📈 Dungeon Master's Oracle - Data Expansion")
    print("=" * 60)
    
    print(f"📊 Current Status: ~5 monsters (very limited!)")
    print(f"🎯 Goal: 100+ monsters for a useful D&D tool")
    print()
    
    all_monsters = []
    
    # Option 1: Download from D&D 5e API
    print("Option 1: Download from D&D 5e API")
    response = input("Download 50 monsters from D&D 5e API? (y/N): ")
    if response.lower() == 'y':
        api_monsters = download_dnd_5e_api_monsters()
        all_monsters.extend(api_monsters)
    
    # Option 2: Add custom monsters
    print("\nOption 2: Add custom monsters")
    response = input("Add 3 additional custom monsters? (y/N): ")
    if response.lower() == 'y':
        custom_monsters = create_additional_monsters()
        all_monsters.extend(custom_monsters)
    
    # Load to BigQuery
    if all_monsters:
        print(f"\n📊 Total monsters to load: {len(all_monsters)}")
        response = input("Load all monsters to BigQuery? (y/N): ")
        if response.lower() == 'y':
            success = load_monsters_to_bigquery(all_monsters)
            if success:
                print("\n🎉 Data expansion completed!")
                print(f"Your Oracle now has much more data to work with!")
            else:
                print("\n❌ Data expansion failed")
        else:
            print("⏭️  Skipped BigQuery loading")
    else:
        print("\n📝 No monsters selected for loading")
    
    print("\n💡 Additional Data Sources to Consider:")
    print("   • More monsters from D&D 5e API (there are 300+)")
    print("   • Spells database")
    print("   • Magic items")
    print("   • D&D rules and lore text")
    print("   • Custom homebrew content")

if __name__ == "__main__":
    main() 