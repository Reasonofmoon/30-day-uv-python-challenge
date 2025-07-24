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
        
        .breadcrumb {{
            margin: 1rem 0 2rem 0;
            padding: 0.5rem;
            font-size: 0.9rem;
            color: var(--secondary-color);
        }}
        
        .breadcrumb a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
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
            <a href="{prev_page}" class="nav-link">← {prev_title}</a>
            <a href="index.html" class="nav-link">📚 전체 목록</a>
            <a href="https://github.com/Reasonofmoon/30-day-uv-python-challenge" class="nav-link">💻 GitHub</a>
            <a href="{next_page}" class="nav-link">{next_title} →</a>
        </nav>
        
        <div class="breadcrumb">
            <a href="index.html">홈</a> > 
            <a href="#week-{week_num}">Week {week_num}</a> > 
            <span>Day {day_num}</span>
        </div>
        
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
            
            # Prepare navigation variables
            title = f"Day {day_number}: {challenge['name']}"
            subtitle = f"30일 uv Python 마스터 챌린지 - Day {day_number}/30"
            
            # Previous page navigation
            prev_day = day_number - 1
            if prev_day >= 1:
                prev_page = f"day{prev_day:02d}.html"
                if prev_day in [1, 2]:  # Known completed days
                    prev_challenge = self.roadmap["challenges"][f"day{prev_day:02d}"]
                    prev_title = f"Day {prev_day}: {prev_challenge['name'][:20]}..."
                else:
                    prev_title = f"Day {prev_day}"
            else:
                prev_page = "index.html"
                prev_title = "메인으로"
            
            # Next page navigation  
            next_day = day_number + 1
            if next_day <= 30:
                next_page = f"day{next_day:02d}.html"
                if f"day{next_day:02d}" in self.roadmap["challenges"]:
                    next_challenge = self.roadmap["challenges"][f"day{next_day:02d}"]
                    next_title = f"Day {next_day}: {next_challenge['name'][:20]}..."
                else:
                    next_title = f"Day {next_day}"
            else:
                next_page = "index.html"
                next_title = "메인으로"
            
            # Week calculation
            week_num = ((day_number - 1) // 7) + 1
            
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
                prev_page=prev_page,
                prev_title=prev_title,
                next_page=next_page,
                next_title=next_title,
                week_num=week_num,
                day_num=day_number
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
        """Create main index page with week-based navigation"""
        try:
            # Get all challenges organized by week
            weeks = {}
            for day_key, challenge in self.roadmap["challenges"].items():
                day_num = int(day_key[3:])
                week_num = ((day_num - 1) // 7) + 1
                
                if week_num not in weeks:
                    week_key = f"week{week_num}"
                    if week_key in self.roadmap["weeks"]:
                        weeks[week_num] = {
                            'name': self.roadmap["weeks"][week_key]["name"],
                            'description': self.roadmap["weeks"][week_key]["description"],
                            'days': []
                        }
                    else:
                        # Fallback for weeks beyond the defined roadmap
                        weeks[week_num] = {
                            'name': f"Week {week_num}",
                            'description': f"Advanced challenges for week {week_num}",
                            'days': []
                        }
                
                status = challenge.get("status", "pending")
                weeks[week_num]['days'].append({
                    'day_num': day_num,
                    'challenge': challenge,
                    'status': status
                })
            
            # Sort days within each week
            for week in weeks.values():
                week['days'].sort(key=lambda x: x['day_num'])
            
            # Create week sections
            week_sections = []
            for week_num in sorted(weeks.keys()):
                week_info = weeks[week_num]
                
                # Create day cards for this week
                day_cards = []
                for day_info in week_info['days']:
                    day_num = day_info['day_num']
                    challenge = day_info['challenge']
                    status = day_info['status']
                    
                    status_emoji = {
                        'completed': '✅',
                        'in_progress': '🚧', 
                        'pending': '📋'
                    }.get(status, '📋')
                    
                    status_class = {
                        'completed': 'completed',
                        'in_progress': 'in-progress',
                        'pending': 'pending'
                    }.get(status, 'pending')
                    
                    if status == 'completed':
                        day_cards.append(f'''
                        <div class="day-card {status_class}">
                            <h4><a href="day{day_num:02d}.html">{status_emoji} Day {day_num}: {challenge['name']}</a></h4>
                            <p>{challenge['description']}</p>
                            <div class="tech-stack">
                                {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in challenge.get('tech_stack', []))}
                            </div>
                        </div>
                        ''')
                    else:
                        day_cards.append(f'''
                        <div class="day-card {status_class}">
                            <h4>{status_emoji} Day {day_num}: {challenge['name']}</h4>
                            <p>{challenge['description']}</p>
                            <div class="tech-stack">
                                {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in challenge.get('tech_stack', []))}
                            </div>
                        </div>
                        ''')
                
                week_sections.append(f'''
                <section class="week-section" id="week-{week_num}">
                    <h2>Week {week_num}: {week_info['name']}</h2>
                    <p class="week-description">{week_info['description']}</p>
                    <div class="day-grid">
                        {''.join(day_cards)}
                    </div>
                </section>
                ''')
            
            # Calculate stats
            completed_count = sum(1 for week in weeks.values() for day in week['days'] if day['status'] == 'completed')
            total_time = completed_count * 60
            all_techs = set()
            for week in weeks.values():
                for day in week['days']:
                    if day['status'] == 'completed':
                        all_techs.update(day['challenge'].get('tech_stack', []))
            
            index_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>30일 uv Python 마스터 챌린지 - 개발 블로그</title>
    <meta name="description" content="30일간의 Python 개발 여정을 기록한 블로그">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --accent-color: #f59e0b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
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
        
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
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
            border: 1px solid var(--border-color);
        }}
        
        .stat-number {{ font-size: 2rem; font-weight: bold; color: var(--primary-color); }}
        .stat-label {{ color: var(--secondary-color); }}
        
        .week-section {{
            margin: 3rem 0;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }}
        
        .week-section h2 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.8rem;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
        }}
        
        .week-description {{
            color: var(--secondary-color);
            margin-bottom: 2rem;
            font-style: italic;
        }}
        
        .day-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .day-card {{
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .day-card.completed {{
            background: linear-gradient(135deg, #ecfeff, #f0f9ff);
            border-color: var(--success-color);
        }}
        
        .day-card.in-progress {{
            background: linear-gradient(135deg, #fffbeb, #fef3c7);
            border-color: var(--warning-color);
        }}
        
        .day-card.pending {{
            background: #f9fafb;
            border-color: var(--border-color);
        }}
        
        .day-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .day-card h4 {{ margin-bottom: 0.5rem; }}
        .day-card h4 a {{ color: var(--primary-color); text-decoration: none; }}
        .day-card h4 a:hover {{ text-decoration: underline; }}
        
        .day-card p {{ color: var(--secondary-color); margin-bottom: 1rem; font-size: 0.9rem; }}
        
        .tech-stack {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
        .tech-tag {{
            background: var(--code-bg);
            color: var(--primary-color);
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
            border: 1px solid var(--border-color);
        }}
        
        .quick-nav {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }}
        
        .quick-nav a {{
            background: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: background-color 0.2s;
        }}
        
        .quick-nav a:hover {{
            background: var(--accent-color);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2rem; }}
            .day-grid {{ grid-template-columns: 1fr; }}
            .quick-nav {{ flex-direction: column; align-items: center; }}
        }}
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
                <div class="stat-number">{completed_count}</div>
                <div class="stat-label">완료된 챌린지</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_time}</div>
                <div class="stat-label">개발 시간 (분)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(all_techs)}</div>
                <div class="stat-label">학습한 기술</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(weeks)}</div>
                <div class="stat-label">진행 주차</div>
            </div>
        </div>
        
        <div class="quick-nav">
            <a href="#week-1">Week 1: Foundation</a>
            <a href="#week-2">Week 2: Web Apps</a>
            <a href="#week-3">Week 3: Data</a>
            <a href="#week-4">Week 4: Advanced</a>
            <a href="https://github.com/Reasonofmoon/30-day-uv-python-challenge">💻 GitHub</a>
        </div>
        
        {''.join(week_sections)}
        
        <footer style="text-align: center; margin-top: 3rem; padding: 2rem 0; border-top: 1px solid var(--border-color); color: var(--secondary-color);">
            <p><strong>30일 uv Python 마스터 챌린지</strong></p>
            <p><a href="https://github.com/Reasonofmoon/30-day-uv-python-challenge" style="color: var(--primary-color);">GitHub 소스코드</a> | 
            <a href="https://github.com/Reasonofmoon" style="color: var(--primary-color);">Reasonofmoon</a></p>
            <p style="margin-top: 1rem; font-size: 0.9rem;">Built with ❤️ and Python | {datetime.now().strftime('%Y년 %m월')}</p>
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
    """Main function - republish all completed days with updated navigation"""
    root_dir = Path(__file__).parent.parent
    publisher = HTMLPublisher(root_dir)
    
    # Find all completed days
    completed_days = []
    for day_key, challenge in publisher.roadmap["challenges"].items():
        if challenge.get("status") == "completed":
            day_num = int(day_key[3:])
            completed_days.append(day_num)
    
    completed_days.sort()
    
    print(f"Republishing {len(completed_days)} completed days with updated navigation...")
    
    # Republish all completed days
    for day_num in completed_days:
        print(f"Publishing Day {day_num}...")
        success = publisher.publish_day_blog(day_num)
        if not success:
            print(f"Failed to publish Day {day_num}")
    
    print("Creating comprehensive index page...")
    publisher.create_index_page()
    
    print("\nPublishing complete!")
    print("Pages available:")
    print(f"   - Main Index: https://reasonofmoon.github.io/30-day-uv-python-challenge/docs/index.html")
    for day_num in completed_days:
        print(f"   - Day {day_num}: https://reasonofmoon.github.io/30-day-uv-python-challenge/docs/day{day_num:02d}.html")
    
    print(f"\nNavigation features:")
    print(f"   - Day 1 -> Day 2 link connection")
    print(f"   - Day 2 -> Day 3 link connection") 
    print(f"   - Full Week-based organization")
    print(f"   - 30-day complete roadmap display")


if __name__ == "__main__":
    main()