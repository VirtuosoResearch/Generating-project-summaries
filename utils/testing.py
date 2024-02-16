"""
Run this file to compare previous version of getDF function used to convert XML file to Pandas Dataframe with getDFOptimized function which is significantly faster
"""

import xmltodict
import json
import pandas as pd
import os
import ast
from line_profiler import LineProfiler
import functools
import time
import matplotlib.pyplot as plt

def profile_function(func):
    @functools.wraps(func)
    def profiled_function(*args, **kwargs):
        profiler = LineProfiler()
        profiler.add_function(func)
        profiler.enable_by_count()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        profiler.disable_by_count()
        profiler.print_stats()
        total_time = end_time - start_time
        return result, total_time
    
    return profiled_function


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

@profile_function
def getDF(folder_path,keys_data)->pd.DataFrame:
    counter=0
    df = pd.DataFrame(columns=list(keys_data))
    for file in os.listdir(folder_path):
        if file.endswith(".xml"):
            with open(folder_path+file, encoding='utf-8') as f:
                xml_data = f.read()
                try:
                    xml_dict = xmltodict.parse(xml_data)
                    labels = []
                    for i in keys_data:
                        labels.append(xml_dict['rootTag']['Award'][i] if i in xml_dict['rootTag']['Award'] else None)
#                     print(file, ' ----> ', len(labels))
                    df.loc[counter] = labels
                    counter+=1
                except:
                    print("Error With File Name: ", file)
                    continue
    return df

@profile_function
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
    df, time_df= getDF(folder_path,keys_data)
    df_opimized, time_df_optimized = getDFOptimized(folder_path, keys_data)

    # Plotting
    plt.plot(['getDF', 'getDFOptimized'], [time_df, time_df_optimized], marker='o')
    plt.ylabel('Total Time (s)')
    plt.title('Comparison of Total Time Taken by Functions')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
