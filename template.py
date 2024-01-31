import json

import click
from jira import JIRA


@click.command()
@click.option('--template', default='template.json', help='Path to the template file.')
@click.option('--config', default='config.json', help='Path to the config file.')
def main(template: str, config: str):
    with open(template) as f:
        template = json.load(f)

    with open(config) as f:
        config = json.load(f)

    jira = JIRA(server=config['server'], basic_auth=(config['username'], config['password']))

    issue_types = jira.project(template['project']).raw['issueTypes']
    task_type = list(filter(lambda t: t['name'] == 'Task', issue_types))[0]
    subtask_type = list(filter(lambda t: t['subtask'], issue_types))[0]

    task = template['task']

    if task.get('epic_name') is not None:
        epic_type = list(filter(lambda t: t['name'] == 'Epic', issue_types))[0]

        fields = task
        fields['project'] = {'key': template['project']}
        fields['issuetype'] = epic_type

        parent = jira.create_issue(fields)

        task['parent'] = {'key': parent.key}

    task['project'] = {'key': template['project']}
    task['issuetype'] = task_type

    sub_tasks = task.pop('tasks', [])

    parent = jira.create_issue(task)

    for task in sub_tasks:
        fields = task
        fields['project'] = {'key': template['project']}
        fields['issuetype'] = subtask_type
        fields['parent'] = {'key': parent.key}

        jira.create_issue(fields)

    print("Successfully created issue #{} ({}) and the {} linked sub-tasks.".format(parent.key, parent.fields.summary,
                                                                                    len(sub_tasks)))


if __name__ == '__main__':
    main()
