# 🧠 Mindful Todo

A psychologically-informed task management app designed to reduce anxiety, build momentum, and help you actually get things done.

## 🎯 Why Mindful Todo?

Most todo apps just give you a list. **Mindful Todo** is built on productivity psychology research to help you:

- **Reduce overwhelm** - Focus on just 3 tasks per day
- **Build momentum** - Celebrate small wins with positive reinforcement
- **Work with your energy** - Match tasks to your current energy level
- **Break down big tasks** - Chunk large projects into manageable pieces
- **Prioritize effectively** - Use proven frameworks (Eisenhower Matrix)
- **Stay motivated** - Get encouraging messages based on your progress

## ✨ Key Features

### 🎯 Daily Focus Mode
Instead of an overwhelming list, see your **top 3 priorities** each day. Research shows limiting your daily goals to 3 important tasks significantly increases completion rates.

### 🌊 Energy-Aware Prioritization
Tasks are tagged by required energy:
- **🧠 High Focus** - Deep work, important thinking
- **⚡ Medium Energy** - Regular work tasks
- **🌊 Low Energy** - Easy tasks for when you're tired
- **⚡ Quick (< 5 min)** - Small wins to build momentum

### 🎉 Positive Reinforcement
Every completed task gets a celebration! The app tracks your progress and gives encouraging messages to keep you motivated.

### 🔨 Task Breakdown
Feeling overwhelmed by a big task? Break it down into smaller subtasks. The app helps you chunk large projects into manageable pieces.

### 📊 Smart Prioritization
Uses psychology-backed priority levels:
- **🔥 Urgent & Important** - Do these first
- **⭐ Important** - Schedule time for these
- **⚡ Urgent** - Delegate or do quickly
- **📌 Normal** - Regular tasks
- **💭 Someday/Maybe** - Ideas for later

### 📁 Project Organization
Group tasks by project (work, personal, learning, etc.) to keep related tasks together.

## 🚀 Quick Start

### Installation

```bash
cd mindful_todo
chmod +x todo
./todo --help
```

### Basic Usage

**Add your first task:**
```bash
./todo add "Write project proposal"
```

**See your daily focus:**
```bash
./todo focus
```

**Complete a task:**
```bash
./todo done 1
```

**List all tasks:**
```bash
./todo list
```

## 📖 Complete Guide

### Adding Tasks

**Simple task:**
```bash
./todo add "Call dentist"
```

**Task with priority and project:**
```bash
./todo add "Finish report" -p work -P urgent-important
```

**Task with due date and energy level:**
```bash
./todo add "Review code" -d tomorrow -e high -t 60
```

**Full example:**
```bash
./todo add "Write quarterly report" \
  -p work \
  -P urgent-important \
  -e high \
  -d 2024-12-31 \
  -t 120 \
  -n "Include Q3 metrics and future projections"
```

### Priority Levels

Use the `-P` or `--priority` flag:

- `ui` or `urgent-important` - 🔥 Do first (deadline + impact)
- `i` or `important` - ⭐ Schedule time (high impact)
- `u` or `urgent` - ⚡ Do soon (deadline)
- `n` or `normal` - 📌 Regular tasks (default)
- `s` or `someday` - 💭 Ideas for later

### Energy Levels

Use the `-e` or `--energy` flag:

- `h` or `high` - 🧠 High Focus (requires deep concentration)
- `m` or `medium` - ⚡ Medium Energy (regular work)
- `l` or `low` - 🌊 Low Energy (easy tasks)
- `q` or `quick` - ⚡ Quick (< 5 minutes)

**Pro tip:** Do high-focus tasks during your peak energy hours!

### Due Dates

Use the `-d` or `--due` flag:

```bash
./todo add "Submit report" -d today
./todo add "Prepare presentation" -d tomorrow
./todo add "File taxes" -d 2024-12-31
```

### Time Estimates

Use the `-t` or `--time` flag (in minutes):

```bash
./todo add "Quick email" -t 5
./todo add "Write blog post" -t 120
```

This helps you plan your day realistically!

### Daily Focus

See your most important tasks:

```bash
./todo focus
```

This shows:
- Your top 3 priorities for today
- Quick wins to build momentum
- Motivational message based on progress

**Pro tip:** Run `./todo focus` every morning!

### Viewing Tasks

**All tasks:**
```bash
./todo list
# or
./todo ls
```

**Tasks by project:**
```bash
./todo list -P work
./todo list -P personal
```

**Tasks by energy:**
```bash
./todo list -e high
./todo list -e quick
```

### Completing Tasks

```bash
./todo done 5
# or
./todo complete 5
./todo finish 5
```

Get a celebration and motivational message! 🎉

### Breaking Down Large Tasks

Overwhelmed by a big task? Break it down:

```bash
./todo break 3
```

Then enter subtasks one per line:
```
→ Research topic
→ Create outline
→ Write first draft
→ Edit and revise
→ Submit for review
```

The original task becomes a "Someday" item, and you get manageable subtasks!

### Project Management

**See all projects:**
```bash
./todo projects
```

**View tasks in a project:**
```bash
./todo list -P work
```

### Statistics

Track your progress:

```bash
./todo stats
```

Shows:
- Tasks completed today
- Tasks completed this week
- Total completed tasks
- Current active tasks

