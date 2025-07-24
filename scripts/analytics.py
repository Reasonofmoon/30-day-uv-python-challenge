#!/usr/bin/env python3
"""
Analytics and Progress Tracking for 30-Day Challenge

Track progress, generate metrics, and create visual reports.
"""

import json
import os
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ChallengeAnalytics:
    """Analytics and progress tracking"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.config_dir = root_dir / "config"
        
        # Load roadmap
        with open(self.config_dir / "challenge_roadmap.json", "r", encoding="utf-8") as f:
            self.roadmap = json.load(f)
    
    def get_overall_progress(self) -> Dict:
        """Get overall challenge progress"""
        challenges = self.roadmap["challenges"]
        
        total_challenges = len(challenges)
        completed = sum(1 for c in challenges.values() if c.get("status") == "completed")
        in_progress = sum(1 for c in challenges.values() if c.get("status") == "in_progress")
        pending = total_challenges - completed - in_progress
        
        # Calculate by week
        week_progress = {}
        for week_name, week_info in self.roadmap["weeks"].items():
            week_completed = 0
            week_total = len(week_info["days"])
            
            for day in week_info["days"]:
                day_key = f"day{day:02d}"
                if challenges.get(day_key, {}).get("status") == "completed":
                    week_completed += 1
            
            week_progress[week_name] = {
                "completed": week_completed,
                "total": week_total,
                "percentage": (week_completed / week_total) * 100
            }
        
        return {
            "total_challenges": total_challenges,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_percentage": (completed / total_challenges) * 100,
            "week_progress": week_progress
        }
    
    def get_technology_stats(self) -> Dict:
        """Get statistics by technology used"""
        tech_count = defaultdict(int)
        tech_completed = defaultdict(int)
        
        for challenge in self.roadmap["challenges"].values():
            for tech in challenge.get("tech_stack", []):
                tech_count[tech] += 1
                if challenge.get("status") == "completed":
                    tech_completed[tech] += 1
        
        tech_stats = {}
        for tech in tech_count:
            tech_stats[tech] = {
                "total_projects": tech_count[tech],
                "completed_projects": tech_completed[tech],
                "completion_rate": (tech_completed[tech] / tech_count[tech]) * 100 if tech_count[tech] > 0 else 0
            }
        
        return dict(sorted(tech_stats.items(), key=lambda x: x[1]["total_projects"], reverse=True))
    
    def get_project_type_stats(self) -> Dict:
        """Get statistics by project type"""
        type_count = defaultdict(int)
        type_completed = defaultdict(int)
        
        for challenge in self.roadmap["challenges"].values():
            proj_type = challenge.get("type", "cli-app")
            type_count[proj_type] += 1
            if challenge.get("status") == "completed":
                type_completed[proj_type] += 1
        
        type_stats = {}
        for proj_type in type_count:
            type_stats[proj_type] = {
                "total_projects": type_count[proj_type],
                "completed_projects": type_completed[proj_type],
                "completion_rate": (type_completed[proj_type] / type_count[proj_type]) * 100 if type_count[proj_type] > 0 else 0
            }
        
        return type_stats
    
    def get_code_metrics(self) -> Dict:
        """Get code metrics for completed projects"""
        metrics = {
            "total_files": 0,
            "total_lines": 0,
            "test_files": 0,
            "test_lines": 0,
            "projects_analyzed": 0
        }
        
        project_metrics = {}
        
        for day_key, challenge in self.roadmap["challenges"].items():
            if challenge.get("status") != "completed":
                continue
            
            project_name = f"{day_key}-{challenge['name'].lower().replace(' ', '-')}"
            project_path = self.root_dir / project_name
            
            if not project_path.exists():
                continue
            
            try:
                project_stats = self._analyze_project_code(project_path)
                project_metrics[project_name] = project_stats
                
                metrics["total_files"] += project_stats["source_files"]
                metrics["total_lines"] += project_stats["source_lines"]
                metrics["test_files"] += project_stats["test_files"] 
                metrics["test_lines"] += project_stats["test_lines"]
                metrics["projects_analyzed"] += 1
                
            except Exception as e:
                print(f"Error analyzing {project_name}: {e}")
        
        metrics["avg_lines_per_project"] = metrics["total_lines"] / max(1, metrics["projects_analyzed"])
        metrics["test_ratio"] = (metrics["test_lines"] / max(1, metrics["total_lines"])) * 100
        metrics["project_details"] = project_metrics
        
        return metrics
    
    def _analyze_project_code(self, project_path: Path) -> Dict:
        """Analyze code metrics for a single project"""
        stats = {
            "source_files": 0,
            "source_lines": 0,
            "test_files": 0,
            "test_lines": 0,
            "avg_complexity": 0
        }
        
        # Count source files
        src_dir = project_path / "src"
        if src_dir.exists():
            for py_file in src_dir.rglob("*.py"):
                if py_file.name != "__init__.py":
                    stats["source_files"] += 1
                    stats["source_lines"] += self._count_lines(py_file)
        
        # Count test files
        test_dir = project_path / "tests"
        if test_dir.exists():
            for py_file in test_dir.rglob("*.py"):
                if py_file.name != "__init__.py":
                    stats["test_files"] += 1
                    stats["test_lines"] += self._count_lines(py_file)
        
        return stats
    
    def _count_lines(self, file_path: Path) -> int:
        """Count non-empty lines in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len([line for line in f if line.strip()])
        except:
            return 0
    
    def get_test_coverage_stats(self) -> Dict:
        """Get test coverage statistics for completed projects"""
        coverage_stats = {
            "projects_with_coverage": 0,
            "average_coverage": 0,
            "coverage_details": {}
        }
        
        total_coverage = 0
        projects_with_data = 0
        
        for day_key, challenge in self.roadmap["challenges"].items():
            if challenge.get("status") != "completed":
                continue
            
            project_name = f"{day_key}-{challenge['name'].lower().replace(' ', '-')}"
            project_path = self.root_dir / project_name
            
            if not project_path.exists():
                continue
            
            try:
                # Try to get coverage data
                os.chdir(project_path)
                result = subprocess.run(
                    ["uv", "run", "pytest", "tests/", "--cov=src", "--cov-report=json", "--quiet"],
                    capture_output=True, text=True, timeout=30
                )
                
                if result.returncode == 0:
                    # Look for coverage.json
                    coverage_file = project_path / "coverage.json"
                    if coverage_file.exists():
                        with open(coverage_file, 'r') as f:
                            cov_data = json.load(f)
                            coverage_percent = cov_data.get("totals", {}).get("percent_covered", 0)
                            
                            coverage_stats["coverage_details"][project_name] = {
                                "coverage": coverage_percent,
                                "target": challenge.get("success_criteria", {}).get("min_coverage", 80),
                                "meets_target": coverage_percent >= challenge.get("success_criteria", {}).get("min_coverage", 80)
                            }
                            
                            total_coverage += coverage_percent
                            projects_with_data += 1
                
            except Exception as e:
                print(f"Error getting coverage for {project_name}: {e}")
        
        if projects_with_data > 0:
            coverage_stats["average_coverage"] = total_coverage / projects_with_data
            coverage_stats["projects_with_coverage"] = projects_with_data
        
        return coverage_stats
    
    def get_time_analysis(self) -> Dict:
        """Analyze time spent on challenges"""
        time_stats = {
            "total_estimated_time": 0,
            "completed_time": 0,
            "average_time_per_challenge": 0,
            "time_by_type": defaultdict(int),
            "time_by_week": defaultdict(int)
        }
        
        completed_challenges = 0
        
        for day_key, challenge in self.roadmap["challenges"].items():
            estimated_time = challenge.get("estimated_time", 60)
            time_stats["total_estimated_time"] += estimated_time
            
            if challenge.get("status") == "completed":
                time_stats["completed_time"] += estimated_time
                completed_challenges += 1
                
                # Time by type
                proj_type = challenge.get("type", "cli-app")
                time_stats["time_by_type"][proj_type] += estimated_time
                
                # Time by week
                day_num = int(day_key[3:])
                week_num = ((day_num - 1) // 7) + 1
                time_stats["time_by_week"][f"week_{week_num}"] += estimated_time
        
        if completed_challenges > 0:
            time_stats["average_time_per_challenge"] = time_stats["completed_time"] / completed_challenges
        
        return dict(time_stats)
    
    def generate_progress_report(self, output_file: Optional[Path] = None) -> str:
        """Generate comprehensive progress report"""
        
        # Collect all metrics
        progress = self.get_overall_progress()
        tech_stats = self.get_technology_stats()
        type_stats = self.get_project_type_stats()
        code_metrics = self.get_code_metrics()
        coverage_stats = self.get_test_coverage_stats()
        time_analysis = self.get_time_analysis()
        
        # Generate report
        report = f"""
# 30-Day uv Python Challenge - Progress Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Progress

- **Total Challenges**: {progress['total_challenges']}
- **Completed**: {progress['completed']} ({progress['completion_percentage']:.1f}%)
- **In Progress**: {progress['in_progress']}
- **Pending**: {progress['pending']}

### Week-by-Week Progress

{chr(10).join(f"- **{week.replace('_', ' ').title()}**: {info['completed']}/{info['total']} ({info['percentage']:.1f}%)" for week, info in progress['week_progress'].items())}

## Technology Statistics

Top technologies by project count:

{chr(10).join(f"- **{tech}**: {stats['completed_projects']}/{stats['total_projects']} projects ({stats['completion_rate']:.1f}%)" for tech, stats in list(tech_stats.items())[:10])}

## 🎯 Project Type Distribution

{chr(10).join(f"- **{ptype.replace('-', ' ').title()}**: {stats['completed_projects']}/{stats['total_projects']} projects ({stats['completion_rate']:.1f}%)" for ptype, stats in type_stats.items())}

## 📈 Code Metrics

- **Projects Analyzed**: {code_metrics['projects_analyzed']}
- **Total Source Files**: {code_metrics['total_files']}
- **Total Lines of Code**: {code_metrics['total_lines']:,}
- **Test Files**: {code_metrics['test_files']}
- **Test Lines**: {code_metrics['test_lines']:,}
- **Average Lines per Project**: {code_metrics['avg_lines_per_project']:.0f}
- **Test-to-Code Ratio**: {code_metrics['test_ratio']:.1f}%

## 🧪 Test Coverage

- **Projects with Coverage Data**: {coverage_stats['projects_with_coverage']}
- **Average Coverage**: {coverage_stats['average_coverage']:.1f}%

### Coverage Details

{chr(10).join(f"- **{proj}**: {details['coverage']:.1f}% {'✅' if details['meets_target'] else '❌'} (target: {details['target']}%)" for proj, details in coverage_stats.get('coverage_details', {}).items())}

## ⏰ Time Analysis

- **Total Estimated Time**: {time_analysis['total_estimated_time']} minutes ({time_analysis['total_estimated_time']/60:.1f} hours)
- **Completed Time**: {time_analysis['completed_time']} minutes ({time_analysis['completed_time']/60:.1f} hours)
- **Average per Challenge**: {time_analysis['average_time_per_challenge']:.0f} minutes

### Time by Project Type

{chr(10).join(f"- **{ptype.replace('-', ' ').title()}**: {time} minutes ({time/60:.1f} hours)" for ptype, time in time_analysis['time_by_type'].items())}

### Time by Week

{chr(10).join(f"- **{week.replace('_', ' ').title()}**: {time} minutes ({time/60:.1f} hours)" for week, time in time_analysis['time_by_week'].items())}

## 🎯 Key Achievements

- Successfully completed {progress['completed']} out of {progress['total_challenges']} challenges
- Wrote {code_metrics['total_lines']:,} lines of production code
- Maintained {code_metrics['test_lines']:,} lines of test code
- Achieved average test coverage of {coverage_stats['average_coverage']:.1f}%
- Learned {len(tech_stats)} different technologies
- Built {len(type_stats)} different types of applications

## 📚 Learning Outcomes

### Technologies Mastered
{chr(10).join(f"- {tech} ({stats['completed_projects']} projects)" for tech, stats in tech_stats.items() if stats['completed_projects'] > 0)}

### Project Types Completed
{chr(10).join(f"- {ptype.replace('-', ' ').title()} ({stats['completed_projects']} projects)" for ptype, stats in type_stats.items() if stats['completed_projects'] > 0)}

## 🔥 Next Steps

{"Congratulations on completing the 30-day challenge! 🎉" if progress['completed'] == progress['total_challenges'] else f"Keep going! {progress['pending']} challenges remaining."}

---

*Report generated by Challenge Analytics System*
*Part of the 30-day uv Python mastery challenge*
"""
        
        if output_file:
            output_file.write_text(report, encoding='utf-8')
            print(f"Report saved to {output_file}")
        
        return report
    
    def update_challenge_status(self, day_number: int, status: str) -> bool:
        """Update challenge status in roadmap"""
        try:
            day_key = f"day{day_number:02d}"
            if day_key in self.roadmap["challenges"]:
                self.roadmap["challenges"][day_key]["status"] = status
                
                # Save updated roadmap
                with open(self.config_dir / "challenge_roadmap.json", "w", encoding="utf-8") as f:
                    json.dump(self.roadmap, f, indent=2, ensure_ascii=False)
                
                return True
            return False
        except Exception as e:
            print(f"Error updating status: {e}")
            return False


def main():
    """Generate analytics report"""
    root_dir = Path(__file__).parent.parent
    analytics = ChallengeAnalytics(root_dir)
    
    # Generate and display report
    report = analytics.generate_progress_report()
    print(report)
    
    # Save report
    report_file = root_dir / f"progress_report_{datetime.now().strftime('%Y%m%d')}.md"
    analytics.generate_progress_report(report_file)


if __name__ == "__main__":
    main()