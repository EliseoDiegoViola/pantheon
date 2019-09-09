# assign_to_project.py

When one or more HumanUsers are assigned to a Task (directly or via a Group)
that is linked to a Project that those HumanUsers aren't already assigned to,
this plugin assigns them to that Project.

Note that this trigger doesn't unassign HumanUsers if they are removed from a
Task's task_assignees field; so be careful when adding HumanUsers to Tasks
because they may end up assigned to Projects they should not have access to.

## Demo

![](images/assign_to_project1.gif?raw=true)

## Args

No settings.
