#!/usr/bin/env python3
"""
Expand D&D Monster Database
Quick script to add more monsters from the D&D 5e API
"""

import requests
import os
import sys
from dotenv import load_dotenv

# Add sql_schema to path
sys.path.append('sql_schema')
from monsters_schema import insert_monster_data

load_dotenv()

def get_monsters_from_api(limit=20):
    """Get monsters from D&D 5e API."""
    print(f"🐉 Downloading {limit} monsters from D&D 5e API...")
    
    try:
        # Get list of monsters
        response = requests.get("https://www.dnd5eapi.co/api/monsters")
        monsters_list = response.json()['results'][:limit]
        
        detailed_monsters = []
        
        for i, monster_ref in enumerate(monsters_list, 1):
            print(f"⏬ {i}/{limit}: {monster_ref['name']}")
            
            try:
                detail_response = requests.get(f"https://www.dnd5eapi.co{monster_ref['url']}")
                monster = detail_response.json()
                
                # Convert to our schema
                formatted = {
                    'name': monster.get('name', 'Unknown'),
                    'type': monster.get('type', 'Beast'),
                    'size': monster.get('size', 'Medium'),
                    'armor_class': monster.get('armor_class', [{}])[0].get('value', 10),
                    'hit_points': monster.get('hit_points', 1),
                    'speed': f"walk {monster.get('speed', {}).get('walk', '30 ft.')}",
                    'challenge_rating': str(monster.get('challenge_rating', 0)),
                    'abilities': format_abilities(monster.get('ability_scores', {})),
                    'skills': format_skills(monster.get('proficiencies', [])),
                    'damage_resistances': ', '.join(monster.get('damage_resistances', [])) or None,
                    'damage_immunities': ', '.join(monster.get('damage_immunities', [])) or None,
                    'condition_immunities': ', '.join([ci['name'] for ci in monster.get('condition_immunities', [])]) or None,
                    'senses': format_senses(monster.get('senses', {})),
                    'languages': ', '.join(monster.get('languages', [])) or None,
                    'special_abilities': format_abilities_list(monster.get('special_abilities', [])),
                    'actions': format_abilities_list(monster.get('actions', [])),
                    'legendary_actions': format_abilities_list(monster.get('legendary_actions', [])),
                    'source': 'D&D 5e SRD'
                }
                
                detailed_monsters.append(formatted)
                
            except Exception as e:
                print(f"⚠️  Failed: {e}")
                continue
        
        return detailed_monsters
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

def format_abilities(abilities):
    """Format ability scores."""
    if not abilities:
        return "STR 10 (+0), DEX 10 (+0), CON 10 (+0), INT 10 (+0), WIS 10 (+0), CHA 10 (+0)"
    
    parts = []
    for ability, score in abilities.items():
        modifier = (score - 10) // 2
        parts.append(f"{ability.upper()[:3]} {score} ({modifier:+d})")
    return ", ".join(parts)

def format_skills(proficiencies):
    """Format skills."""
    skills = [p for p in proficiencies if 'Skill:' in p['proficiency']['name']]
    if not skills:
        return None
    return ", ".join([f"{s['proficiency']['name'].replace('Skill: ', '')}: +{s['value']}" for s in skills])

def format_senses(senses):
    """Format senses."""
    parts = []
    for sense, value in senses.items():
        if sense != 'passive_perception':
            parts.append(f"{sense.replace('_', ' ').title()}: {value}")
    
    pp = senses.get('passive_perception', 10)
    parts.append(f"Passive Perception: {pp}")
    return ", ".join(parts)

def format_abilities_list(abilities_list):
    """Format special abilities, actions, etc."""
    if not abilities_list:
        return None
    return "; ".join([f"{a['name']}: {a.get('desc', '')[:100]}..." for a in abilities_list])

def main():
    """Main function."""
    print("🎲 D&D Monster Database Expansion")
    print("=" * 50)
    
    # Check current monster count
    print("📊 Current database: ~5-8 monsters")
    print("🎯 Goal: Add 20+ more monsters")
    
    monsters = get_monsters_from_api(20)
    
    if monsters:
        print(f"\n✅ Successfully processed {len(monsters)} monsters")
        
        # Show sample
        print("\n📋 Sample monsters:")
        for monster in monsters[:3]:
            print(f"  • {monster['name']} ({monster['type']}, CR {monster['challenge_rating']})")
        
        # Load to BigQuery
        response = input(f"\nLoad {len(monsters)} monsters to BigQuery? (y/N): ")
        if response.lower() == 'y':
            project_id = os.getenv("PROJECT_ID", "dandd-oracle")
            try:
                insert_monster_data(project_id, monsters)
                print(f"🎉 Successfully added {len(monsters)} monsters!")
                print("🔄 Restart your FastAPI server to see the new data")
            except Exception as e:
                print(f"❌ Failed to load: {e}")
        else:
            print("⏭️  Skipped loading")
    else:
        print("❌ No monsters retrieved")

if __name__ == "__main__":
    main() 