import requests
from bs4 import BeautifulSoup
import os
import time

def scrape_gita_verses(chapter=1, start_verse=1, end_verse=47):
    """
    Scrape Bhagavad Gita verses and commentaries from holy-bhagavad-gita.org
    
    Args:
        chapter: Chapter number
        start_verse: Starting verse number
        end_verse: Ending verse number
    """
    
    # Create directory for saving files
    output_dir = f"Bhagavad_Gita_Chapter_{chapter}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    base_url = "https://www.holy-bhagavad-gita.org/chapter"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"--- Starting Chapter {chapter} (Verses {start_verse}-{end_verse}) ---")
    
    for verse_num in range(start_verse, end_verse + 1):
        url = f"{base_url}/{chapter}/verse/{verse_num}/en/"
        
        try:
            print(f"Scraping Chapter {chapter}, Verse {verse_num}...", end=" ")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract verse translation
            translation_section = soup.find('div', class_='bg-verse-translation')
            verse_text = "N/A"
            if translation_section:
                verse_text = translation_section.get_text(strip=True)
            
            # Extract commentary
            commentary_section = soup.find('div', class_='bg-verse-commentary')
            commentary_text = "N/A"
            if commentary_section:
                commentary_text = commentary_section.get_text(strip=True)
            
            # Prepare content
            content = f"""BHAGAVAD GITA - CHAPTER {chapter}, VERSE {verse_num}
{'='*60}

VERSE TRANSLATION:
{'-'*60}
{verse_text}

COMMENTARY:
{'-'*60}
{commentary_text}
"""
            
            # Save to file
            filename = f"{output_dir}/Chapter_{chapter}_Verse_{verse_num:02d}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ Saved")
            
            # Be respectful to the server
            time.sleep(0.1) # 0.1-second delay between verses
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Parsing error: {e}")
    
    print(f"--- Completed Chapter {chapter}. All verses saved to {output_dir}/ ---")

if __name__ == "__main__":
    # This dictionary holds the total number of verses for each chapter.
    # Data derived from the provided index.txt 
    chapter_verse_counts = {
        1: 47,  # 
        2: 72,  # 
        3: 43,  # 
        4: 42,  # 
        5: 29,  # 
        6: 47,  # 
        7: 30,  # 
        8: 28,  # 
        9: 34,  # 
        10: 42, # 
        11: 55, # 
        12: 20, # 
        13: 35, # 
        14: 27, # 
        15: 20, # 
        16: 24, # 
        17: 28, # 
        18: 78  # 
    }
    
    print("Starting script to scrape all 18 chapters of the Bhagavad Gita...")
    
    # Loop through the dictionary and call the scraper for each chapter
    for chapter, end_verse in chapter_verse_counts.items():
        scrape_gita_verses(chapter=chapter, start_verse=1, end_verse=end_verse)
        print(f"\nMoving to next chapter...\n")
        time.sleep(0.5) # Add a 0.5-second pause between chapters
    
    print("Script finished. All chapters have been processed.")