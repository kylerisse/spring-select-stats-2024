#!/usr/bin/env python3
'''
generate.py reads schedule csv files and outputs a valid sports club stats import email
'''

import csv
import datetime
import os
import sys
import jinja2

divisions = [
    "10ub",
    "10ug",
    "12ub",
    "12ug",
    "14ub",
    "14ug",
    "16ub",
    "16ug",
]

def read_schedule(file):
    '''
    read_schedule takes the path to a csv and returns a schedule as a list of lists
    each csv entry must be either a comment (#), blank line, or contain 3 or 5 fields
    '''
    schedule = []

    try:
        with open(file, 'r', encoding='utf8') as fh:

            reader = csv.reader(filter(lambda row: row[0] != '#' and row[0] != '\n', fh))

            for row in reader:
                if len(row) not in [3, 5]:
                    print(f'bad row in {file} {str(row)}')
                    sys.exit(1)
                schedule.append(row)

    except: #pylint: disable=bare-except
        print(f'cannot open {file}')
        sys.exit(1)

    return schedule

def extract_teams(schedule):
    '''
    extract_teams takes a schedule and returns a list of unique teams
    '''
    teams = []
    for row in schedule:
        if row[1] not in teams:
            teams.append(row[1])
        if row[2] not in teams:
            teams.append(row[2])
    return teams

def read_deductions(teams, file):
    '''
    read_deductions takes a team list and the path to a deductions file to populate
    the deductions list
    '''
    deductions = {}
    for team in teams:
        deductions[team] = {
            'sendoffs': 0,
            'reporting': 0,
        }
    try:
        with open(file, 'r', encoding='utf8') as fh:
            reader = csv.reader(filter(lambda row: row[0] != '#' and row[0] != '\n', fh))

            for row in reader:
                if len(row) != 3:
                    print(f'bad row in {file} {str(row)}')
                    sys.exit(1)
                if row[0] not in teams:
                    print(f'invalid team name in {file} {str(row)}')
                    sys.exit(1)
                deductions[row[0]] = {
                    'sendoffs': int(row[1]),
                    'reporting': int(row[2]),
                }
    except: #pylint: disable=bare-except
        print(f'cannot open {file}')
        sys.exit(1)

    return deductions

def parse_schedule(schedule):
    '''
    parse_schedule takes a raw schedule and returns both past (with scores) and
    future (without scores)
    '''
    past_schedule = []
    future_schedule = []
    for row in schedule:
        if len(row) == 5:
            past_schedule.append([row[0], row[1], row[2], int(row[3]), int(row[4])])
        if len(row) == 3:
            future_schedule.append(row)
        if len(row) not in [3, 5]:
            print(f'invalid row in schedule {str(row)}')
            sys.exit(1)
    return past_schedule, future_schedule

def calc_tie_percent(past_schedule):
    '''
    calc_tie_percent reads a schedule with scores and returns the percentage of ties
    '''
    total = len(past_schedule)
    ties = 0
    for row in past_schedule:
        if row[3] == row[4]:
            ties += 1
    return round(ties / total, 2) if total != 0 else 0

def gender(division):
    '''
    gender returns either male, female, or coed based on the division name
    '''
    if division[-1] == 'b':
        return 'male'
    if division[-1] == 'g':
        return 'female'
    return 'coed'

def write_file(division, teams, deductions, schedule):
    '''
    write_file renders the output from a jinja template
    '''
    past_schedule, future_schedule = parse_schedule(schedule)
    outfile = f'output_{ datetime.datetime.now():%Y%m%d-%H%M%S}_{ division }.txt'
    work_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(work_dir))
    text = j2_env.get_template('template.j2').render(
        division=division,
        gender=gender(division),
        teams=teams,
        deductions=deductions,
        tie_percent=calc_tie_percent(past_schedule),
        past_schedule=past_schedule,
        future_schedule=future_schedule,
    )
    try:
        with open(outfile, 'w', encoding='utf8') as fh:
            fh.write(text)
    except: #pylint: disable=bare-except
        print(f'could not write to {outfile}')
        sys.exit(1)
    print(f'\n email body written to { outfile }')

def main():
    '''
    main is the entrypoint
    '''
    for division in divisions:
        schedule = read_schedule(f'./schedules/{division}_schedule.csv')
        teams = extract_teams(schedule)
        deductions = read_deductions(teams, f'./schedules/{division}_deductions.csv')
        write_file(division, teams, deductions, schedule)

if __name__ == "__main__":
    main()
