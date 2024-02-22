import xmltodict
import json
import pandas as pd
import os
import ast
from line_profiler import LineProfiler
import functools
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

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
    file_list = [file for file in os.listdir(folder_path) if file.endswith(".xml")]
    print("Total XML Files:", len(file_list))
    with tqdm(total=len(file_list)) as pbar:
        for file in file_list:
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
            pbar.update(1)
    df = pd.DataFrame(data, columns=keys_data)
    return df

def str_to_dict(string):
    if isinstance(string, str):
        dict_str = string.replace("OrderedDict([", "").replace("])", "")
        return ast.literal_eval(dict_str)
    else:
        return None

def preprocess(df) -> pd.DataFrame:
    """
    args: data: pd.DataFrame
    returns: pd.DataFrame

    Preprocess the data
    """
    df['Institution'] = df['Institution'].apply(str_to_dict)
    df['AwardInstrument'] = df['AwardInstrument'].apply(str_to_dict)
    df['Organization'] = df['Organization'].apply(str_to_dict)
    df['Organization'] = df['Organization'].apply(str_to_dict)
    df['Investigator'] = df['Investigator'].apply(str_to_dict)
    df['Performance_Institution'] = df['Performance_Institution'].apply(str_to_dict)
    df['ProgramElement'] = df['ProgramElement'].apply(str_to_dict)
    df['ProgramOfficer'] = df['ProgramOfficer'].apply(str_to_dict)

    df['Appropriation'] = df['Appropriation'].apply(lambda x: str_to_dict(x) if x is not None else None)
    df['Fund'] = df['Fund'].apply(lambda x: str_to_dict(x) if x is not None else None)
    df['ProgramReference'] = df['ProgramReference'].apply(lambda x: str_to_dict(x) if x is not None else None)
    df['AwardInstrument'] = df['AwardInstrument'].apply(lambda x: x['Value'] if x is not None else None)
    df['AwardEffectiveDate'] = pd.to_datetime(df['AwardEffectiveDate'])
    df['AwardExpirationDate'] = pd.to_datetime(df['AwardExpirationDate'])
    df['MinAmdLetterDate'] = pd.to_datetime(df['MinAmdLetterDate'])
    df['MaxAmdLetterDate'] = pd.to_datetime(df['MaxAmdLetterDate'])
    return df

def main() -> None:
    sample_file = r'/media/notorious/AdityaExtDI/data/1351716.xml'
    folder_path = r'/media/notorious/AdityaExtDI/data/'
    keys_data = getKeys(sample_file)
    print("################## Converting XML to CSV ##############################")
    df = getDFOptimized(folder_path, keys_data)
    print("################# CSV File Created ##############################")
    df = preprocess(df)
    print("################ preprocessing done ##############################")
    df.to_csv('data.csv')
    print("################ CSV File Saved ##############################")
    df = pd.read_csv('data.csv')
   


if __name__ == '__main__':
    main()