from __future__ import annotations

import pandas as pd  # remember to install the package pandas! (my version is 2.2.1)

olympics = pd.read_csv("summer.csv")
olympics = olympics.dropna()
# Renamed some sports to have consistent names
olympics.loc[olympics['Discipline'] == 'Beach volley.', 'Discipline'] = 'Beach Volleyball'
olympics.loc[olympics['Discipline'] == 'BMX', 'Discipline'] = 'Cycling BMX'
olympics.loc[olympics['Discipline'] == 'Modern Pentath.', 'Discipline'] = 'Modern Pentathlon'
olympics.loc[olympics['Discipline'] == 'Artistic G.', 'Discipline'] = 'Gymnastics Artistic'
olympics.loc[olympics['Discipline'] == 'Rhythmic G.', 'Discipline'] = 'Gymnastics Rhythmic'
olympics.loc[olympics['Discipline'] == 'Synchronized S.', 'Discipline'] = 'Synchronized Swimming'
olympics.loc[olympics['Discipline'] == 'Water polo', 'Discipline'] = 'Water Polo'
olympics.loc[olympics['Discipline'] == 'Wrestling Free.', 'Discipline'] = 'Wrestling Freestyle'
olympics.loc[olympics['Discipline'] == 'Water Motorspor', 'Discipline'] = 'Water Motorsport'
# Rename countries to be consistent with country_codes
olympics.loc[olympics['Country'] == 'GRE', 'Country'] = 'GRC'
olympics.loc[olympics['Country'] == 'GER', 'Country'] = 'DEU'
olympics.loc[olympics['Country'] == 'DEN', 'Country'] = 'DNK'
olympics.loc[olympics['Country'] == 'SUI', 'Country'] = 'CHE'
olympics.loc[olympics['Country'] == 'NED', 'Country'] = 'NLD'
olympics.loc[olympics['Country'] == 'RSA', 'Country'] = 'ZAF'
olympics.loc[olympics['Country'] == 'POR', 'Country'] = 'PRT'
olympics.loc[olympics['Country'] == 'URU', 'Country'] = 'URY'
olympics.loc[olympics['Country'] == 'HAI', 'Country'] = 'HTI'
olympics.loc[olympics['Country'] == 'PHI', 'Country'] = 'PHL'
olympics.loc[olympics['Country'] == 'CHI', 'Country'] = 'CHL'
olympics.loc[olympics['Country'] == 'LAT', 'Country'] = 'LVA'
olympics.loc[olympics['Country'] == 'SRI', 'Country'] = 'LKA'
olympics.loc[olympics['Country'] == 'PUR', 'Country'] = 'PRI'
olympics.loc[olympics['Country'] == 'IRI', 'Country'] = 'IRN'
olympics.loc[olympics['Country'] == 'TRI', 'Country'] = 'TTO'
olympics.loc[olympics['Country'] == 'BUL', 'Country'] = 'BGR'
olympics.loc[olympics['Country'] == 'LIB', 'Country'] = 'LBN'
olympics.loc[olympics['Country'] == 'BAH', 'Country'] = 'BHS'
olympics.loc[olympics['Country'] == 'SIN', 'Country'] = 'SGP'
olympics.loc[olympics['Country'] == 'NGR', 'Country'] = 'NGA'
olympics.loc[olympics['Country'] == 'MGL', 'Country'] = 'MNG'
olympics.loc[olympics['Country'] == 'NIG', 'Country'] = 'NER'
olympics.loc[olympics['Country'] == 'BER', 'Country'] = 'BMU'
olympics.loc[olympics['Country'] == 'TAN', 'Country'] = 'TZA'
olympics.loc[olympics['Country'] == 'ZIM', 'Country'] = 'ZWE'
olympics.loc[olympics['Country'] == 'ZAM', 'Country'] = 'ZMB'
olympics.loc[olympics['Country'] == 'ALG', 'Country'] = 'DZA'
olympics.loc[olympics['Country'] == 'CRC', 'Country'] = 'CRI'
olympics.loc[olympics['Country'] == 'INA', 'Country'] = 'IDN'
olympics.loc[olympics['Country'] == 'ISV', 'Country'] = 'VGB'
olympics.loc[olympics['Country'] == 'EUN', 'Country'] = 'URS'  # Actually 2 different team but still in Soviet
olympics.loc[olympics['Country'] == 'MAS', 'Country'] = 'MYS'
olympics.loc[olympics['Country'] == 'CRO', 'Country'] = 'HRV'
olympics.loc[olympics['Country'] == 'SLO', 'Country'] = 'SVK'
olympics.loc[olympics['Country'] == 'TGA', 'Country'] = 'TON'
olympics.loc[olympics['Country'] == 'BAR', 'Country'] = 'BRB'
olympics.loc[olympics['Country'] == 'KSA', 'Country'] = 'SAU'
olympics.loc[olympics['Country'] == 'KUW', 'Country'] = 'KWT'
olympics.loc[olympics['Country'] == 'VIE', 'Country'] = 'VNM'
olympics.loc[olympics['Country'] == 'PAR', 'Country'] = 'PRY'
olympics.loc[olympics['Country'] == 'UAE', 'Country'] = 'ARE'
olympics.loc[olympics['Country'] == 'SUD', 'Country'] = 'SDN'
olympics.loc[olympics['Country'] == 'MRI', 'Country'] = 'MUS'
olympics.loc[olympics['Country'] == 'TOG', 'Country'] = 'TGO'
olympics.loc[olympics['Country'] == 'GUA', 'Country'] = 'GTM'
olympics.loc[olympics['Country'] == 'GRN', 'Country'] = 'GRD'
olympics.loc[olympics['Country'] == 'BOT', 'Country'] = 'BWA'

# Convert back to a new csv file
olympics.to_csv('summer_modified.csv')


country_codes = pd.read_csv("country_codes.csv")
country_codes = country_codes[['Region Name_en (M49)', 'Country or Area_en (M49)', 'ISO-alpha3 Code (M49)']]
country_codes = country_codes.dropna()
country_codes.reset_index(inplace=True, drop=True)
country_codes.loc[len(country_codes.index)] = ['World', 'International Olympic Committee Mixed teams', 'ZZX']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Bohemia', 'BOH']
country_codes.loc[len(country_codes.index)] = ['Oceania', 'Australasia', 'ANZ']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Russian Empire', 'RU1']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Czechoslovakia', 'TCH']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Yugoslavia', 'YUG']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Soviet Union', 'URS']
country_codes.loc[len(country_codes.index)] = ['Europe', 'United Team of Germany', 'EUA']
country_codes.loc[len(country_codes.index)] = ['Americas', 'British West Indies', 'BWI']
country_codes.loc[130] = ['Asia', 'Chinese Taipei', 'TPE']
country_codes.loc[len(country_codes.index)] = ['Europe', 'East Germany', 'GDR']
country_codes.loc[len(country_codes.index)] = ['Europe', 'West Germany', 'FRG']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Netherlands Antilles', 'AHO']
country_codes.loc[len(country_codes.index)] = ['World', 'Independent Olympic Participants', 'IOP']
country_codes.loc[len(country_codes.index)] = ['Europe', 'Serbia and Montenegro', 'SCG']

# Convert back to a new csv file
country_codes.to_csv('country_codes_modified.csv')

small_olympics = pd.read_csv("summer_modified.csv")
small_olympics = small_olympics.iloc[0:50,]
small_olympics = small_olympics.drop(['Unnamed: 0'], axis=1)
small_olympics.to_csv("summer_small.csv")
