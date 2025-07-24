#!/usr/bin/env python3
"""
HTML Publisher for 30-Day Challenge

Convert markdown blogs to beautiful HTML pages for GitHub Pages.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class HTMLPublisher:
    """Convert markdown blogs to HTML pages"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.config_dir = root_dir / "config"
        self.docs_dir = root_dir / "docs"
        
        # Create docs directory for GitHub Pages
        self.docs_dir.mkdir(exist_ok=True)
        
        # Load roadmap
        with open(self.config_dir / "challenge_roadmap.json", "r", encoding="utf-8") as f:
            self.roadmap = json.load(f)
    
    def convert_markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with Korean support"""
        
        # Convert headers
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', markdown_content, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Convert code blocks
        html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', 
                      html, flags=re.DOTALL)
        
        # Convert inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Convert bold text
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        
        # Convert italic text
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Convert links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # Convert lists
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
        html = re.sub(r'</ul>\s*<ul>', '', html)  # Merge consecutive lists
        
        # Convert line breaks
        html = re.sub(r'\n\n', '</p><p>', html)
        html = '<p>' + html + '</p>'
        
        # Clean up empty paragraphs
        html = re.sub(r'<p></p>', '', html)
        html = re.sub(r'<p>\s*</p>', '', html)
        
        return html
    
    def get_page_template(self) -> str:
        """Get HTML template for blog pages"""
        return '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 30일 uv Python 챌린지</title>
    <meta name="description" content="{description}">
    <meta name="author" content="Reasonofmoon">
    
    <!-- Open Graph for social sharing -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://reasonofmoon.github.io/30-day-uv-python-challenge/{filename}">
    
    <!-- CSS Styling -->
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --accent-color: #f59e0b;
            --text-color: #1f2937;
            --bg-color: #ffffff;
            --code-bg: #f8fafc;
            --border-color: #e2e8f0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background-color: var(--bg-color);
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
            border-bottom: 3px solid var(--primary-color);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            color: var(--secondary-color);
            font-weight: 500;
        }}
        
        .navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background-color: var(--code-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .nav-link {{
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        
        .nav-link:hover {{
            background-color: var(--primary-color);
            color: white;
        }}
        
        .content {{
            line-height: 1.8;
        }}
        
        .content h1 {{
            font-size: 2.2rem;
            color: var(--primary-color);
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
        }}
        
        .content h2 {{
            font-size: 1.8rem;
            color: var(--text-color);
            margin: 2rem 0 1rem 0;
            border-left: 4px solid var(--primary-color);
            padding-left: 1rem;
        }}
        
        .content h3 {{
            font-size: 1.4rem;
            color: var(--text-color);
            margin: 1.5rem 0 0.5rem 0;
        }}
        
        .content h4 {{
            font-size: 1.2rem;
            color: var(--secondary-color);
            margin: 1rem 0 0.5rem 0;
        }}
        
        .content p {{
            margin-bottom: 1rem;
            text-align: justify;
        }}
        
        .content ul {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        
        .content li {{
            margin-bottom: 0.5rem;
        }}
        
        .content pre {{
            background-color: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            overflow-x: auto;
            font-family: 'Fira Code', 'Monaco', 'Menlo', monospace;
        }}
        
        .content code {{
            background-color: var(--code-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Fira Code', 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
        }}
        
        .content strong {{
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        .content a {{
            color: var(--primary-color);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-bottom-color 0.2s;
        }}
        
        .content a:hover {{
            border-bottom-color: var(--primary-color);
        }}
        
        .meta-info {{
            background-color: var(--code-bg);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
            border-left: 4px solid var(--accent-color);
        }}
        
        .meta-info h3 {{
            color: var(--accent-color);
            margin-bottom: 1rem;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 2rem 0;
        }}
        
        .tag {{
            background-color: var(--primary-color);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
            text-decoration: none;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 2rem 0;
            border-top: 1px solid var(--border-color);
            color: var(--secondary-color);
        }}
        
        .footer a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .content h1 {{
                font-size: 1.8rem;
            }}
            
            .content h2 {{
                font-size: 1.5rem;
            }}
            
            .navigation {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
        </header>
        
        <nav class="navigation">
            <a href="index.html" class="nav-link">← 메인으로</a>
            <a href="https://github.com/Reasonofmoon/30-day-uv-python-challenge" class="nav-link">GitHub 소스코드</a>
            <a href="{next_page}" class="nav-link">다음 Day →</a>
        </nav>
        
        <main class="content">
            {content}
        </main>
        
        <div class="meta-info">
            <h3>프로젝트 정보</h3>
            <p><strong>기술 스택:</strong> {tech_stack}</p>
            <p><strong>개발 시간:</strong> {dev_time}분</p>
            <p><strong>테스트 커버리지:</strong> {coverage}%+</p>
            <p><strong>프로젝트 링크:</strong> <a href="{github_link}">GitHub에서 보기</a></p>
        </div>
        
        <div class="tags">
            {tags}
        </div>
        
        <footer class="footer">
            <p>30일 uv Python 마스터 챌린지 | 
            <a href="https://github.com/Reasonofmoon">Reasonofmoon</a> | 
            {date}</p>
            <p>Built with ❤️ and Python</p>
        </footer>
    </div>
</body>
</html>'''
    
    def publish_day_blog(self, day_number: int) -> bool:
        """Publish a specific day's blog to HTML"""
        try:
            day_key = f"day{day_number:02d}"
            
            # Get challenge info
            if day_key not in self.roadmap["challenges"]:
                print(f"Day {day_number} not found in roadmap")
                return False
            
            challenge = self.roadmap["challenges"][day_key]
            
            # Find blog markdown file
            project_name = f"day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}"
            
            # Handle special cases for existing projects
            if day_number == 2:
                project_name = "day02-web-scraper"
            elif day_number == 1:
                project_name = "day01-smart-calculator"
            
            blog_file = self.root_dir / project_name / "BLOG.md"
            
            if not blog_file.exists():
                print(f"Blog file not found: {blog_file}")
                return False
            
            # Read markdown content
            with open(blog_file, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            
            # Convert to HTML
            html_content = self.convert_markdown_to_html(markdown_content)
            
            # Generate tags
            tags = []
            for tech in challenge.get('tech_stack', []):
                tags.append(f'<span class="tag">#{tech}</span>')
            tags.extend([
                '<span class="tag">#Python</span>',
                '<span class="tag">#uv</span>',
                '<span class="tag">#30일챌린지</span>',
                '<span class="tag">#개발일기</span>'
            ])
            
            # Prepare template variables
            title = f"Day {day_number}: {challenge['name']}"
            subtitle = f"30일 uv Python 마스터 챌린지 - Day {day_number}/30"
            next_day = day_number + 1
            next_page = f"day{next_day:02d}.html" if next_day <= 30 else "index.html"
            
            # Fill template
            html_page = self.get_page_template().format(
                title=title,
                subtitle=subtitle,
                description=challenge['description'],
                filename=f"day{day_number:02d}.html",
                content=html_content,
                tech_stack=', '.join(challenge.get('tech_stack', [])),
                dev_time=challenge.get('estimated_time', 60),
                coverage=challenge.get('success_criteria', {}).get('min_coverage', 80),
                github_link=f"https://github.com/Reasonofmoon/30-day-uv-python-challenge/tree/main/{project_name}",
                tags=' '.join(tags),
                date=datetime.now().strftime('%Y년 %m월 %d일'),
                next_page=next_page
            )
            
            # Save HTML file
            output_file = self.docs_dir / f"day{day_number:02d}.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_page)
            
            print(f"Published: {output_file}")
            print(f"URL: https://reasonofmoon.github.io/30-day-uv-python-challenge/day{day_number:02d}.html")
            
            return True
            
        except Exception as e:
            print(f"Error publishing day {day_number}: {e}")
            return False
    
    def create_index_page(self) -> bool:
        """Create main index page with blog links"""
        try:
            # Get completed challenges
            completed_days = []
            for day_key, challenge in self.roadmap["challenges"].items():
                if challenge.get("status") == "completed":
                    day_num = int(day_key[3:])
                    completed_days.append((day_num, challenge))
            
            completed_days.sort(key=lambda x: x[0])
            
            # Create blog links
            blog_links = []
            for day_num, challenge in completed_days:
                blog_links.append(f'''
                <div class="blog-card">
                    <h3><a href="day{day_num:02d}.html">Day {day_num}: {challenge['name']}</a></h3>
                    <p>{challenge['description']}</p>
                    <div class="tech-stack">
                        {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in challenge.get('tech_stack', []))}
                    </div>
                </div>
                ''')
            
            index_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>30일 uv Python 마스터 챌린지 - 개발 블로그</title>
    <meta name="description" content="30일간의 Python 개발 여정을 기록한 블로그">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        /* Same CSS variables and base styles as blog pages */
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --accent-color: #f59e0b;
            --text-color: #1f2937;
            --bg-color: #ffffff;
            --code-bg: #f8fafc;
            --border-color: #e2e8f0;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Noto Sans KR', sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background-color: var(--bg-color);
        }}
        
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 3rem 0;
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            color: white;
            border-radius: 12px;
        }}
        
        .header h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .header p {{ font-size: 1.2rem; opacity: 0.9; }}
        
        .blog-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .blog-card {{
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .blog-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .blog-card h3 {{ margin-bottom: 1rem; }}
        .blog-card h3 a {{ color: var(--primary-color); text-decoration: none; }}
        .blog-card h3 a:hover {{ text-decoration: underline; }}
        
        .blog-card p {{ color: var(--secondary-color); margin-bottom: 1rem; }}
        
        .tech-stack {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
        .tech-tag {{
            background: var(--code-bg);
            color: var(--primary-color);
            padding: 0.3rem 0.6rem;
            border-radius: 15px;
            font-size: 0.8rem;
            border: 1px solid var(--border-color);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 3rem 0;
        }}
        
        .stat-card {{
            background: var(--code-bg);
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-number {{ font-size: 2rem; font-weight: bold; color: var(--primary-color); }}
        .stat-label {{ color: var(--secondary-color); }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🚀 30일 uv Python 챌린지</h1>
            <p>실무급 Python 애플리케이션을 하루 60분씩 30일간 개발하는 여정</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(completed_days)}</div>
                <div class="stat-label">완료된 챌린지</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(completed_days) * 60}</div>
                <div class="stat-label">개발 시간 (분)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(tech for _, challenge in completed_days for tech in challenge.get("tech_stack", [])))}</div>
                <div class="stat-label">학습한 기술</div>
            </div>
        </div>
        
        <div class="blog-grid">
            {''.join(blog_links)}
        </div>
        
        <footer style="text-align: center; margin-top: 3rem; padding: 2rem 0; border-top: 1px solid var(--border-color);">
            <p><a href="https://github.com/Reasonofmoon/30-day-uv-python-challenge">GitHub 소스코드</a> | 
            <a href="https://github.com/Reasonofmoon">Reasonofmoon</a></p>
        </footer>
    </div>
</body>
</html>'''
            
            # Save index page
            index_file = self.docs_dir / "index.html"
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(index_content)
            
            print(f"Created index page: {index_file}")
            return True
            
        except Exception as e:
            print(f"Error creating index page: {e}")
            return False


def main():
    """Main function for testing"""
    root_dir = Path(__file__).parent.parent
    publisher = HTMLPublisher(root_dir)
    
    # Publish Day 2 blog
    print("Publishing Day 2 blog...")
    success = publisher.publish_day_blog(2)
    
    if success:
        print("Creating index page...")
        publisher.create_index_page()
        print("\nPublishing complete!")
        print("Visit: https://reasonofmoon.github.io/30-day-uv-python-challenge/day02.html")
    else:
        print("Publishing failed!")


if __name__ == "__main__":
    main()