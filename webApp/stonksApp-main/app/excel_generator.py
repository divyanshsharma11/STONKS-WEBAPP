from pandas_datareader import data as dreader
import os
import shutil
from datetime import datetime


def generateCsv(user_name, stock):

    directory = user_name
    parent_dir = "./app/static"
    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)

    except:
        print("folder present")

    print("Directory '% s' created" % directory)

    end = datetime.today()

    dreader.DataReader(f'{stock}', 'yahoo', '2010-01-01',
                       end).to_excel(f'./app/static/{directory}/'+f'{stock}'+'.xlsx')


def deleteFolder(user_name):

    print(f"trying to delete folder {user_name}")
    try:
        shutil.rmtree(f'./app/static/{user_name}')

    except:
        print("file does not exist")
