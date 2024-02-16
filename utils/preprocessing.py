import xmltodict
import json
import pandas as pd
import os
import ast
from line_profiler import LineProfiler
import functools
import time
import matplotlib.pyplot as plt

def getKeys(file) ->list:
    """
    args: file: str
    returns: list

    Pass a sample file to get the keys of the XML file
    """
    with open(file) as f:
        xml_data = f.read()
        # Convert XML to Python dictionary
        xml_dict = xmltodict.parse(xml_data)
        keys_data = xml_dict['rootTag']['Award'].keys()
    return keys_data

def getDFOptimized(folder_path, keys_data):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".xml"):
            with open(os.path.join(folder_path, file), encoding='utf-8') as f:
                xml_data = f.read()
                try:
                    xml_dict = xmltodict.parse(xml_data)
                    labels = [xml_dict['rootTag']['Award'].get(i) for i in keys_data]
                    data.append(labels)
                except Exception as e:
                    print("Error with File Name:", file)
                    print(e)
                    continue
    df = pd.DataFrame(data, columns=keys_data)
    return df


def main() -> None:
    sample_file = r'/home/notorious/Documents/VirtuosoResearch/generating-novel-contents/Test/1351716.xml'
    folder_path = r'/home/notorious/Documents/VirtuosoResearch/generating-novel-contents/Test/'
    keys_data = getKeys(sample_file)
    df_opimized = getDFOptimized(folder_path, keys_data)
    print(df_opimized)

if __name__ == '__main__':
    main()
