 # guide for data analysis


[![license](https://img.shields.io/github/license/:user/:repo.svg)](LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This is file to make a introduction of data analysis

data analysis folder is for data cleaning and model training. it contains three sub folders, clean_data, initial_data and model. also, several notebooks are the analysis process.

## Table of Contents

- [clean_data](#clean_data)
- [initial_data](#initial_data)
- [model](#model)
- [notebook](#notebook)
- [model_input](#model_input)
- [model_output](#model_output)
- [License](#license)

## clean_data
in this folder, it contains the csv files of cleaned data, when you run the notebooks for cleaning the initial data, the result will be stored here. 

## Background
in this folder, it contains the initial tables of data. when you run the notebooks for getting initial data from remote database, the results will be stored here. 

## model

this folder is for the training models. when the backend want to training the data, it can find model here.  

## notebook
notebooks is for the whole process. you can visit them from the first one to the last one. 

## model_input
the inputs for this model can be divided by two parts, users input and system input. user input data should be input by the user. like time, start station, end station. the other features in the modlel except for the user input is the system input. it is automatically get from the database.

## model_output
the output of this model is the predict time.


## Contributing

See [the contributing file](CONTRIBUTING.md)!

PRs accepted.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

### Any optional sections

## License

[dreamteam © botao wang](../LICENSE)
