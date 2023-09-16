# Pandas DataFrame

This notebook goes over how to load data from a [pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html) DataFrame.


```python
#!pip install pandas
```


```python
import pandas as pd
```


```python
df = pd.read_csv("example_data/mlb_teams_2012.csv")
```


```python
df.head()
```



```
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>"Payroll (millions)"</th>
      <th>"Wins"</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Nationals</td>
      <td>81.34</td>
      <td>98</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Reds</td>
      <td>82.20</td>
      <td>97</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Yankees</td>
      <td>197.96</td>
      <td>95</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Giants</td>
      <td>117.62</td>
      <td>94</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Braves</td>
      <td>83.31</td>
      <td>94</td>
    </tr>
  </tbody>
</table>
</div>
```



```python
from langchain.document_loaders import DataFrameLoader
```


```python
loader = DataFrameLoader(df, page_content_column="Team")
```


```python
loader.load()
```




    [Document(page_content='Nationals', metadata={' "Payroll (millions)"': 81.34, ' "Wins"': 98}),
     Document(page_content='Reds', metadata={' "Payroll (millions)"': 82.2, ' "Wins"': 97}),
     Document(page_content='Yankees', metadata={' "Payroll (millions)"': 197.96, ' "Wins"': 95}),
     Document(page_content='Giants', metadata={' "Payroll (millions)"': 117.62, ' "Wins"': 94}),
     Document(page_content='Braves', metadata={' "Payroll (millions)"': 83.31, ' "Wins"': 94}),
     Document(page_content='Athletics', metadata={' "Payroll (millions)"': 55.37, ' "Wins"': 94}),
     Document(page_content='Rangers', metadata={' "Payroll (millions)"': 120.51, ' "Wins"': 93}),
     Document(page_content='Orioles', metadata={' "Payroll (millions)"': 81.43, ' "Wins"': 93}),
     Document(page_content='Rays', metadata={' "Payroll (millions)"': 64.17, ' "Wins"': 90}),
     Document(page_content='Angels', metadata={' "Payroll (millions)"': 154.49, ' "Wins"': 89}),
     Document(page_content='Tigers', metadata={' "Payroll (millions)"': 132.3, ' "Wins"': 88}),
     Document(page_content='Cardinals', metadata={' "Payroll (millions)"': 110.3, ' "Wins"': 88}),
     Document(page_content='Dodgers', metadata={' "Payroll (millions)"': 95.14, ' "Wins"': 86}),
     Document(page_content='White Sox', metadata={' "Payroll (millions)"': 96.92, ' "Wins"': 85}),
     Document(page_content='Brewers', metadata={' "Payroll (millions)"': 97.65, ' "Wins"': 83}),
     Document(page_content='Phillies', metadata={' "Payroll (millions)"': 174.54, ' "Wins"': 81}),
     Document(page_content='Diamondbacks', metadata={' "Payroll (millions)"': 74.28, ' "Wins"': 81}),
     Document(page_content='Pirates', metadata={' "Payroll (millions)"': 63.43, ' "Wins"': 79}),
     Document(page_content='Padres', metadata={' "Payroll (millions)"': 55.24, ' "Wins"': 76}),
     Document(page_content='Mariners', metadata={' "Payroll (millions)"': 81.97, ' "Wins"': 75}),
     Document(page_content='Mets', metadata={' "Payroll (millions)"': 93.35, ' "Wins"': 74}),
     Document(page_content='Blue Jays', metadata={' "Payroll (millions)"': 75.48, ' "Wins"': 73}),
     Document(page_content='Royals', metadata={' "Payroll (millions)"': 60.91, ' "Wins"': 72}),
     Document(page_content='Marlins', metadata={' "Payroll (millions)"': 118.07, ' "Wins"': 69}),
     Document(page_content='Red Sox', metadata={' "Payroll (millions)"': 173.18, ' "Wins"': 69}),
     Document(page_content='Indians', metadata={' "Payroll (millions)"': 78.43, ' "Wins"': 68}),
     Document(page_content='Twins', metadata={' "Payroll (millions)"': 94.08, ' "Wins"': 66}),
     Document(page_content='Rockies', metadata={' "Payroll (millions)"': 78.06, ' "Wins"': 64}),
     Document(page_content='Cubs', metadata={' "Payroll (millions)"': 88.19, ' "Wins"': 61}),
     Document(page_content='Astros', metadata={' "Payroll (millions)"': 60.65, ' "Wins"': 55})]




```python

```