## 🧠 Psychological Principles

### 1. Limiting Daily Goals (Rule of 3)

Research shows that people who limit themselves to 3 main goals per day have significantly higher completion rates than those with longer lists. This reduces decision fatigue and cognitive overload.

**Mindful Todo:** The `focus` command shows only your top 3 priorities.

### 2. Positive Reinforcement

Celebrating small wins releases dopamine, creating positive associations with task completion and increasing motivation.

**Mindful Todo:** Every completed task gets a celebration with encouraging messages.

### 3. Task Chunking

Breaking large tasks into smaller pieces makes them less overwhelming and easier to start. This overcomes procrastination caused by task complexity.

**Mindful Todo:** The `break` command helps you chunk large tasks.

### 4. Energy Management

Matching tasks to your energy level is more effective than pure time management. High-focus work requires high energy.

**Mindful Todo:** Tasks are tagged by energy requirements so you can work with your natural rhythms.

### 5. Quick Wins for Momentum

Starting with quick, easy tasks creates momentum and builds confidence for tackling harder tasks.

**Mindful Todo:** The focus view shows "Quick Wins" to help you get started.

### 6. Eisenhower Matrix

Prioritizing by urgency AND importance helps you focus on what truly matters, not just what's screaming loudest.

**Mindful Todo:** Priority system based on this proven framework.

### 7. Progress Visualization

Seeing your progress motivates continued effort and creates a sense of accomplishment.

**Mindful Todo:** Stats tracking shows your completed tasks and current streak.

## 💡 Best Practices

### Morning Routine

1. Run `./todo focus` to see your top priorities
2. Choose one quick win to build momentum
3. Tackle your hardest task during peak energy
4. Celebrate each completion!

### Weekly Review

1. Run `./todo stats` to see your progress
2. Review `./todo projects` to check project status
3. Clean up completed tasks
4. Plan next week's priorities

### Managing Overwhelm

Feeling overwhelmed? Try this:

1. Do one quick win (< 5 min task)
2. Break down large tasks: `./todo break [id]`
3. Focus on just TODAY's top 3
4. Celebrate small progress

### Energy-Based Scheduling

- **Morning (high energy):** High focus tasks
- **Midday (medium energy):** Regular work tasks
- **Afternoon (low energy):** Easy tasks, admin work
- **Any time:** Quick wins (< 5 min)

## 📱 Daily Workflow Example

**Morning:**
```bash
# See what's important today
./todo focus

# Add any new tasks
./todo add "Review PR #123" -p work -e medium -d today

# Start with a quick win
./todo done 5

# Tackle the most important task
./todo done 1
```

**Afternoon:**
```bash
# Check progress
./todo stats

# Do some low-energy tasks
./todo list -e low
./todo done 7
```

**Evening:**
```bash
# Add tomorrow's tasks while they're fresh
./todo add "Prepare for meeting" -p work -d tomorrow -e high
./todo add "Call insurance" -e quick -P urgent
```

## 🎨 Beautiful Output

Mindful Todo uses colors and emojis to make your tasks clear and motivating:

- ✓ Green checkmarks for completed tasks
- ☐ Blue boxes for incomplete tasks
- 🔥 Red for urgent+important tasks
- ⭐ Yellow for important tasks
- 🎉 Celebrations for completions
- 📊 Stats visualization

## 🔧 Technical Details

### Data Storage

Tasks are stored in `~/.mindful_todo.json` as JSON. This makes it:
- Easy to back up
- Portable across machines
- Human-readable
- Version control friendly

### No Dependencies

Uses only Python standard library - no external dependencies needed!

### Cross-Platform

Works on Linux, macOS, and Windows (with Python 3.6+).

## 🎓 Learn More

### Productivity Research

This app is based on:
- Getting Things Done (GTD) methodology
- The Eisenhower Matrix
- Energy management principles
- Chunking theory
- Positive psychology research

### Books & Resources

- "The 7 Habits of Highly Effective People" - Stephen Covey
- "Getting Things Done" - David Allen
- "The Power of Habit" - Charles Duhigg
- "Atomic Habits" - James Clear
- "Deep Work" - Cal Newport

## 🚀 Tips for Success

1. **Run `./todo focus` every morning** - Start your day with clarity
2. **Limit yourself to 3 main tasks per day** - Quality over quantity
3. **Match tasks to your energy** - Work with your natural rhythms
4. **Celebrate small wins** - Build positive momentum
5. **Break down big tasks** - Make progress less overwhelming
6. **Review weekly** - Track progress and adjust

## 💬 Philosophy

**Mindful Todo believes:**

- Less is more - Focus beats overwhelm
- Progress > Perfection - Done is better than perfect
- Celebrate everything - Small wins matter
- Work with yourself - Not against your nature
- Reduce anxiety - Structure brings peace
- Build momentum - Success breeds success

## 🎯 Start Now!

Ready to get started? Try these commands:

```bash
# See your focus view (even with no tasks yet)
./todo focus

# Add your first task
./todo add "Try out Mindful Todo" -e quick -P important

# Complete it and get your first celebration!
./todo done 1
```

**Welcome to stress-free productivity! 🎉**

---

Made with 🧠 and 💚 to help you feel good about getting things done.
