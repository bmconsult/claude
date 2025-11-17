#!/usr/bin/env python3
"""
Mindful Todo - A psychologically-informed task management app

Design principles:
- Reduce cognitive load
- Celebrate small wins
- Break down overwhelming tasks
- Focus on daily intentions
- Energy-aware prioritization
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from enum import Enum


class Priority(Enum):
    """Task priorities based on importance and urgency"""
    URGENT_IMPORTANT = "🔥 Urgent & Important"
    IMPORTANT = "⭐ Important"
    URGENT = "⚡ Urgent"
    NORMAL = "📌 Normal"
    SOMEDAY = "💭 Someday/Maybe"


class Energy(Enum):
    """Energy level required for task"""
    HIGH = "🧠 High Focus"
    MEDIUM = "⚡ Medium Energy"
    LOW = "🌊 Low Energy"
    QUICK = "⚡ Quick (< 5 min)"


class Task:
    """A single task with psychological metadata"""

    def __init__(
        self,
        title: str,
        task_id: Optional[int] = None,
        priority: Priority = Priority.NORMAL,
        energy: Energy = Energy.MEDIUM,
        project: str = "inbox",
        notes: str = "",
        due_date: Optional[str] = None,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        estimated_minutes: int = 30,
        is_completed: bool = False,
        parent_id: Optional[int] = None,
        tags: Optional[List[str]] = None
    ):
        self.task_id = task_id
        self.title = title
        self.priority = priority if isinstance(priority, Priority) else Priority[priority]
        self.energy = energy if isinstance(energy, Energy) else Energy[energy]
        self.project = project
        self.notes = notes
        self.due_date = due_date
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.estimated_minutes = estimated_minutes
        self.is_completed = is_completed
        self.parent_id = parent_id
        self.tags = tags or []

    def to_dict(self) -> Dict:
        """Convert task to dictionary for storage"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'priority': self.priority.name,
            'energy': self.energy.name,
            'project': self.project,
            'notes': self.notes,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'estimated_minutes': self.estimated_minutes,
            'is_completed': self.is_completed,
            'parent_id': self.parent_id,
            'tags': self.tags
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        return cls(**data)

    def complete(self):
        """Mark task as completed with timestamp"""
        self.is_completed = True
        self.completed_at = datetime.now().isoformat()

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.is_completed:
            return False
        return datetime.fromisoformat(self.due_date) < datetime.now()

    def is_due_soon(self) -> bool:
        """Check if task is due within 24 hours"""
        if not self.due_date or self.is_completed:
            return False
        due = datetime.fromisoformat(self.due_date)
        return datetime.now() < due < datetime.now() + timedelta(days=1)


class TodoList:
    """Main todo list manager with psychological features"""

    def __init__(self, data_file: str = None):
        self.data_file = data_file or str(Path.home() / '.mindful_todo.json')
        self.tasks: List[Task] = []
        self.next_id = 1
        self.stats = {
            'completed_today': 0,
            'completed_this_week': 0,
            'total_completed': 0,
            'current_streak': 0
        }
        self.load()

    def load(self):
        """Load tasks from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
                    self.stats = data.get('stats', self.stats)
            except Exception as e:
                print(f"Error loading data: {e}")
                self.tasks = []

    def save(self):
        """Save tasks to file"""
        data = {
            'tasks': [t.to_dict() for t in self.tasks],
            'next_id': self.next_id,
            'stats': self.stats,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_task(self, task: Task) -> Task:
        """Add a new task"""
        task.task_id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Complete a task and update stats"""
        task = self.get_task(task_id)
        if task and not task.is_completed:
            task.complete()
            self.stats['completed_today'] += 1
            self.stats['completed_this_week'] += 1
            self.stats['total_completed'] += 1
            self.save()
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save()
            return True
        return False

    def get_active_tasks(self, include_completed: bool = False) -> List[Task]:
        """Get all active tasks"""
        if include_completed:
            return self.tasks
        return [t for t in self.tasks if not t.is_completed]

    def get_daily_focus(self, max_tasks: int = 3) -> List[Task]:
        """
        Get recommended daily focus tasks
        Psychological principle: Limit to 3 main tasks to avoid overwhelm
        """
        active = self.get_active_tasks()

        # Prioritize: overdue > due soon > urgent+important > important
        scored = []
        for task in active:
            score = 0
            if task.is_overdue():
                score += 1000
            elif task.is_due_soon():
                score += 500

            if task.priority == Priority.URGENT_IMPORTANT:
                score += 100
            elif task.priority == Priority.IMPORTANT:
                score += 50
            elif task.priority == Priority.URGENT:
                score += 40

            scored.append((score, task))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [task for _, task in scored[:max_tasks]]

    def get_quick_wins(self) -> List[Task]:
        """Get quick tasks for momentum building"""
        active = self.get_active_tasks()
        return [t for t in active if t.energy == Energy.QUICK][:5]

    def get_tasks_by_energy(self, energy: Energy) -> List[Task]:
        """Get tasks by required energy level"""
        active = self.get_active_tasks()
        return [t for t in active if t.energy == energy]

    def get_tasks_by_project(self, project: str) -> List[Task]:
        """Get tasks for a specific project"""
        active = self.get_active_tasks()
        return [t for t in active if t.project.lower() == project.lower()]

    def get_projects(self) -> List[str]:
        """Get list of all projects"""
        projects = set()
        for task in self.get_active_tasks():
            projects.add(task.project)
        return sorted(list(projects))

    def break_down_task(self, task_id: int, subtasks: List[str]) -> List[Task]:
        """
        Break down a large task into smaller ones
        Psychological principle: Chunking reduces overwhelm
        """
        parent = self.get_task(task_id)
        if not parent:
            return []

        created = []
        for subtask_title in subtasks:
            subtask = Task(
                title=subtask_title,
                priority=parent.priority,
                energy=Energy.LOW,  # Subtasks are usually easier
                project=parent.project,
                parent_id=parent.task_id,
                estimated_minutes=parent.estimated_minutes // len(subtasks)
            )
            created.append(self.add_task(subtask))

        # Mark parent as completed or move to someday
        parent.priority = Priority.SOMEDAY
        self.save()

        return created

    def get_motivation_message(self) -> str:
        """Generate encouraging message based on progress"""
        completed = self.stats['completed_today']

        messages = {
            0: "Ready to start? Every journey begins with a single step! 🌱",
            1: "Great start! You've completed your first task! 🎉",
            2: "You're building momentum! Keep it going! 💪",
            3: "Fantastic! You've hit your daily goal of 3 tasks! ⭐",
            5: "You're on fire! 5 tasks completed! 🔥",
            10: "Incredible productivity today! 10 tasks! You're a champion! 🏆"
        }

        # Return the message for the highest milestone reached
        for threshold in sorted(messages.keys(), reverse=True):
            if completed >= threshold:
                return messages[threshold]

        return "Keep going! You're doing great! 💫"
