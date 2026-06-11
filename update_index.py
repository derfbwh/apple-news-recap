import os
import re
from datetime import datetime

def update_index():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in ['index.html', 'cannolis.html']]
    html_files.sort(reverse=True) # Assuming filenames are sortable by date or sequence

    issue_items = []
    for filename in html_files:
        with open(filename, 'r') as f:
            content = f.read()
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else filename
            
            # Try to extract date from filename or content
            # For now, let's just use the file modification time if not in filename
            date_str = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%B %d, %Y')
            
            issue_items.append(f'<li><a href="{filename}">{title}</a><span class="date">{date_str}</span></li>')

    with open('index.html', 'r') as f:
        index_content = f.read()

    new_list_content = '\n'.join(issue_items)
    updated_content = re.sub(r'<!-- Issues will be added here -->', new_list_content, index_content)

    with open('index.html', 'w') as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_index()
