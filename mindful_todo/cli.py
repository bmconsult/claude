#!/usr/bin/env python3
"""
Mindful Todo CLI - Beautiful, intuitive command-line interface
"""

import sys
import argparse
from datetime import datetime, timedelta
from typing import Optional, List

from todo import TodoList, Task, Priority, Energy


class Colors:
    """ANSI color codes for beautiful terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright variants
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'

    # Background colors
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


def colorize(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text"""
    prefix = Colors.BOLD if bold else ''
    return f"{prefix}{color}{text}{Colors.RESET}"


def print_header(text: str):
    """Print a styled header"""
    print()
    print(colorize("═" * 60, Colors.CYAN))
    print(colorize(f"  {text}", Colors.CYAN, bold=True))
    print(colorize("═" * 60, Colors.CYAN))
    print()


def print_task(task: Task, show_id: bool = True):
    """Print a single task with beautiful formatting"""
    # Task ID and checkbox
    checkbox = colorize("✓", Colors.GREEN, bold=True) if task.is_completed else colorize("☐", Colors.BLUE)
    task_id = colorize(f"[{task.task_id}]", Colors.DIM) if show_id else ""

    # Title with completion styling
    title = task.title
    if task.is_completed:
        title = colorize(title, Colors.DIM)
    elif task.is_overdue():
        title = colorize(title, Colors.BRIGHT_RED, bold=True)
    elif task.is_due_soon():
        title = colorize(title, Colors.BRIGHT_YELLOW, bold=True)

    # Priority indicator
    priority_colors = {
        Priority.URGENT_IMPORTANT: Colors.BRIGHT_RED,
        Priority.IMPORTANT: Colors.BRIGHT_YELLOW,
        Priority.URGENT: Colors.YELLOW,
        Priority.NORMAL: Colors.WHITE,
        Priority.SOMEDAY: Colors.DIM
    }
    priority = colorize(task.priority.value, priority_colors.get(task.priority, Colors.WHITE))

    # Energy indicator
    energy = colorize(task.energy.value, Colors.CYAN)

    # Build the line
    line = f"  {checkbox} {task_id} {title}"
    print(line)

    # Details on second line
    details = []
    details.append(priority)
    details.append(energy)

    if task.project and task.project != "inbox":
        details.append(colorize(f"📁 {task.project}", Colors.BLUE))

    if task.estimated_minutes:
        hours = task.estimated_minutes // 60
        minutes = task.estimated_minutes % 60
        time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        details.append(colorize(f"⏱️  {time_str}", Colors.MAGENTA))

    if task.due_date:
        due = datetime.fromisoformat(task.due_date)
        due_str = due.strftime("%b %d")
        if task.is_overdue():
            details.append(colorize(f"⚠️  Overdue: {due_str}", Colors.BRIGHT_RED))
        elif task.is_due_soon():
            details.append(colorize(f"🔔 Due: {due_str}", Colors.BRIGHT_YELLOW))
        else:
            details.append(colorize(f"📅 Due: {due_str}", Colors.WHITE))

    if task.notes:
        details.append(colorize(f"💭 Note", Colors.DIM))

    if details:
        print("    " + "  •  ".join(details))

    if task.notes and not task.is_completed:
        print(colorize(f"    └─ {task.notes}", Colors.DIM))

    print()


def print_motivation(todo_list: TodoList):
    """Print motivational message"""
    msg = todo_list.get_motivation_message()
    print(colorize(f"  {msg}", Colors.BRIGHT_GREEN, bold=True))
    print()


def print_stats(todo_list: TodoList):
    """Print productivity statistics"""
    stats = todo_list.stats
    active_count = len(todo_list.get_active_tasks())

    print(colorize("📊 Your Progress", Colors.CYAN, bold=True))
    print(f"  Today: {colorize(str(stats['completed_today']), Colors.GREEN, bold=True)} completed")
    print(f"  This week: {colorize(str(stats['completed_this_week']), Colors.GREEN, bold=True)} completed")
    print(f"  Total: {colorize(str(stats['total_completed']), Colors.GREEN, bold=True)} completed")
    print(f"  Active tasks: {colorize(str(active_count), Colors.YELLOW, bold=True)}")
    print()


