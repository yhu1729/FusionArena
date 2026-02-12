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
        for value in text.values():
            print(value, file=f)


def build_text_publications(data):
    text = ''
    text += '## Publications\n'
    text += '\n'

    data = [{
        'doi': entry[0],
        'year': int(entry[1]),
        'code': entry[2].split(';'),
        'title': entry[3],
        'author': entry[4].split(';'),
        'keyword': entry[5].split(';'),
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
        if entry['keyword'][0] != '':
            line_keyword = f'  - {', '.join([value for value in entry['keyword']])}'
            text += f'{line}\n{line_keyword}\n'
        else:
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
        'code': entry[2].split(';'),
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

    data = [entry for entry in data if entry['code'] != ['']]
    for entry in data:
        if entry['year'] not in year_list:
            year_list.append(entry['year'])
        for code in entry['code']:
            if code not in score.keys():
                score[code] = {}
    year_list = list(range(min(year_list) - 1, max(year_list) + 1))

    score = dict(sorted(score.items(), key=lambda entry: entry[0].lower(), reverse=True))
    for code in score.keys():
        score[code] = {year: 0 for year in year_list}
        score_partial_sum[code] = {year: 0 for year in year_list}
    print(f'Label count: {len(score.keys())}')

    for entry in data:
        for code in entry['code']:
            score[code][entry['year']] += 1

    for entry in data:
        for code in entry['code']:
            for year in range(entry['year'], year_list[-1] + 1):
                score_partial_sum[code][year] += 1

    # 50 colors
    # tool: https://medialab.github.io/iwanthue/
    # H: 0 - 360
    # C: 30 - 80
    # L: 30 - 100
    color_map = [
        '#017bc9',
        '#cac400',
        '#913dc3',
        '#a6fb65',
        '#d4119a',
        '#00c051',
        '#f045be',
        '#00a427',
        '#ff70eb',
        '#f4ff77',
        '#0248b8',
        '#ffc028',
        '#a787ff',
        '#417100',
        '#e28eff',
        '#00742a',
        '#bd0076',
        '#d7ffa1',
        '#79197d',
        '#ffd15b',
        '#9c9cff',
        '#ab8d00',
        '#623279',
        '#fffcbc',
        '#7d1e68',
        '#00d5c2',
        '#e71c43',
        '#4ae4ff',
        '#a80013',
        '#84e9ff',
        '#ff544c',
        '#01a69e',
        '#ff4467',
        '#005518',
        '#ffa2e4',
        '#7c5a00',
        '#cbb5ff',
        '#b55f00',
        '#028cc5',
        '#ffa565',
        '#71d3d1',
        '#b6004e',
        '#5e4210',
        '#ff697a',
        '#c89a72',
        '#950039',
        '#8d5476',
        '#872015',
        '#861c42',
        '#743236',
    ]
    color_map = color_map[:len(score.keys())]

    figure = pyplot.figure(figsize=(16, 24))

    ax = figure.add_subplot(2, 1, 1)
    ax.set_title('Total publications')
    y = [value for value in score_partial_sum.values()]
    y = [list(value.values()) for value in y]
    label_list = [
        f'{key} ({value[year_list[-1]]})'
        for key, value in score_partial_sum.items()
    ]
    ax.set_prop_cycle(color=color_map[::-1])
    ax.stackplot(year_list, y, labels=label_list)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    handle, label = ax.get_legend_handles_labels()
    ax.legend(handle[::-1], label[::-1])

    ax = figure.add_subplot(2, 1, 2)
    ax.set_title('Publications')
    ax.set_prop_cycle(color=color_map[::-1])
    bottom = numpy.zeros(len(year_list))
    for key, value in score.items():
        x, y = zip(*sorted(value.items()))
        ax.bar(x, y, label=key, bottom=bottom)
        bottom += y
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    handle, label = ax.get_legend_handles_labels()
    ax.legend(handle[::-1], label[::-1])

    figure.savefig('figure/publications.png', dpi=400, bbox_inches='tight')


if __name__ == '__main__':
    build_readme()
