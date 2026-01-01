#!/usr/bin/env python3
"""
Course Recommendation System
Author: Pranay M.

Tool that suggests courses based on student interests and career goals.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║               📚 COURSE RECOMMENDATION SYSTEM 📚                               ║
║                    Personalized Academic Path Planning                         ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Interest-Based Recommender", "interest", "Get courses by interests"),
    "2": ("Career Path Advisor", "career", "Plan career-aligned courses"),
    "3": ("Skill Gap Analyzer", "skills", "Identify skill gaps to fill"),
    "4": ("Prerequisite Mapper", "prereq", "Map course prerequisites"),
    "5": ("Course Load Balancer", "load", "Balance semester workload"),
    "6": ("Elective Explorer", "electives", "Explore elective options"),
    "7": ("Minor/Concentration Planner", "minor", "Plan minors or concentrations"),
    "8": ("Schedule Optimizer", "schedule", "Optimize course schedules"),
    "9": ("Graduation Path Planner", "graduation", "Plan path to graduation"),
    "10": ("Recommendation Summary", "summary", "Get complete recommendations")
}

SYSTEM_PROMPTS = {
    "interest": """You are an expert academic advisor helping students find courses.

For interest-based recommendations:

1. **Interest Analysis**: Understand stated interests
2. **Course Suggestions**: Relevant courses for those interests
3. **Cross-Disciplinary**: Courses from multiple departments
4. **Beginner to Advanced**: Options at different levels
5. **Hidden Gems**: Less obvious but relevant courses
6. **Why Each Fits**: Explain relevance to interests

Help students discover courses they'll enjoy.""",

    "career": """You are an expert career and academic advisor.

For career path advising:

1. **Career Goal Analysis**: Understand target career
2. **Required Skills**: Skills needed for that career
3. **Essential Courses**: Must-take courses
4. **Recommended Courses**: Helpful additional courses
5. **Industry Alignment**: What employers look for
6. **Timeline**: When to take each course

Align course selection with career goals.""",

    "skills": """You are an expert in skills assessment and development.

For skill gap analysis:

1. **Current Skills**: Assess existing skills
2. **Target Skills**: Skills needed for goals
3. **Gap Identification**: Missing skills
4. **Course Mapping**: Courses that build each skill
5. **Priority Order**: Most important gaps first
6. **Alternative Learning**: Non-course options

Identify and address skill gaps through coursework.""",

    "prereq": """You are an expert in curriculum planning and prerequisites.

For prerequisite mapping:

1. **Course Chain**: Prerequisite sequences
2. **Foundation Courses**: Starting points
3. **Intermediate Courses**: Bridge courses
4. **Advanced Courses**: End goals
5. **Flexible Paths**: Alternative routes
6. **Time Planning**: Semester-by-semester plan

Map prerequisite relationships for course planning.""",

    "load": """You are an expert in academic workload management.

For course load balancing:

1. **Difficulty Assessment**: Course difficulty levels
2. **Time Requirements**: Expected weekly hours
3. **Balance Strategy**: Mix hard and easier courses
4. **Semester Planning**: Balanced semester loads
5. **Stress Points**: Identify heavy periods
6. **Recommendations**: Optimal combinations

Help balance course workload across semesters.""",

    "electives": """You are an expert academic advisor for elective exploration.

For elective exploration:

1. **Available Categories**: Types of electives
2. **Interest Matching**: Electives matching interests
3. **Skill Building**: Electives that add value
4. **Easy A Options**: Less demanding options
5. **Unique Experiences**: Special topics courses
6. **Strategic Choices**: Electives that complement major

Help explore and select elective courses.""",

    "minor": """You are an expert in minor and concentration planning.

For minor/concentration planning:

1. **Options Available**: Possible minors/concentrations
2. **Alignment**: Which complement the major
3. **Requirements**: Courses needed for each
4. **Overlap**: Courses counting for both
5. **Career Value**: Which add career value
6. **Feasibility**: Can it fit in the plan?

Help plan minors and concentrations.""",

    "schedule": """You are an expert in course schedule optimization.

For schedule optimization:

1. **Time Preferences**: When student learns best
2. **Conflict Resolution**: Avoiding time conflicts
3. **Buffer Time**: Breaks between classes
4. **Efficiency**: Minimizing campus travel
5. **Study Time**: Building in study periods
6. **Optimal Schedule**: Best weekly arrangement

Optimize weekly course schedules.""",

    "graduation": """You are an expert in graduation planning.

For graduation path planning:

1. **Requirements Audit**: What's still needed
2. **Remaining Semesters**: How many left
3. **Course Sequencing**: Order to take courses
4. **Bottlenecks**: Courses that could delay graduation
5. **Alternative Paths**: Different ways to complete
6. **Timeline**: Semester-by-semester plan

Plan the path to graduation.""",

    "summary": """You are an expert academic advisor providing comprehensive guidance.

For a complete recommendation summary:

1. **Student Profile**: Summarize interests/goals
2. **Immediate Recommendations**: Next semester courses
3. **Long-term Plan**: Multi-semester roadmap
4. **Career Alignment**: How plan serves career
5. **Flexibility Options**: Alternative choices
6. **Action Items**: Specific next steps

Provide comprehensive course recommendation summary."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="📚 Recommendation Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"📚 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} needs:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"📚 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Course Recommendation System![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
