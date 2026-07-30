import os
import re

directories = ['templates', 'core']
extensions = ['.html', '.py']

# Characters to look for: ', ', ’, ʻ, ʼ, `
ap_chars = r"['‘’ʻʼ`]"

def fix_text(text):
    # 1. Fix O', o', G', g' -> O', o', G', g‘ (U+2018)
    # We will match O/o/G/g followed by any apostrophe-like char.
    # To avoid matching HTML (like `<img src='...png'>`), we ensure itʼs followed by a valid Uzbek letter OR itʼs preceded by one.
    # Actually, in words like "O‘zbek", "o'" is followed by "z".
    # In words like "tog‘", "g'" is preceded by "o".
    # So we replace if it is preceded or followed by an Uzbek letter.
    # BUT wait, "png'" -> 'g' is preceded by 'n'. 'n' is a letter. So it would match!
    # To fix this, we ONLY match if the preceding letter is an Uzbek vowel (a, e, i, o, u, o').
    # E.g. "tog‘" -> 'o' is a vowel. "bog‘" -> 'o' is a vowel.
    # Are there any Uzbek words ending in g' where the preceding letter is a consonant? No, itʼs always a vowel.
    # What about o' at the end of a word? "Xato'"? No, "xato". There is no word ending in o'.
    
    # Pattern 1: O/o/G/g + apostrophe + letter
    text = re.sub(r"([OoGg])" + ap_chars + r"(?=[a-zA-Z])", r"\1‘", text)
    
    # Pattern 2: Vowel + O/o/G/g + apostrophe + NOT a letter (end of word)
    text = re.sub(r"([aAeEiIoOuU][OoGg])" + ap_chars + r"(?![a-zA-Z])", r"\1‘", text)
    
    # Now for tutuq belgisi (ʼ, U+02BC)
    # It occurs between two letters (e.g. maʼno, aʼzo, sanʼat).
    # Since we already converted o' and g' to ‘ (U+2018), any remaining apostrophe between two letters 
    # (that is NOT an HTML attribute) should be tutuq belgisi.
    # Wait, in HTML, `<div class='hero'>` -> `s='h` -> NOT two letters (itʼs =').
    # `data-test='abc'` -> `t='a` -> not two letters.
    # So between two letters `(?<=[a-zA-Z])` and `(?=[a-zA-Z])` is extremely safe!
    # EXCEPT for English words like "donʼt", "itʼs". The prompt says "Zarurat bo‘lmasa chet tillaridagi so‘zlarni ishlatma."
    # So we just convert all of them to tutuq belgisi.
    # One exception: `‘` is now used for o‘ and g', so we shouldnʼt overwrite it!
    # So we look for any apostrophe-like char EXCEPT `‘` between two letters.
    ap_chars_except_left_quote = r"['’ʻʼ`]"
    text = re.sub(r"(?<=[a-zA-Z])" + ap_chars_except_left_quote + r"(?=[a-zA-Z])", "ʼ", text)
    
    # Also, the user asked to replace straight quotes with curly quotes for IQTIBOS.
    # "..." -> “...”
    # This is dangerous with regex because of HTML attributes `class="..."`.
    # Letʼs skip quotes for now or do it manually if needed, because the user said "Oddiy qo‘shtirnoqni faqat foydalanuvchi talab qilganda ishlat", but breaking HTML is worse.
    # Actually, we can replace "..." if itʼs NOT inside a tag. But letʼs leave it for manual if we spot any.

    return text

for root, dirs, files in os.walk('.'):
    if any(ignore in root for ignore in ['.git', '__pycache__', 'env', 'venv', 'media', 'static', 'migrations']):
        continue
    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = fix_text(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed: {filepath}")

