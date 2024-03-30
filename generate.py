#!/usr/bin/env python3

import csv
#import datetime
#import os
#import jinja2

divisions = [
    "12ug"
]

def read_schedule(file):
    try:
        fh = open(file, 'r')
    except:
        print(f'cannot open {file}')
        exit(1)
    reader = csv.reader(filter(lambda row: row[0] != '#' and row[0] != '\n', fh))
    schedule = []
    for row in reader:
        if len(row) not in [3, 5]:
            print(f'bad row in {file} {str(row)}')
            exit(1)
        schedule.append(row)
    fh.close()
    return schedule

def extract_teams(schedule):
    teams = []
    for row in schedule:
        if row[1] not in teams:
            teams.append(row[1])
        if row[2] not in teams:
            teams.append(row[2])
    return teams

def read_deductions(teams, file):
    try:
        fh = open(file, 'r')
    except:
        print(f'cannot open {file}')
        exit(1)
    reader = csv.reader(filter(lambda row: row[0] != '#' and row[0] != '\n', fh))

    deductions = {}
    for team in teams:
        deductions[team] = 0

    for row in reader:
        if len(row) != 2:
            print(f'bad row in {file} {str(row)}')
            exit(1)
        if row[0] not in teams:
            print(f'invalid team name in {file} {str(row)}')
            exit(1)
        deductions[row[0]] = int(row[1])
    return deductions

def parse_schedule(schedule, teams):
    pastSchedule = []
    futureSchedule = []
    for row in schedule:
        if len(row) == 5:
            pastSchedule.append(row)
        if len(row) == 3:
            futureSchedule.append(row)
        if len(row) not in [3, 5]:
            print(f'invalid row in schedule {str(row)}')
            exit(1)
    return pastSchedule, futureSchedule

def calc_tiepct(pastSchedule):
    total = len(pastSchedule)
    ties = 0
    for row in pastSchedule:
        if int(row[3]) == int(row[4]):
            ties += 1
    return round(ties / total, 2)

def gender(division):
    if division[-1] == 'b':
        return 'male'
    if division[-1] == 'g':
        return 'female'
    return 'coed'

def main():
    for division in divisions:
        schedule = read_schedule(f'./schedules/{division}_schedule.csv')
        teams = extract_teams(schedule)
        deductions = read_deductions(teams, f'./schedules/{division}_deductions.csv')
        pastSchedule, futureSchedule = parse_schedule(schedule, teams)
        tiepct = calc_tiepct(pastSchedule)

        # debug
        print(f'{gender(division)}')
        print(f'{schedule}')
        print(f'{teams}')
        print(f'{deductions}')
        print(f'{pastSchedule}')
        print(f'{futureSchedule}')
        print(f'{tiepct}')

    #outfile = "output_{:%Y%m%d-%H%M%S}".format(datetime.datetime.now())
    #schedule = readSchedule(scheduleFile)
    #teams = extractTeams(schedule)
    #matches, tiepct = generateMatches(schedule)
    #writeFile(teams, matches, tiepct, outfile)

if __name__ == "__main__":
    main()
