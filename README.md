
# MA705 Final Project

This repository contains files used in the MA705 dashboard project.

The final dashboard is deployed on Heroku [here](https://ma705bostonuniversities.herokuapp.com).

## Dashboard Description

This dashboard uses live API to convert USD to any foreign currency and provides trends of the 
last 3 years for major currency conversions against the USD.

### Data Sources

Brief description of where/how you got the data and how it was processed.

- http://api.currencylayer.com/
Live API to convert USD to 167 other currencies
Two components were combined in order to create the drop down menu and obtain rates 
Note: There is a cap on 250 requests

- https://www.ofx.com/en-us/forex-news/historical-exchange-rates/
Created a CSV in order to get the data, then used it to graph.

