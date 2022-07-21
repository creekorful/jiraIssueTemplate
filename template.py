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

    task = template['task']
    task['project'] = {'key': template['project']}
    task['issuetype'] = {'name': 'Task'}

    sub_tasks = task.pop('tasks', [])

    parent = jira.create_issue(template['task'])

    for task in sub_tasks:
        fields = task
        fields['project'] = {'key': template['project']}
        fields['issuetype'] = {'name': 'Sub-task'}
        fields['parent'] = {'key': parent.key}

        jira.create_issue(fields)

    print("Successfully created issue #{} ({}) and the {} linked sub-tasks.".format(parent.key, parent.fields.summary,
                                                                                    len(sub_tasks)))


if __name__ == '__main__':
    main()
