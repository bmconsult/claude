# 🚀 Mindful Todo - Quick Start

Get started in 60 seconds!

## ⚡ 1-Minute Setup

```bash
cd mindful_todo
./todo --help
```

That's it! No installation, no dependencies, just works.

## 📋 Essential Commands

### See What Matters Today
```bash
./todo focus
```
Shows your top 3 priorities + quick wins. **Run this every morning!**

### Add a Task
```bash
./todo add "Your task here"
```

### Add a Task (with details)
```bash
./todo add "Write report" -p work -P important -e high -d tomorrow
```

### Complete a Task
```bash
./todo done 1
```
Get a celebration! 🎉

### List All Tasks
```bash
./todo list
```

### See Your Progress
```bash
./todo stats
```

## 🎯 Priority Shortcuts

When adding tasks, use `-P` for priority:

- `-P ui` = 🔥 Urgent & Important (do first!)
- `-P i` = ⭐ Important (schedule time)
- `-P u` = ⚡ Urgent (do soon)
- `-P n` = 📌 Normal (default)
- `-P s` = 💭 Someday (ideas for later)

## 🌊 Energy Levels

Use `-e` to match tasks to your energy:

- `-e high` = 🧠 Needs deep focus
- `-e medium` = ⚡ Regular work
- `-e low` = 🌊 Easy tasks
- `-e quick` = ⚡ Under 5 minutes

## 📅 Due Dates

- `-d today` = Due today
- `-d tomorrow` = Due tomorrow
- `-d 2024-12-31` = Specific date

## 💡 Quick Tips

1. **Morning:** `./todo focus` - see your top 3
2. **Do quick tasks first** - build momentum
3. **High-energy work in morning** - tackle hard stuff early
4. **Celebrate completions** - enjoy the dopamine!
5. **Overwhelmed?** - `./todo break [id]` to split big tasks

## 🎮 Try It Now

Copy and paste these commands to see it in action:

```bash
# Add some example tasks
./todo add "Review emails" -e quick -P normal
./todo add "Write project proposal" -p work -P urgent-important -e high -d tomorrow
./todo add "Call dentist" -e quick -P urgent
./todo add "Learn new framework" -p learning -e medium

# See your focus
./todo focus

# Complete the quick task
./todo done 1

# See your progress
./todo stats
```

## 🧠 The Secret Sauce

**Limit yourself to 3 main tasks per day.**

Research shows this dramatically increases completion rates. The `focus` command does this automatically!

## 📖 Learn More

See `README.md` for:
- Complete command reference
- Psychological principles
- Best practices
- Daily workflow examples

## 🎯 Daily Workflow

**Every Morning:**
```bash
./todo focus
```

**When You Finish a Task:**
```bash
./todo done [task-id]
```

**When You Think of Something:**
```bash
./todo add "That thing" -p project
```

**Every Evening:**
```bash
./todo stats
```

That's it! Simple, effective, stress-free. 🎉

---

**Start now:**
```bash
./todo focus
```
