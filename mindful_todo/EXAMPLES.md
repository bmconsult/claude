# 📝 Mindful Todo - Real-World Examples

## 🎯 Common Scenarios

### Scenario 1: Monday Morning Planning

```bash
# Check what's on your plate
./todo list

# Add this week's priorities
./todo add "Finish Q4 budget review" -p work -P urgent-important -e high -d friday -t 180
./todo add "Prepare team presentation" -p work -P important -e high -d thursday -t 120
./todo add "Schedule dentist appointment" -e quick -P urgent
./todo add "Review project proposals" -p work -e medium -t 90 -d wednesday

# See your focus for today
./todo focus
```

### Scenario 2: Overwhelmed by a Big Project

```bash
# You have a huge task
./todo add "Launch new product feature" -p work -P urgent-important -e high

# Break it down
./todo break 1

# Enter subtasks:
→ Write technical specification
→ Review spec with team
→ Implement core functionality
→ Write tests
→ Create documentation
→ Deploy to staging
→ Get stakeholder approval
→ Deploy to production

# Now you have manageable pieces!
./todo focus
```

### Scenario 3: Low Energy Afternoon

```bash
# It's 3pm, you're tired but want to stay productive
./todo list -e low

# Work on easy tasks
./todo done 12  # Organize files
./todo done 13  # Reply to simple emails
./todo done 14  # Update spreadsheet

# Check your progress - feel good!
./todo stats
```

### Scenario 4: Starting Your Day with Momentum

```bash
# Morning: See your focus
./todo focus

# Start with quick wins
./todo done 5  # Quick email - 2 min
./todo done 7  # Schedule meeting - 3 min

# Now you're warmed up for the hard stuff!
./todo done 1  # Big important task

# Celebrate your progress
./todo stats
```

## 💼 Work-Specific Examples

### Software Developer

```bash
# Morning standup prep
./todo add "Review PRs" -p work -e medium -d today -t 30
./todo add "Fix critical bug #432" -p work -P urgent-important -e high -d today -t 120
./todo add "Update documentation" -p work -e low -t 45

# Focus time
./todo add "Implement user authentication" -p feature -P important -e high -t 240

# Code review
./todo add "Review team's PRs" -p work -e medium -d today -t 60

# See what needs high focus
./todo list -e high
```

### Project Manager

```bash
# Weekly planning
./todo add "Update project timeline" -p management -P important -e medium -t 60
./todo add "Send status report" -p management -P urgent -d friday -t 30
./todo add "Schedule 1-on-1s" -p management -e low -t 45

# Meetings
./todo add "Prepare board presentation" -p management -P urgent-important -e high -d monday -t 180

# Follow-ups
./todo add "Follow up on action items" -p management -e quick -t 10

./todo projects  # See all your projects
```

### Freelancer

```bash
# Client work
./todo add "Design mockups for Client A" -p client-a -P urgent-important -e high -d friday -t 300
./todo add "Review feedback from Client B" -p client-b -e medium -t 45
./todo add "Send invoice to Client C" -p admin -e quick -P urgent -d today

# Business development
./todo add "Update portfolio" -p marketing -e medium -t 120
./todo add "Reply to project inquiry" -p leads -e quick -P urgent -t 15

# See client work
./todo list -P client-a
```

## 🏠 Personal Life Examples

### Weekend Planning

```bash
# Chores
./todo add "Grocery shopping" -p home -e low -t 60 -d saturday
./todo add "Laundry" -p home -e low -t 30
./todo add "Clean kitchen" -p home -e medium -t 45

# Personal projects
./todo add "Research vacation destinations" -p personal -e low -t 90
./todo add "Call parents" -p personal -e quick -P important
./todo add "Read 2 chapters" -p learning -e low -t 45

# Health
./todo add "Go for run" -p health -e medium -d today -t 30
./todo add "Meal prep for week" -p health -e medium -t 120
```

### Learning New Skills

```bash
# Study plan
./todo add "Complete Python course module 3" -p learning -e high -t 120 -d friday
./todo add "Practice coding exercises" -p learning -e medium -t 60
./todo add "Watch tutorial video" -p learning -e low -t 45
./todo add "Read documentation" -p learning -e medium -t 30

# Build project
./todo add "Build portfolio website" -p project -P important -e high
./todo break [id]
→ Design layout
→ Set up development environment
→ Build homepage
→ Add projects section
→ Deploy to hosting
```

## 🎯 Advanced Workflows

### GTD (Getting Things Done) Style

