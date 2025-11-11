import os
import csv
import time
import google.generativeai as genai
from pathlib import Path

# Configure Gemini API
# IMPORTANT: Replace with your actual API key in your local environment
# It's safer to use environment variables, but for this script, we'll use the placeholder
GEMINI_API_KEY = "8===============D"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def read_verse_file(filepath):
    """Read a verse file and extract its content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def get_chapter_persona(chapter_num):
    """Get the specialized persona for each chapter based on Gita-18 Expert Framework"""
    personas = {
        1: "CrisisCore - an empathetic divine counselor who deeply understands human dilemmas, grief, and moral confusion",
        2: "AtmaAnalytics - a wise teacher of eternal truth, expert in the immortal self and the steady mind",
        3: "ActionFlow - a guide to selfless action and Karma Yoga, helping overcome laziness and burnout",
        4: "KarmicKnowledge - an enlightened master of the synergy between knowledge and action",
        5: "ZenithOS - a philosopher of engaged detachment, expert in renunciation of fruits while remaining active",
        6: "MindfulModulator - a meditation master offering practical techniques for mental control and inner stability",
        7: "SourceCode - a metaphysical expert revealing the divine source code and the illusion of Maya",
        8: "Continuum - a guide through life's transitions, expert in death and the soul's journey",
        9: "OmniPresence - a revealer of the royal secret, showing how the divine pervades all creation",
        10: "AweMatrix - a divine pattern recognizer, revealing the supreme in all categories to inspire devotion",
        11: "CosmosView - a cosmic visionary showing the overwhelming Universal Form",
        12: "DevotionAI - a loving advocate of Bhakti Yoga, champion of the devotional path",
        13: "FieldScanner - a precise analyst distinguishing the Field from the Knower",
        14: "GunaClassifier - a diagnostic sage identifying Sattva, Rajas, and Tamas",
        15: "NexusCut - a metaphysical strategist wielding the axe of detachment",
        16: "VirtueCompass - an ethical guide distinguishing divine qualities from demonic traits",
        17: "LifestyleOps - a practical advisor classifying faith, food, charity, and austerity",
        18: "MokshaPath - the master of liberation, teaching the path of total surrender"
    }
    return personas.get(chapter_num, "a divine, enlightened being")

def generate_qa_pairs(verse_content, chapter_num, verse_num, model):
    """
    Generate Q&A pairs for real-life problems based on the verse's wisdom.
    The AI generates both realistic user questions and divine answers from ALL possible angles.
    """
    
    persona = get_chapter_persona(chapter_num)
    
    prompt = f"""You are {persona}, a divine being speaking directly to seekers about their life problems.

First, read and deeply internalize the wisdom from this verse:

{verse_content}

Now, your task is to generate AS MANY realistic Q&A pairs as possible, exploring ALL ANGLES and perspectives where this verse's wisdom can help people with their life problems.

Think comprehensively:
- Different age groups (students, professionals, parents, elderly)
- Different life areas (career, relationships, health, money, purpose)
- Different emotional states (anxiety, anger, confusion, grief, fear)
- Different situations (crisis, daily struggles, transitions, conflicts)

QUESTION GUIDELINES:
- Make questions sound like real people asking for help with their problems
- Focus on modern, relatable life situations
- Keep questions conversational and genuine
- Questions should fit Chapter {chapter_num}'s expertise area
- Cover DIVERSE scenarios - don't repeat similar problems

ANSWER GUIDELINES:
- Speak as a divine being directly to the seeker (use "you", "your")
- Keep each answer to ONE SHORT PARAGRAPH (3-5 sentences maximum)
- Be warm, wise, compassionate, and authoritative
- Apply the verse's wisdom naturally without mentioning "the verse says" or "according to scripture"
- Speak like Krishna to Arjuna - personal, loving, yet profound
- Make it feel like divine guidance, not a lecture
- Avoid jargon - use simple, clear language
- Ensure answers are one liners

Format your response EXACTLY as follows:

Q: [Create a realistic life problem question]
A: [Your divine answer in one short paragraph]

Q: [Create another realistic life problem question from a DIFFERENT angle]  
A: [Your divine answer in one short paragraph]

(Continue generating as many Q&A pairs as you can think of)

CRITICAL: Generate maximum Q&A pairs exploring different angles. Do not generate questions about the verse itself, Sanskrit terms, or Gita characters."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating Q&A for Chapter {chapter_num}, Verse {verse_num}: {e}")
        try:
            print("Retrying after error...")
            time.sleep(5)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            print(f"Retry failed for Chapter {chapter_num}, Verse {verse_num}: {e2}")
            return None

