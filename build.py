import csv
from matplotlib import pyplot
from matplotlib.ticker import MaxNLocator
import numpy


def build_readme():
    data = {}

    data['publications'] =[]
    with open('data/publications.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['publications'].append(row)

    data['datasets'] = []
    with open('data/datasets.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['datasets'].append(row)

    data['codes'] = []
    with open('data/codes.csv', newline='') as f:
        content = csv.reader(f)
        for row in content:
            data['codes'].append(row)

    text = {}
    text['publications'] = build_text_publications(data['publications'])
    text['datasets'] = build_text_datasets(data['datasets'])
    text['codes'] = build_text_codes(data['codes'])

    with open('README.md', mode='w') as f:
        print('# FusionArena', file=f)
        print('', file=f)
        print(text['publications'], file=f)
        print(text['datasets'], file=f)
        print(text['codes'], file=f)


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

    build_figure_publications(data)
    text += '![figure-publications](figure/publications.png)\n'
    text += '\n'

    for entry in data:
        author = ''
        if len(entry['author']) >= 3:
            author = f'{entry['author'][0]} at el.'
        elif len(entry['author']) == 2:
            author = f'{entry['author'][0]} and {entry['author'][1]}'
        else:
            author = f'{entry['author'][0]}'

        doi_url = f'https://doi.org/{entry['doi']}'

        line = f'- {entry['title']}. {author} ({entry['year']}) [{entry['doi']}]({doi_url})'

        text += f'{line}\n'

    return text


def build_text_codes(data):
    text = ''
    text += '## Codes\n'
    text += '\n'

    data = [{
        'name': entry[0],
        'url': entry[1],
        'language': entry[2].split(';'),
    } for entry in data[1:]]
    data = sorted(data, key=lambda entry: entry['name'].lower())

    for entry in data:
        language = ','.join(entry['language'])

        line = f'- [{entry['name']}]({entry['url']}) ({language})'

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
        author = ''
        if len(entry['author']) >= 3:
            author = f'{entry['author'][0]} at el.'
        elif len(entry['author']) == 2:
            author = f'{entry['author'][0]} and {entry['author'][1]}'
        else:
            author = f'{entry['author'][0]}'

        doi_url = f'https://doi.org/{entry['doi']}'

        line = f'- {entry['title']}. {author} ({entry['year']}) [{entry['doi']}]({doi_url})'

        text += f'{line}\n'

    return text


def build_figure_publications(data):
    year_list = []
    score = {}
    score_partial_sum = {}

    for entry in data:
        if entry['year'] not in year_list:
            year_list.append(entry['year'])
        for tag in entry['tag']:
            if tag not in score.keys():
                score[tag] = {}
    year_list = list(range(min(year_list) - 1, max(year_list) + 1))

    score = dict(sorted(score.items(), key=lambda entry: entry[0].lower()))
    for tag in score.keys():
        score[tag] = {year: 0 for year in year_list}
        score_partial_sum[tag] = {year: 0 for year in year_list}

    for entry in data:
        for tag in entry['tag']:
            score[tag][entry['year']] += 1

    for entry in data:
        for tag in entry['tag']:
            for year in range(entry['year'], year_list[-1] + 1):
                score_partial_sum[tag][year] += 1

    figure = pyplot.figure(figsize=(16, 16))

    ax = figure.add_subplot(2, 1, 1)
    ax.set_title('Total publications')
    y = [value for value in score_partial_sum.values()]
    y = [list(value.values()) for value in y]
    label_list = [key for key in score_partial_sum.keys()]
    ax.stackplot(year_list, y, labels=label_list)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()

    ax = figure.add_subplot(2, 1, 2)
    ax.set_title('Publications')
    bottom = numpy.zeros(len(year_list))
    for key, value in score.items():
        x, y = zip(*sorted(value.items()))
        ax.bar(x, y, label=key, bottom=bottom)
        bottom += y
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()

    figure.savefig('figure/publications.png', dpi=400, bbox_inches='tight')


if __name__ == '__main__':
    build_readme()
