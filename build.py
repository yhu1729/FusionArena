import csv


def build_readme():
    data = {}

    data['publications'] =[]
    with open('data/publications.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['publications'].append(row)

    data['codes'] = []
    with open('data/codes.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['codes'].append(row)

    data['datasets'] = []
    with open('data/datasets.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['datasets'].append(row)

    text = {}
    text['publications'] = build_text_publications(data['publications'])
    text['codes'] = build_text_codes(data['codes'])
    text['datasets'] = build_text_datasets(data['datasets'])

    with open('README.md', mode='w') as f:
        print('# FusionArena', file=f)
        print('', file=f)
        print(text['publications'], file=f)
        print(text['codes'], file=f)
        print(text['datasets'], file=f)


def build_text_publications(data):
    text = ''
    text += '## Publications\n'
    text += '\n'

    data = [{
        'doi': entry[0],
        'year': int(entry[1]),
        'tag': entry[2].split(';'),
        'title': entry[3],
        'author': entry[4].split(';'),
    } for entry in data[1:]]
    data = sorted(data, key=lambda entry: entry['author'], reverse=False)
    data = sorted(data, key=lambda entry: entry['year'], reverse=True)

    for entry in data:
        if len(entry['author']) >= 3:
            entry['author'] = f'{entry['author'][0]} at el.'
        elif len(entry['author']) == 2:
            entry['author'] = f'{entry['author'][0]} and {entry['author'][1]}'
        else:
            entry['author'] = f'{entry['author'][0]}'

        doi_url = f'https://doi.org/{entry['doi']}'

        line = f'- {entry['title']}. {entry['author']} ({entry['year']}) [{entry['doi']}]({doi_url})'

        text += f'{line}\n'

    return text


def build_text_codes(data):
    text = ''
    text += '## Codes\n'
    text += '\n'

    data = [{
        'name': entry[0],
        'url': entry[1],
    } for entry in data[1:]]
    data = sorted(data, key=lambda entry: entry['name'].lower())

    for entry in data:
        line = f'- [{entry['name']}]({entry['url']})'

        text += f'{line}\n'

    return text


def build_text_datasets(data):
    text = ''
    text += '## Datasets\n'
    text += '\n'

    data = [{
        'doi': entry[0],
        'year': int(entry[1]),
        'tag': entry[2].split(';'),
        'title': entry[3],
        'author': entry[4].split(';'),
    } for entry in data[1:]]
    data = sorted(data, key=lambda entry: entry['author'], reverse=False)
    data = sorted(data, key=lambda entry: entry['year'], reverse=True)

    for entry in data:
        if len(entry['author']) >= 3:
            entry['author'] = f'{entry['author'][0]} at el.'
        elif len(entry['author']) == 2:
            entry['author'] = f'{entry['author'][0]} and {entry['author'][1]}'
        else:
            entry['author'] = f'{entry['author'][0]}'

        doi_url = f'https://doi.org/{entry['doi']}'

        line = f'- {entry['title']}. {entry['author']} ({entry['year']}) [{entry['doi']}]({doi_url})'

        text += f'{line}\n'

    return text


if __name__ == '__main__':
    build_readme()