def parse_qa_response(response_text):
    """Parse the Gemini response into a list of Q&A pairs"""
    qa_pairs = []
    lines = response_text.strip().split('\n')
    
    current_question = None
    current_answer = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Q:'):
            if current_question and current_answer:
                qa_pairs.append({
                    'question': current_question,
                    'answer': ' '.join(current_answer).strip()
                })
            current_question = line[2:].strip()
            current_answer = []
            
        elif line.startswith('A:'):
            current_answer.append(line[2:].strip())
            
        elif current_question and not line.startswith('Q:'):
            current_answer.append(line)
    
    if current_question and current_answer:
        qa_pairs.append({
            'question': current_question,
            'answer': ' '.join(current_answer).strip()
        })
    
    return qa_pairs

def process_chapter(chapter_num, input_dir, output_dir, model):
    """Process all verses in a chapter and generate Q&A CSV"""
    
    chapter_dir = Path(input_dir) / f"Bhagavad_Gita_Chapter_{chapter_num}"
    
    if not chapter_dir.exists():
        print(f"Directory not found: {chapter_dir}")
        return
    
    verse_files = sorted(chapter_dir.glob("Chapter_*.txt"))
    
    if not verse_files:
        print(f"No verse files found in {chapter_dir}")
        return
    
    print(f"\n{'='*70}")
    print(f"Processing Chapter {chapter_num} - Found {len(verse_files)} verses")
    print(f"Gemini will generate Q&A pairs from ALL possible angles")
    print(f"{'='*70}")
    
    all_qa_pairs = []
    output_file = Path(output_dir) / f"Chapter_{chapter_num}_QA.csv"
    
    for verse_file in verse_files:
        verse_num = int(verse_file.stem.split('_')[-1])
        print(f"Processing Chapter {chapter_num}, Verse {verse_num}/{len(verse_files)}...", end=" ")
        
        verse_content = read_verse_file(verse_file)
        qa_response = generate_qa_pairs(verse_content, chapter_num, verse_num, model)
        
        if qa_response:
            qa_pairs = parse_qa_response(qa_response)
            
            for qa in qa_pairs:
                qa['chapter'] = chapter_num
                qa['verse_source'] = f"{chapter_num}.{verse_num}"
                all_qa_pairs.append(qa)
            
            print(f"✓ Generated {len(qa_pairs)} Q&A pairs (Total: {len(all_qa_pairs)})")
            
            # Save progress every 5 verses
            if verse_num % 5 == 0 and all_qa_pairs:
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['chapter', 'verse_source', 'question', 'answer']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(all_qa_pairs)
                print(f"  💾 Saved progress to {output_file.name}")
        else:
            print("✗ Failed")
        
        time.sleep(2)  # Be respectful to API
    
    # Final save
    if all_qa_pairs:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['chapter', 'verse_source', 'question', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_qa_pairs)
        
        print(f"\n{'='*70}")
        print(f"✓ Chapter {chapter_num} complete!")
        print(f"  Total Q&A pairs: {len(all_qa_pairs)}")
        print(f"  Saved to: {output_file}")
        print(f"{'='*70}")
    else:
        print(f"\n✗ No Q&A pairs generated for Chapter {chapter_num}")

def main():
    """Main function to process all chapters"""
    
    INPUT_BASE_DIR = "."  # Current directory where chapter folders are
    OUTPUT_DIR = "QA_Datasets"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("\n" + "="*70)
    print("BHAGAVAD GITA Q&A DATASET GENERATOR")
    print("Gita-18 Expert Framework - Life Problems Focus")
    print("="*70)
    print(f"Input directory: {INPUT_BASE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*70)
    
    # Get user input
    chapters_input = input("\nEnter chapter numbers to process (e.g., '1-3, 5, 18' or 'all'): ")
    
    # Parse chapter input
    process_list = []
    if chapters_input.lower() == 'all':
        process_list = range(1, 19)
    else:
        try:
            parts = chapters_input.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    process_list.extend(range(start, end + 1))
                else:
                    process_list.append(int(part))
            process_list = sorted(list(set(process_list)))
        except ValueError:
            print("Invalid input. Please use format like '1-3, 5, 18'. Exiting.")
            return

    print(f"\nProcessing chapters: {process_list}")
    print("Generating maximum Q&A pairs per verse\n")

    # Process each chapter
    for chapter_num in process_list:
        if chapter_num < 1 or chapter_num > 18:
            print(f"Skipping invalid chapter number: {chapter_num}")
            continue
        try:
            process_chapter(chapter_num, INPUT_BASE_DIR, OUTPUT_DIR, model)
            print(f"\nPausing before next chapter...\n")
            time.sleep(5)
        except Exception as e:
            print(f"\n✗ Error processing Chapter {chapter_num}: {e}")
            continue
    
    print("\n" + "="*70)
    print("✓ ALL SELECTED CHAPTERS PROCESSED!")
    print("="*70)
    print(f"\nYour Q&A datasets are ready in the '{OUTPUT_DIR}' folder.")
    print("Each CSV contains: chapter, verse_source, question, answer")

if __name__ == "__main__":
    main()
