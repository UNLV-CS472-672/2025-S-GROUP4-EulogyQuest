from datetime import datetime
import json
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

TITLE_FONT_SIZE = 28
LABEL_FONT_SIZE = 24
TICK_FONT_SIZE = 20
LEGEND_FONT_SIZE = 20

projectStart = datetime(2025, 3, 6)
weekCount = list(range(1, ((datetime.today() - projectStart).days // 7) + 1))

def githubActivity(names, prs):
    fig, ax = plt.subplots(figsize=(16, 9), layout='tight')

    for i, userdata in enumerate(prs):
        for j, date in enumerate(prs[i]):
            prs[i][j] = date.split('T')[0]
            prs[i][j] = ((datetime.strptime(prs[i][j], '%Y-%m-%d') - projectStart).days // 7) + 1
        prs[i] = Counter(prs[i])
        weeklyCount = [prs[i].get(week, 0) for week in weekCount]
        ax.plot(weekCount, weeklyCount, label=names[i], linewidth=3)

    ax.set_xlabel('Week', fontsize=LABEL_FONT_SIZE)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel('Pull Requests', fontsize=LABEL_FONT_SIZE)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Weekly PR Activity', fontsize=TITLE_FONT_SIZE)
    ax.tick_params(labelsize=TICK_FONT_SIZE)
    ax.legend(fontsize=LEGEND_FONT_SIZE)

    plt.tight_layout()
    plt.savefig('chart_1_weekly_prs.png', dpi=150)
    plt.close()

def memberContributions(names, prs, reviews, issues, comments):
    fig, ax = plt.subplots(figsize=(16, 9), layout='tight')
    xAxis = np.arange(len(names))
    width = 0.2

    ax.bar(xAxis - (1.5 * width), prs, width=width, label='PRs')
    ax.bar(xAxis - (width / 2), reviews, width=width, label='PR-Reviews')
    ax.bar(xAxis + (width / 2), issues, width=width, label='Issues')
    ax.bar(xAxis + (1.5 * width), comments, width=width, label='Issue-Comments')

    ax.set_xticks(xAxis)
    ax.set_xticklabels(names, rotation=30, ha='right')
    ax.set_xlabel('Name', fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel('Contributions', fontsize=LABEL_FONT_SIZE)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Individual Contributions', fontsize=TITLE_FONT_SIZE)
    ax.tick_params(labelsize=TICK_FONT_SIZE)
    ax.legend(fontsize=LEGEND_FONT_SIZE)

    plt.tight_layout()
    plt.savefig('chart_2_individual_contributions.png', dpi=150)
    plt.close()

def filesChanged(names, files):
    fig, ax = plt.subplots(figsize=(16, 9), layout='tight')
    ax.bar(names, files, label='Files Changed')

    ax.set_xticklabels(names, rotation=30, ha='right')
    ax.set_xlabel('Name', fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel('Files Changed', fontsize=LABEL_FONT_SIZE)
    ax.set_title('Files Changed by Each Member', fontsize=TITLE_FONT_SIZE)
    ax.tick_params(labelsize=TICK_FONT_SIZE)

    plt.tight_layout()
    plt.savefig('chart_3_files_changed.png', dpi=150)
    plt.close()

def locChanged(names, loc):
    fig, ax = plt.subplots(figsize=(16, 9), layout='tight')
    ax.bar(names, loc, label='LOC Changed', log=True)

    ax.set_xticklabels(names, rotation=30, ha='right')
    ax.set_xlabel('Name', fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel('Lines of Code Changed', fontsize=LABEL_FONT_SIZE)
    ax.set_title('Lines of Code Changed by Each Member', fontsize=TITLE_FONT_SIZE)
    ax.tick_params(labelsize=TICK_FONT_SIZE)

    plt.tight_layout()
    plt.savefig('chart_4_loc_changed.png', dpi=150)
    plt.close()

if __name__ == '__main__':
    with open('chart_data.json', 'r') as file:
        chart_data = json.load(file)

    names = [userdata['Name'] for userdata in chart_data.values()]
    prs_dates = [userdata['PR Dates'] for userdata in chart_data.values()]
    prs = [userdata['PR Count'] for userdata in chart_data.values()]
    reviews = [userdata['PR Reviews'] for userdata in chart_data.values()]
    issues = [userdata['Issue Count'] for userdata in chart_data.values()]
    comments = [userdata['Issue Comments'] for userdata in chart_data.values()]
    files = [userdata['Files Changed'] for userdata in chart_data.values()]
    loc = [userdata['LOC Changed'] for userdata in chart_data.values()]

    githubActivity(names, prs_dates)
    memberContributions(names, prs, reviews, issues, comments)
    filesChanged(names, files)
    locChanged(names, loc)
