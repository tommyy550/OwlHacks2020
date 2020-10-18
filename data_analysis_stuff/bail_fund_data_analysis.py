# -*- coding: utf-8 -*-
"""bail_fund_data_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tJfDdaULM5RBvWB01Wl34geLyMSe1FLA
"""

!pip3 install pandas==1.0.5
!pip install pandasql
!pip install googledrivedownloader

import pandas as pd
print(pd.__version__ == '1.0.5')

import numpy as np
from matplotlib.pyplot as plt
import seaborn as sns
import pandasql as ps
import ast
import datetime
import time
from datetime import date

from google.colab import drive
drive.mount('/content/drive')

philly_bail_df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/parsed1.csv")
vermont_bail_df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/arraignment_data_2019_5_30.csv")
philly_bail_df
vermont_bail_df

philly_bail_df

philly_bail_df.dtypes

monetary_bail_judge_df = ps.sqldf('''
  SELECT bail_set_by AS magistrate, AVG(bail_amount) AS average_bail_amount, count(*) AS bail_count
  FROM philly_bail_df
  WHERE bail_type = "Monetary"
  GROUP BY bail_set_by
  HAVING bail_count > 10
  ORDER BY average_bail_amount
'''
, locals())

monetary_bail_judge_df

plt.figure('Bail Amount By Magistrate')
plt.title('Average Bail Amount by Magistrate')
plt.ylabel('Magistrate')
plt.xlabel('Average Bail Amount ($)')
plt.barh(y=monetary_bail_judge_df['magistrate'], width=monetary_bail_judge_df['average_bail_amount'], color='purple')
plt.savefig('/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/amount_by_magistrate')

monetary_bail_zip_query = '''
  SELECT zip AS zipcode, AVG(bail_amount) AS average_bail_amount, count(*) AS bail_count
  FROM philly_bail_df
  GROUP BY zip
  HAVING bail_count > 100
  ORDER BY average_bail_amount DESC
'''
monetary_bail_zip_df = ps.sqldf(monetary_bail_zip_query, locals())
monetary_bail_zip_df

philly_average_bail_amount = ps.sqldf('''
  SELECT AVG(bail_amount) AS philly_average_bail_amount
  FROM philly_bail_df
  WHERE bail_type = 'Monetary'
''', locals())
print(philly_average_bail_amount)

vermont_average_bail_amount = ps.sqldf('''
  SELECT AVG(bail_amount) AS vermont_average_bail_amount
  FROM vermont_bail_df
  WHERE bail_types = 'Bail'
''', locals())
print(vermont_average_bail_amount)

plt.figure('philly_vs_vermont')
plt.title('Average Bail Amount in Philadelphia vs Vermont')
plt.xlabel('Location')
plt.ylabel('Average Bail Amount ($)')
plt.ylim(0, 120000)
plt.bar(x=['Philadelphia', 'Vermont'], height=[99400, 4428], \
        width = 0.3, color='lightcoral')
plt.savefig('/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/amount_philly_vs_vermont')

for x,y in zip(['Philadelphia', 'Vermont'],[99400, 4428]):
    label = y
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')
plt.show()

date_df = philly_bail_df[['arrest_dt','bail_amount','bail_type']].dropna()
date_df['arrest_dt'] = date_df['arrest_dt'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%y'))
date_df['month'] = pd.DatetimeIndex(date_df['arrest_dt']).month
date_df['year'] = pd.DatetimeIndex(date_df['arrest_dt']).year
bail_by_month_df = ps.sqldf('''
SELECT year, month, COUNT(*) AS TotalCount, AVG(bail_amount) AS average_bail_amount
FROM date_df
WHERE bail_type = 'Monetary' and year = 2020
GROUP BY month
ORDER BY month
''', locals())

plt.figure('Bail Amount By Month')
plt.xlabel('Month of year 2020')
plt.ylabel('Average Bail Amount ($)')
plt.title('Average Bail Amount by Month')
plt.ylim(0,200000)
plt.plot(bail_by_month_df['month'], bail_by_month_df['average_bail_amount'], color='teal')
plt.savefig('/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/amount_by_month')

def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - \
         ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age

age_df = philly_bail_df[['dob','bail_amount','bail_type']].dropna()
age_df['age'] = age_df['dob'].apply(lambda x: calculateAge(datetime.datetime.strptime(x, '%m/%d/%y')))
age_df

bail_amount_by_age_df = ps.sqldf('''
  SELECT ABS(age) as Age, AVG(bail_amount) AS average_bail_amount, count(*) AS bail_count
  FROM age_df
  WHERE bail_type = "Monetary"
  GROUP BY ABS(age)
  ORDER BY Age
'''
, locals())


plt.figure('Bail Amount By Age')
plt.title('Average Bail Amount by Age')
plt.xlabel('Age')
plt.ylabel('Average Bail Amount ($)')
plt.bar(x=bail_amount_by_age_df['Age'], height=bail_amount_by_age_df['average_bail_amount'], width = 0.5, color='lightblue')
plt.savefig('/content/drive/My Drive/Colab Notebooks/2020 OwlHacks Bail Fund Project/amount_by_age')

bail_amount_by_age_df.sort_values('average_bail_amount', ascending=False)

from google.colab import drive
drive.mount('/content/drive')