def cmd_add(todo_list: TodoList, args):
    """Add a new task"""
    # Parse priority
    priority_map = {
        'ui': Priority.URGENT_IMPORTANT,
        'urgent-important': Priority.URGENT_IMPORTANT,
        'i': Priority.IMPORTANT,
        'important': Priority.IMPORTANT,
        'u': Priority.URGENT,
        'urgent': Priority.URGENT,
        'n': Priority.NORMAL,
        'normal': Priority.NORMAL,
        's': Priority.SOMEDAY,
        'someday': Priority.SOMEDAY
    }
    priority = priority_map.get(args.priority.lower(), Priority.NORMAL)

    # Parse energy
    energy_map = {
        'h': Energy.HIGH,
        'high': Energy.HIGH,
        'm': Energy.MEDIUM,
        'medium': Energy.MEDIUM,
        'l': Energy.LOW,
        'low': Energy.LOW,
        'q': Energy.QUICK,
        'quick': Energy.QUICK
    }
    energy = energy_map.get(args.energy.lower(), Energy.MEDIUM)

    # Parse due date
    due_date = None
    if args.due:
        if args.due.lower() == 'today':
            due_date = datetime.now().replace(hour=23, minute=59).isoformat()
        elif args.due.lower() == 'tomorrow':
            due_date = (datetime.now() + timedelta(days=1)).replace(hour=23, minute=59).isoformat()
        else:
            try:
                due_date = datetime.strptime(args.due, '%Y-%m-%d').isoformat()
            except ValueError:
                print(colorize("❌ Invalid date format. Use YYYY-MM-DD, 'today', or 'tomorrow'", Colors.RED))
                return

    task = Task(
        title=args.title,
        priority=priority,
        energy=energy,
        project=args.project,
        notes=args.notes or "",
        due_date=due_date,
        estimated_minutes=args.time
    )

    added = todo_list.add_task(task)
    print(colorize(f"✨ Task added successfully!", Colors.GREEN, bold=True))
    print_task(added)


def cmd_list(todo_list: TodoList, args):
    """List tasks with various filters"""
    print_header("Your Tasks")

    if args.project:
        tasks = todo_list.get_tasks_by_project(args.project)
        print(colorize(f"  📁 Project: {args.project}", Colors.BLUE, bold=True))
        print()
    elif args.energy:
        energy_map = {
            'high': Energy.HIGH,
            'medium': Energy.MEDIUM,
            'low': Energy.LOW,
            'quick': Energy.QUICK
        }
        energy = energy_map.get(args.energy.lower())
        tasks = todo_list.get_tasks_by_energy(energy)
        print(colorize(f"  ⚡ Energy level: {energy.value}", Colors.CYAN, bold=True))
        print()
    else:
        tasks = todo_list.get_active_tasks()

    if not tasks:
        print(colorize("  🎉 No tasks! You're all caught up!", Colors.GREEN, bold=True))
        print()
        return

    for task in tasks:
        print_task(task)

    print(colorize(f"  Total: {len(tasks)} tasks", Colors.DIM))
    print()


def cmd_focus(todo_list: TodoList, args):
    """Show daily focus tasks"""
    print_header("🎯 Your Daily Focus")
    print_motivation(todo_list)

    focus_tasks = todo_list.get_daily_focus(3)

    if not focus_tasks:
        print(colorize("  🎉 No urgent tasks! Great job staying on top of things!", Colors.GREEN, bold=True))
        print()
        return

    print(colorize("  These are your top 3 priorities today:", Colors.CYAN))
    print(colorize("  Focus on completing these before moving to other tasks.", Colors.DIM))
    print()

    for i, task in enumerate(focus_tasks, 1):
        print(colorize(f"  Priority #{i}", Colors.YELLOW, bold=True))
        print_task(task, show_id=True)

    # Show quick wins for momentum
    quick_wins = todo_list.get_quick_wins()
    if quick_wins:
        print(colorize("  ⚡ Quick Wins (< 5 minutes)", Colors.CYAN, bold=True))
        print(colorize("  Start with these to build momentum!", Colors.DIM))
        print()
        for task in quick_wins[:3]:
            print_task(task)


def cmd_done(todo_list: TodoList, args):
    """Complete a task with celebration"""
    task = todo_list.complete_task(args.id)

    if task:
        print()
        print(colorize("  🎉 " + "✨" * 20, Colors.GREEN, bold=True))
        print(colorize(f"  🎊 Congratulations! Task completed!", Colors.GREEN, bold=True))
        print(colorize("  🎉 " + "✨" * 20, Colors.GREEN, bold=True))
        print()
        print(colorize(f"  ✓ {task.title}", Colors.GREEN, bold=True))
        print()
        print_motivation(todo_list)
    else:
        print(colorize(f"  ❌ Task {args.id} not found", Colors.RED))


def cmd_delete(todo_list: TodoList, args):
    """Delete a task"""
    task = todo_list.get_task(args.id)
    if task:
        if todo_list.delete_task(args.id):
            print(colorize(f"  🗑️  Deleted: {task.title}", Colors.YELLOW))
        else:
            print(colorize(f"  ❌ Error deleting task", Colors.RED))
    else:
        print(colorize(f"  ❌ Task {args.id} not found", Colors.RED))


