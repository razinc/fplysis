# Introduction
<p align="center">
  <img src="image/banner.png" width="500">
</p>

<p align="center">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Make better calls in [Fantasy Premier League](https://fantasy.premierleague.com/). 

# The Zen of FPL
* Fixtures over form.
* Transfers are precious. 
* Ignore price rises.
* Avoid confirmation of bias.
* Luck is a factor.
* Utilise xG data.

Read Fabio Forges full interview [here](https://fantasyfootballcommunity.com/tips-from-the-worlds-best-fpl-manager/).

# Features
* `analysis_league.py` is unavailable right now.
* `analysis_team.py` is used to track your team performance and suggest players which you should buy.
* `analysis_top_10k.py` is used to track which players is owned by top 10K managers.

# Installation
`fplysis` uses `poetry` for dependacies management. To install all of them:
```bash
poetry install
```

# Credentials
All credentials are stored in `fpl_credentials.py` using below format. This is required for `analysis_league.py` and `analysis_top_10k.py` where login is required to access league's data. You can use `analysis_team.py` with or without credentials. With credentials, you will get the latest team and money in the banks.
```python
EMAIL = ""
PASSWORD = ""
```

You can view sample outputs of each script in section below.

# Usage
Enter virtual environment:
```bash
poetry shell
```
Or you can use `poetry run` before any script:
```bash
poetry run python analysis_top_10k.py
```
Each of available scripts have a simple guide on how to use them by adding `-h` switch.
```bash
poetry run python analysis_team.py -h
```

# Sample Output
**Warning**: These samples might be outdated but you can still get the idea on what each script does.
* `analysis_team.py`
<p align="center">
  <img src="image/analysis_team_sample.png" width="1000">
</p>

* `analysis_top_10k.py`
<p align="center">
  <img src="image/analysis_top_10k_sample.png" width="1000">
</p>

# Miscellaneous
[Additional resources](https://fplform.com/fpl-resources#fpl-data-tools).
