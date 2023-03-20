# Vaxtrac

Vaxtrac is an application for managing the task of staying healthy with preventative immunizations.

## Features
- Add and track completed immunizations, dates of administration, and reactions
<br><br>

- Learn about currently available vaccines with information from openFDA and [Drugs.com]

<br><br>

## Demo
Click [here](https://youtu.be/zHuDHg2AnZQ) to view the Vaxtrac demo video!
<br><br>

## Tech Stack
Category | Tech
--- | --- 
**Backend** | [Python], [Flask], [Postgresql], [SQLAlchemy]
**Frontend** | [JavaScript], [HTML], [CSS], [Bootstrap]
**API** | openFDA [NDC_lookup], CDC Vaccine [Provider_locations]
**Libraries** | [Pandas], [Chart.js], [D3.js]
**Other** | [BeautifulSoup], [Jinja], [Drugs.com], [FluView], [Canva]

## Installation

To begin, clone this repository to your local machine.
```sh
git clone https://github.com/ershams/Vaxtrac.git
```

After cloning, use your CLI to navigate to the project root directory and initialize a virtual environment.
```sh
virtualenv venv
source venv/bin/activate
```

Once in the virtual environment, install all required depenencies.
```sh
pip3 install -r requirements.txt
```

Next, create and seed a database for the project. You will need [PostgreSQL] installed for this.
```sh
python3 seed_database.py
```
Finally, start the server to launch Vaxtrac.
```sh
python3 server.py
```

## Author
Eusra Shams | *[Github], [Linkedin]*


[Drugs.com]: <https://www.drugs.com/>
[Python]: <https://www.python.org/>
[Flask]: <https://flask.palletsprojects.com/en/2.1.x/>
[Postgresql]: <https://www.postgresql.org/>
[SQLAlchemy]: <https://www.sqlalchemy.org/>
[JavaScript]: <https://developer.mozilla.org/en-US/docs/Web/JavaScript>
[HTML]: <https://developer.mozilla.org/en-US/docs/Web/HTML>
[CSS]: <https://developer.mozilla.org/en-US/docs/Web/CSS>
[Bootstrap]: <https://getbootstrap.com/>
[FluView]: <https://www.cdc.gov/flu/weekly/fluviewinteractive.htm>
[Provider_locations]: <https://data.cdc.gov/resource/5jp2-pgaw.json>
[Pandas]: <https://pandas.pydata.org/>
[Chart.js]: <https://www.chartjs.org/docs/latest/getting-started/>
[D3]: <https://d3js.org/>
[BeautifulSoup]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
[Jinja]: <https://jinja.palletsprojects.com/en/3.1.x/>
[Github]: <https://github.com/ershams>
[Linkedin]: <https://www.linkedin.com/in/eusra-shams/>
[Canva]: <https://www.canva.com/>