def cmd_break(todo_list: TodoList, args):
    """Break down a large task"""
    task = todo_list.get_task(args.id)
    if not task:
        print(colorize(f"  ❌ Task {args.id} not found", Colors.RED))
        return

    print(colorize(f"  🔨 Breaking down: {task.title}", Colors.CYAN, bold=True))
    print()
    print(colorize("  Enter subtasks (one per line, empty line to finish):", Colors.YELLOW))

    subtasks = []
    while True:
        try:
            line = input(colorize("    → ", Colors.CYAN))
            if not line.strip():
                break
            subtasks.append(line.strip())
        except (EOFError, KeyboardInterrupt):
            break

    if subtasks:
        created = todo_list.break_down_task(args.id, subtasks)
        print()
        print(colorize(f"  ✨ Created {len(created)} subtasks!", Colors.GREEN, bold=True))
        print()
        for subtask in created:
            print_task(subtask)
    else:
        print(colorize("  ❌ No subtasks entered", Colors.RED))


def cmd_projects(todo_list: TodoList, args):
    """List all projects"""
    print_header("📁 Your Projects")

    projects = todo_list.get_projects()

    if not projects:
        print(colorize("  No projects yet. Add tasks with --project to organize them!", Colors.YELLOW))
        return

    for project in projects:
        tasks = todo_list.get_tasks_by_project(project)
        completed = len([t for t in tasks if t.is_completed])
        total = len(tasks)

        print(colorize(f"  📁 {project}", Colors.BLUE, bold=True))
        print(f"     {completed}/{total} completed")
        print()


def cmd_stats(todo_list: TodoList, args):
    """Show statistics"""
    print_header("📊 Your Productivity Stats")
    print_stats(todo_list)
    print_motivation(todo_list)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Mindful Todo - A psychologically helpful task manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  todo add "Write project proposal" -p work -e high -d tomorrow
  todo add "Call mom" -e quick -P urgent-important
  todo focus                    # Show today's top 3 priorities
  todo list                     # List all tasks
  todo list -P work            # List tasks in 'work' project
  todo done 5                   # Complete task #5
  todo break 3                  # Break task #3 into subtasks
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('-p', '--project', default='inbox', help='Project name (default: inbox)')
    add_parser.add_argument('-P', '--priority', default='normal',
                            help='Priority: ui/i/u/n/s (urgent-important/important/urgent/normal/someday)')
    add_parser.add_argument('-e', '--energy', default='medium',
                            help='Energy: h/m/l/q (high/medium/low/quick)')
    add_parser.add_argument('-d', '--due', help='Due date: YYYY-MM-DD, today, or tomorrow')
    add_parser.add_argument('-t', '--time', type=int, default=30, help='Estimated minutes (default: 30)')
    add_parser.add_argument('-n', '--notes', help='Additional notes')

    # List command
    list_parser = subparsers.add_parser('list', help='List tasks', aliases=['ls'])
    list_parser.add_argument('-P', '--project', help='Filter by project')
    list_parser.add_argument('-e', '--energy', help='Filter by energy: high/medium/low/quick')

    # Focus command
    focus_parser = subparsers.add_parser('focus', help='Show daily focus tasks')

    # Done command
    done_parser = subparsers.add_parser('done', help='Complete a task', aliases=['complete', 'finish'])
    done_parser.add_argument('id', type=int, help='Task ID')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task', aliases=['rm'])
    delete_parser.add_argument('id', type=int, help='Task ID')

    # Break command
    break_parser = subparsers.add_parser('break', help='Break a task into subtasks')
    break_parser.add_argument('id', type=int, help='Task ID to break down')

    # Projects command
    projects_parser = subparsers.add_parser('projects', help='List all projects')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show productivity statistics')

    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments, show focus by default
        args = parser.parse_args(['focus'])
    else:
        args = parser.parse_args()

    # Initialize todo list
    todo_list = TodoList()

    # Execute command
    commands = {
        'add': cmd_add,
        'list': cmd_list,
        'ls': cmd_list,
        'focus': cmd_focus,
        'done': cmd_done,
        'complete': cmd_done,
        'finish': cmd_done,
        'delete': cmd_delete,
        'rm': cmd_delete,
        'break': cmd_break,
        'projects': cmd_projects,
        'stats': cmd_stats
    }

    if args.command in commands:
        try:
            commands[args.command](todo_list, args)
        except KeyboardInterrupt:
            print()
            print(colorize("  👋 Goodbye! Keep being awesome!", Colors.CYAN))
            print()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
