"""This file contains org parser and analyser
"""
import json
from datetime import datetime,timedelta
import pandas as pd
from orgparse import load


def item2dict(item):
    """
    convert org node to dict
    """
    try:
        result = {
            "name":item.heading,
            "tag":list(item.tags)[0],
            "start_time":item.clock[0].start,
            "end_time":item.clock[0].end,
            "duration":item.clock[0].duration
        }
        return result
    except Exception as e:
        """
        find out which one is wrong
        """
        print(item)
        print(e)

def org2df(root):
    """
    convert org root node to pandas dataframe
    """
    days = root.children
    item_nodes = []
    for day in days:
        item_nodes += day.children
    return pd.DataFrame([item2dict(item) for item in item_nodes])[['name','duration','start_time','end_time','tag']]

def org_path2df(path):
    """
    convert path of org file to pandas dataframe
    """
    root = load(path)
    df = org2df(root)
    return df

def get_org_df():
    """
    get pandas dataframe from org path
    """
    org_path = "/home/mark/code/org_time_record/2018.org"
    org_df = org_path2df(org_path)
    return org_df

def get_this_week(df,now):
    """
    get dataframe start_time >= one week ago and end_time <= now
    """
    one_week_ago = now - timedelta(weeks=1)
    now = now.replace(hour=23,minute=59,second=0)
    one_week_ago = one_week_ago.replace(hour=0,minute=0,second=0)
    df = df[(df.start_time>=one_week_ago)&(df.end_time<=now)]
    return df


def main():
    df = get_org_df()
    now  = datetime.now()
    this_week = get_this_week(df,now)
    print(this_week)

if __name__ == '__main__':
    main()
