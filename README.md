# jiraIssueTemplate

Generate a Jira Issue with summary description and sub-tasks directly from a defined template definition.

## usage

```
$ python3 template.py --config=config.json --template=template.json
```

### config.json

This file is used to configure your Jira server credentials.

```json
{
  "server": "https://xxxx.atlassian.net/",
  "username": "",
  "password": ""
}
```

### template.json

This file is used to configure the Issue details.

```json
{
  "project": "XXX",
  "task": {
    "summary": "Parent task",
    "description": "Parent task description",
    "tasks": [
      {
        "summary": "Sub-task #1",
        "description": "..."
      },
      {
        "summary": "Sub-task #2",
        "description": "..."
      }
    ]
  }
}
```
