from datetime import datetime, timedelta
import json
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Project start date - uses the week first PR made by our group
# Weeks start on Tuesdays b/c Final presentation is on Tuesday
projectStart = datetime(2025, 3, 4)
weekCount = list(range(1, ((datetime.today() - projectStart).days // 7) + 1))

def githubActivity(names, prs):
    fig, ax = plt.subplots()

    # Process data - Convert dates to weeks relative to and get count of prs 
    for i, userdata in enumerate(prs):
        for j, date in enumerate(prs[i]):
            prs[i][j] = date.split('T')[0]
            prs[i][j] = ((datetime.strptime(prs[i][j], '%Y-%m-%d') - projectStart).days // 7) + 1
        prs[i] = Counter(prs[i])
        weeklyCount = [prs[i].get(week, 0) for week in weekCount]
        ax.plot(weekCount, weeklyCount, label=names[i])

    ax.set_xlabel('Week')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel('Pull Requests')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Weekly PR Activity')
    ax.legend()
    plt.show()

def memberContributions(names, prs, reviews, issues, comments):
    fig, ax = plt.subplots()
    xAxis = np.arange(len(names))
    width = 0.2

    ax.bar(xAxis-(1.5*width), prs, width=width, label='PRs')
    ax.bar(xAxis-(width/2), reviews, width=width, label='PR-Reviews')
    ax.bar(xAxis+(width/2), issues, width=width, label='Issues')
    ax.bar(xAxis+(1.5*width), comments, width=width, label='Issue-Comments')

    ax.set_xticks(xAxis, names)
    ax.set_xlabel('Name')
    ax.set_ylabel('Contributions')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Individual Contributions')
    plt.legend()
    plt.show()

def filesChanged(names, files):
    fig, ax = plt.subplots()
    ax.bar(names, files, label='Files Changed')

    ax.set_xlabel('Name')
    ax.set_ylabel('Files Changed')
    ax.set_title('Files Changed by Each Member')
    plt.show()

def locChanged(names, loc):
    fig, ax = plt.subplots()
    ax.bar(names, loc, label='LOC Changed', log=True)

    ax.set_xlabel('Name')
    ax.set_ylabel('Lines of Code Changed')
    ax.set_title('Lines of Code Changed by Each Member')
    plt.show()

if __name__ == '__main__':
    # Get data
    with open('chart_data.json', 'r') as file:
        chart_data = json.load(file)

    # Get group member names - x data for most charts
    names = [userdata['Name'] for userdata in chart_data.values()]

    # Create chart 1 - Group's GitHub Activity
    prs = [userdata['PR Dates'] for userdata in chart_data.values()]
    # prs = [date for userdata in chart_data.values() for date in userdata['PR Dates']]
    githubActivity(names, prs)

    # Create chart 2 - Individual Contributions
    prs = [userdata['PR Count'] for userdata in chart_data.values()]
    reviews = [userdata['PR Reviews'] for userdata in chart_data.values()]
    issues = [userdata['Issue Count'] for userdata in chart_data.values()]
    comments = [userdata['Issue Comments'] for userdata in chart_data.values()]
    memberContributions(names, prs, reviews, issues, comments)

    # Create chart 3 - Files Changed
    files = [userdata['Files Changed'] for userdata in chart_data.values()]
    filesChanged(names, files)

    # Create chart 4 - Lines of Code Changed
    loc = [userdata['LOC Changed'] for userdata in chart_data.values()]
    locChanged(names, loc)
