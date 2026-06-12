import os
import re
from datetime import datetime
import email.utils
import json
import markdown

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def update_site():
    base_url = "https://derfbwh.github.io/apple-news-recap/"
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in ['index.html', 'cannolis.html']]
    html_files.sort(reverse=True)

    posts = []
    for filename in html_files:
        with open(filename, 'r') as f:
            content = f.read()
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1).replace(" - This Week in Apple", "") if title_match else filename
            
            # Extract date from filename (YYYY-MM-DD-...)
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
            date_str = date_match.group(1) if date_match else datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d')
            
            # Extract a brief description for RSS
            desc_match = re.search(r'<article>(.*?)</article>', content, re.DOTALL)
            description = desc_match.group(1)[:500] + "..." if desc_match else ""
            
            posts.append({
                'title': title,
                'filename': filename,
                'date': date_str,
                'description': description
            })

    # Update index.html
    items_html = ""
    rainbow_colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]
    for i, post in enumerate(posts):
        color = rainbow_colors[i % len(rainbow_colors)]
        items_html += f"""<li style="border-left: 5px solid {color};">
            <span class="date">{post["date"]}</span>
            <a href="{post["filename"]}">{post["title"]}</a>
        </li>\n"""
    
    index_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>This Week in Apple</title>
    <link rel="alternate" type="application/rss+xml" title="RSS Feed for This Week in Apple" href="feed.xml" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: "Iowan Old Style", "Palatino Linotype", "Palatino", Georgia, "Times New Roman", serif;
            line-height: 1.7;
            color: #2c2c2c;
            max-width: 740px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
            background: #fcf8f0;
        }}

        .rainbow-bar {{
            height: 6px;
            border-radius: 3px;
            background: linear-gradient(90deg,
                #e74c3c, #e67e22, #f1c40f, #2ecc71, #3498db, #9b59b6, #e74c3c);
            background-size: 200% 100%;
            margin-bottom: 2.5rem;
            animation: shimmer 6s linear infinite;
        }}

        @keyframes shimmer {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 200% 50%; }}
        }}

        header {{
            margin-bottom: 3rem;
        }}

        h1 {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #e74c3c, #e67e22, #f1c40f, #2ecc71, #3498db, #9b59b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .tagline {{
            font-size: 1.15rem;
            color: #888;
            font-style: italic;
            border-left: 3px solid #e6ddd0;
            padding-left: 1rem;
        }}

        .tagline a {{
            color: #888;
            -webkit-text-fill-color: #888;
            text-decoration: underline;
            text-decoration-color: #ddd;
            text-underline-offset: 3px;
        }}

        .tagline a:hover {{
            color: #555;
            text-decoration-color: #999;
        }}

        .count {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #bbb;
            margin-bottom: 1.5rem;
        }}

        ul {{
            list-style: none;
            padding: 0;
        }}

        li {{
            background: white;
            padding: 1.25rem 1.5rem;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03);
            margin-bottom: 1rem;
            display: flex;
            align-items: baseline;
            gap: 1.25rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}

        li:hover {{
            transform: translateX(4px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.04);
        }}

        .date {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #bbb;
            min-width: 88px;
            flex-shrink: 0;
            font-variant-numeric: tabular-nums;
            letter-spacing: 0.02em;
        }}

        a {{
            color: #2c2c2c;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 400;
            transition: color 0.15s ease;
        }}

        li:hover a {{
            color: #e67e22;
        }}

        footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #eee7dd;
            text-align: center;
            font-size: 0.85rem;
            color: #ccc;
        }}

        @media (max-width: 600px) {{
            body {{ padding: 1.5rem 1rem; }}
            h1 {{ font-size: 2rem; }}
            li {{ flex-direction: column; gap: 0.25rem; padding: 1rem 1.25rem; }}
            .date {{ min-width: auto; font-size: 0.8rem; }}
            a {{ font-size: 1rem; }}
        }}
    </style>
</head>
<body>
    <div class="rainbow-bar"></div>
    <header>
        <h1>This Week in Apple</h1>
        <p class="tagline">A weekly digest of Apple happenings &mdash; AI-generated, human-curated. <a href="feed.xml">RSS</a></p>
    </header>
    <main>
        <p class="count">{len(posts)} week{'' if len(posts) == 1 else 's'}</p>
        <ul>
            {items_html}
        </ul>
    </main>
    <footer>
        <p>&copy; 2026 This Week in Apple &middot; Powered by AI &amp; caffeine</p>
    </footer>
</body>
</html>"""
    
    with open('index.html', 'w') as f:
        f.write(index_template)

    # Update feed.xml
    rss_items = ""
    for post in posts:
        link = f"{base_url}{post['filename']}"
        dt = datetime.strptime(post['date'], "%Y-%m-%d")
        pub_date = email.utils.formatdate(dt.timestamp(), localtime=False)
        rss_items += f"""
        <item>
            <title>{post['title']}</title>
            <link>{link}</link>
            <guid isPermaLink="true">{link}</guid>
            <pubDate>{pub_date}</pubDate>
            <description><![CDATA[{post['description']}]]></description>
        </item>"""

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>This Week in Apple</title>
    <link>{base_url}</link>
    <description>A weekly recap of everything Apple. <b>Generated by AI.</b></description>
    <language>en-us</language>
    <lastBuildDate>{email.utils.formatdate(datetime.now().timestamp(), localtime=False)}</lastBuildDate>
    <atom:link href="{base_url}feed.xml" rel="self" type="application/rss+xml" />
    {rss_items}
</channel>
</rss>"""

    with open('feed.xml', 'w') as f:
        f.write(rss_content)

if __name__ == "__main__":
    update_site()