```bash
# Inbox processing
./todo add "Process emails" -e quick -d today
./todo add "Clear download folder" -e low -t 15
./todo add "Review meeting notes" -e medium -t 30

# Next actions
./todo add "Call vendor about order" -p work -e quick -P urgent
./todo add "Draft proposal" -p work -P important -e high -t 120

# Waiting for
./todo add "Follow up on report from Sarah" -p work -e quick -d friday

# Someday/Maybe
./todo add "Learn Docker" -p learning -P someday -e high
./todo add "Redesign home office" -p personal -P someday -e medium
```

### Time Blocking

```bash
# Morning block (9am-12pm) - High energy work
./todo list -e high
./todo add "Write article" -p writing -P important -e high -t 120
./todo add "Deep work on architecture" -p work -P important -e high -t 120

# Afternoon block (1pm-3pm) - Medium energy
./todo list -e medium
./todo add "Team meetings" -p work -e medium -t 90
./todo add "Review analytics" -p work -e medium -t 45

# Evening block (3pm-5pm) - Low energy
./todo list -e low
./todo add "Respond to emails" -p work -e low -t 60
./todo add "File expenses" -p admin -e low -t 30
```

### Sprint Planning (Agile)

```bash
# Sprint 12 - Two weeks
./todo add "User story: Login flow" -p sprint12 -P urgent-important -e high -d 2024-12-01
./todo add "Bug fix: Payment processing" -p sprint12 -P urgent-important -e high -d 2024-11-28
./todo add "Feature: Dark mode" -p sprint12 -P important -e medium -d 2024-12-05

# Break down stories
./todo break 1
→ Design login UI
→ Implement authentication
→ Add password reset
→ Write tests
→ Update documentation

# Daily standup
./todo list -P sprint12
```

## 🔄 Habit Building

### Morning Routine

```bash
# Same tasks every day
./todo add "Morning meditation" -p habits -e low -t 10 -d today
./todo add "Journal 3 things I'm grateful for" -p habits -e low -t 5 -d today
./todo add "Review daily goals" -p habits -e quick -d today

# Build the habit of checking focus
./todo focus
```

### Weekly Review

```bash
# Friday afternoon review
./todo stats  # See what you accomplished

# Clean up
./todo list -P someday  # Review someday items
./todo list  # Archive completed tasks

# Plan next week
./todo add "Plan sprint 13" -p work -P important -e high -d monday
./todo add "Update roadmap" -p work -P important -e medium -d tuesday
```

## 💡 Pro Tips in Action

### The 2-Minute Rule

```bash
# If it takes < 2 minutes, mark it as quick
./todo add "Reply to simple email" -e quick
./todo add "File that document" -e quick
./todo add "Send quick message" -e quick

# See all quick tasks
./todo list -e quick

# Do them all at once
./todo done 5
./todo done 6
./todo done 7
```

### Eating the Frog

```bash
# Add your hardest task
./todo add "Write difficult email to stakeholder" -p work -P urgent-important -e high -d today

# Do it FIRST thing in the morning
./todo focus  # It'll be priority #1
./todo done 1  # Get it done!

# Rest of day feels easier!
```

### Energy Matching

```bash
# Monday 9am (high energy)
./todo list -e high
./todo done 1  # Tackle the hard stuff

# Monday 3pm (low energy)
./todo list -e low
./todo done 8  # Easy admin work

# Maximize productivity by working with your energy!
```

## 🎨 Custom Workflows

### Content Creator

```bash
./todo add "Research video topic" -p youtube -e medium -t 60 -d monday
./todo add "Write script" -p youtube -P important -e high -t 120 -d tuesday
./todo add "Film video" -p youtube -P important -e high -t 180 -d wednesday
./todo add "Edit video" -p youtube -P urgent -e high -t 240 -d thursday
./todo add "Create thumbnail" -p youtube -e medium -t 45 -d thursday
./todo add "Write description & schedule" -p youtube -e low -t 30 -d friday

./todo list -P youtube
```

### Student

```bash
./todo add "Read Chapter 5" -p biology -e medium -t 60 -d today
./todo add "Complete math problem set" -p math -P urgent -e high -t 90 -d tomorrow
./todo add "Start essay outline" -p english -P important -e high -t 60 -d friday
./todo add "Study for quiz" -p history -P urgent -e medium -t 45 -d thursday

./todo projects  # See all classes
```

---

These examples show the flexibility of Mindful Todo. Find what works for you! 🎯
