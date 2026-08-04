import os
import re

def fix_uzbek_orthography(text):
    # Fix O', o', G', g' to use ‘ (U+2018)
    # Only replace if it's inside a word or followed by a word character to avoid breaking code strings
    # We look for o', O', g', G' followed by a letter (Uzbek words)
    text = re.sub(r"(?<=[oO])'(?=[a-zA-Z])", "‘", text)
    text = re.sub(r"(?<=[gG])'(?=[a-zA-Z])", "‘", text)
    
    # Sometimes it's at the end of a word or before a dash (e.g. o'g'il, o'-o'zidan)
    text = re.sub(r"(?<=[oOgG])'(?=[-\s.,!?])", "‘", text)
    text = re.sub(r"(?<=[oOgG])'(?=$)", "‘", text)

    # For tutuq belgisi ('), we replace it with ’ (U+2019)
    # It usually appears after other letters like a, e, u, i, s, n
    # We look for any letter (except o, g) followed by ' and then a letter
    text = re.sub(r"(?<=[a-zA-Z])'(?=[a-zA-Z])", "’", text)
    
    return text

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Skip virtual env and migrations
        if 'venv' in root or '.git' in root or 'migrations' in root:
            continue
        for file in files:
            if file.endswith('.py') or file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = fix_uzbek_orthography(content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    process_directory("/home/lochinbek/Desktop/yetakchilar/core")
    process_directory("/home/lochinbek/Desktop/yetakchilar/templates")
    print("Done")
