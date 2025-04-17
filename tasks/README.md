# Tasks Module

This module provides a personal to-do list application with bounty tracking features for the Personal Dashboard.

## Core Features

### Task Management
- Create, read, update, and delete tasks
- Filter tasks by status and priority
- Mark tasks as complete to earn bounties

### Task Properties
- **Title** (required): Brief description of the task
- **Description** (optional): Detailed description of the task
- **Due Date** (optional): When the task should be completed
- **Priority** (low, medium, high): Task importance
- **Status** (not started, in progress, completed): Current state of the task
- **Bounty** (numeric value): Points earned upon task completion

### Bounty System
- Earn bounty points when tasks are marked as completed
- Track total bounties earned over time
- Set weekly bounty goals to motivate productivity
- View bounty velocity through time-based charts

## Dashboard Features
- **Tasks List**: View, filter, and manage all tasks
- **Bounty Dashboard**: Track productivity metrics
  - Total bounties earned
  - Current week's progress
  - Weekly velocity chart
  - Goal setting and tracking

## Technical Implementation

### Models
- `Task`: Stores task data and provides utility methods
- `BountyGoal`: Tracks weekly bounty goals

### Views
- Task CRUD operations
- Bounty dashboard with statistics and charts
- Integration with the main dashboard

### Templates
- Modern, responsive UI with Tailwind CSS
- Interactive charts for data visualization
- User-friendly forms for task management

## Tests
The module includes comprehensive test coverage:
- Model tests for data integrity and method behavior
- Form tests for validation
- View tests for proper rendering and functionality
- Integration tests with the main dashboard

## Usage
1. Navigate to the Tasks list from the main dashboard
2. Create new tasks with appropriate details and bounty values
3. Update task status as you work on them
4. Mark tasks as completed to earn bounties
5. Visit the Bounty Dashboard to track your productivity

## Future Enhancements
- Task categories/tags for better organization
- Recurring tasks
- Due date reminders
- Enhanced reporting and analytics
- Mobile notifications