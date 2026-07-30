import os
import re

for root, dirs, files in os.walk('.'):
    if any(ignore in root for ignore in ['.git', '__pycache__', 'env', 'venv']):
        continue
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If there's a U+2018 `‘` at the end of a string literal, it's followed by `,`, `]`, `)`, `:`, or space+newline.
            # E.g. 'short_bio', -> 'short_bio',
            # 'CEO', -> 'CEO',
            # DEBUG', -> DEBUG',
            # We look for `‘` followed by `]`, `)`, `}`, `,`, `:`, or `\n`.
            new_content = re.sub(r"‘([,\])}:\n])", r"'\1", content)
            
            # Also fix things like `['short_bio']` -> `['short_bio']`
            new_content = re.sub(r"‘\]", r"']", new_content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed string literals in: {filepath}")

