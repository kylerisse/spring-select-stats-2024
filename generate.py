#!/usr/bin/env python3

import csv
import datetime
import os
import jinja2

divisions = [
    "12ub",
    "12ug",
    "14ub",
    "14ug",
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
        deductions[team] = {
            'sendoffs': 0,
            'reporting': 0,
        }
    for row in reader:
        if len(row) != 3:
            print(f'bad row in {file} {str(row)}')
            exit(1)
        if row[0] not in teams:
            print(f'invalid team name in {file} {str(row)}')
            exit(1)
        deductions[row[0]] = {
            'sendoffs': int(row[1]),
            'reporting': int(row[2]),
        }
    return deductions

def parse_schedule(schedule, teams):
    pastSchedule = []
    futureSchedule = []
    for row in schedule:
        if len(row) == 5:
            pastSchedule.append([row[0], row[1], row[2], int(row[3]), int(row[4])])
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
        if row[3] == row[4]:
            ties += 1
    return round(ties / total, 2)

def gender(division):
    if division[-1] == 'b':
        return 'male'
    if division[-1] == 'g':
        return 'female'
    return 'coed'

def write_file(division, teams, deductions, schedule):
    pastSchedule, futureSchedule = parse_schedule(schedule, teams)
    outfile = f'output_{ '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) }_{ division }.txt'
    PWD = os.path.dirname(os.path.abspath(__file__))
    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(PWD))
    text = j2_env.get_template('template.j2').render(
        division=division,
        gender=gender(division),
        teams=teams,
        deductions=deductions,
        tiepct=calc_tiepct(pastSchedule),
        pastSchedule=pastSchedule,
        futureSchedule=futureSchedule,
    )
    try:
        fh = open(outfile, 'w')
        fh.write(text)
        fh.close()
    except:
        print(f'could not write to {outfile}')
        exit(1)
    print(f'\n email body written to { outfile }')

def main():
    for division in divisions:
        schedule = read_schedule(f'./schedules/{division}_schedule.csv')
        teams = extract_teams(schedule)
        deductions = read_deductions(teams, f'./schedules/{division}_deductions.csv')
        write_file(division, teams, deductions, schedule)

if __name__ == "__main__":
    main()
