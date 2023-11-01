## TradingView API

A simple python implementation for connecting to the TradingView websocket backend, and extracting ticker historical series.

### **Usage:**
```python
from TView_api import TViewAPI

tickers = ["TVC:CA10Y", 'TVC:RU10Y']
trading_view_api = TViewAPI()
data = trading_view_api.get_series(tickers)

display(data)
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
      <th>date</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>symbol</th>
      <th>country</th>
      <th>type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1985-12-31 22:00:00</td>
      <td>9.803</td>
      <td>10.378</td>
      <td>9.803</td>
      <td>10.268</td>
      <td>TVC:CA10Y</td>
      <td>CA</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1986-02-02 22:00:00</td>
      <td>10.288</td>
      <td>10.288</td>
      <td>9.753</td>
      <td>9.753</td>
      <td>TVC:CA10Y</td>
      <td>CA</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1986-03-02 22:00:00</td>
      <td>9.680</td>
      <td>9.680</td>
      <td>9.096</td>
      <td>9.096</td>
      <td>TVC:CA10Y</td>
      <td>CA</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1986-03-31 22:00:00</td>
      <td>9.016</td>
      <td>9.189</td>
      <td>8.849</td>
      <td>9.001</td>
      <td>TVC:CA10Y</td>
      <td>CA</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1986-04-30 21:00:00</td>
      <td>9.040</td>
      <td>9.226</td>
      <td>8.787</td>
      <td>9.226</td>
      <td>TVC:CA10Y</td>
      <td>CA</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>606</th>
      <td>2023-07-02 21:00:00</td>
      <td>11.190</td>
      <td>11.560</td>
      <td>11.150</td>
      <td>11.500</td>
      <td>TVC:RU10Y</td>
      <td>RU</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>607</th>
      <td>2023-07-31 21:00:00</td>
      <td>11.500</td>
      <td>12.090</td>
      <td>11.440</td>
      <td>12.030</td>
      <td>TVC:RU10Y</td>
      <td>RU</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>608</th>
      <td>2023-08-31 21:00:00</td>
      <td>12.040</td>
      <td>12.930</td>
      <td>11.980</td>
      <td>12.900</td>
      <td>TVC:RU10Y</td>
      <td>RU</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>609</th>
      <td>2023-10-01 21:00:00</td>
      <td>12.910</td>
      <td>13.360</td>
      <td>12.000</td>
      <td>12.700</td>
      <td>TVC:RU10Y</td>
      <td>RU</td>
      <td>bond</td>
    </tr>
    <tr>
      <th>610</th>
      <td>2023-10-31 21:00:00</td>
      <td>12.700</td>
      <td>12.730</td>
      <td>12.470</td>
      <td>12.520</td>
      <td>TVC:RU10Y</td>
      <td>RU</td>
      <td>bond</td>
    </tr>
  </tbody>
</table>
<p>611 rows × 8 columns</p>
</div>

