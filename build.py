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

    data['datasets'] = None

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

    for row in data[1:]:
        doi = row[0]
        year = row[1]
        tag = row[2]
        title = row[3]
        author = row[4]

        doi_url = f'https://doi.org/{doi}'

        author = author.split(';')
        if len(author) >= 3:
            author = f'{author[0]} at el.'
        elif len(author) == 2:
            author = f'{author[0]} and {author[1]}'
        else:
            author = f'{author[0]}'

        line = f'- {title}. {author} ({year}) [{doi}]({doi_url})'

        text += f'{line}\n'

    return text


def build_text_codes(data):
    text = ''
    text += '## Codes\n'
    text += '\n'

    for row in data[1:]:
        name = row[0]
        url = row[1]

        line = f'- [{name}]({url})'

        text += f'{line}\n'

    return text


def build_text_datasets(data):
    text = ''
    text += '## Datasets\n'

    return text


if __name__ == '__main__':
    build_readme()
