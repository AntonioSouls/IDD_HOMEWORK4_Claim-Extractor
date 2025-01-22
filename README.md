# <div align="center"> HOMEWORK 4: CLAIM EXTRACTOR </div>
This repository contains the fourth homework assigned to us during the Data Engineering course. It was created with the aim of making public the solution that my colleague @danielluca00 and I devised and proposed to solve the tasks assigned to us by the delivery.

## - Homework Goals
In Data Science, it is not enough just to extract data from the web (as we saw in the first homework). After the Web Scraping operation carried out in the first project, in fact, specific data extracted from the Web are obtained, which, however, are in raw form. So, in addition to this extraction, it is also important to clean this data by extracting only the really informative content.
With this project, therefore, we show the solution designed to carry out this operation, which is formally called Knowledge Extraction.

## - Homework Requirements
The project is divided into three tasks:
1) From the json relating to the papers downloaded in the first homework, extract all the tables and store, for each one, all the claims present
2) Carry out a profiling of the extracted claims, that is, make an analysis of how the values of the claims are distributed, etc.
3) Align the claims, that is, understand each claim in which tables it appears


## - Description of Our Solution
### ° Task 1
Our solution starts with the creation of a Table_Converter that aims to extract all the tables from the json related to the papers downloaded in the first project. For each extracted table, we convert its HTML content into a Data-Frame through the Pandas library and store the result of this transformation in a special json file dedicated exclusively to the table. This operation allows us not only to analyze the individual tables faster, but also to be able to have a more understandable tabular format and, therefore, on which it is easier to understand how to extract the claims.
After that, you are ready to extract the claims. So, a Claim_Extractor class is created that simply queries a model (Gemini 2.0 Flash Thinking) and asks it to extract all the claims from every single table. The response of the model is then interpreted and modified so that it can be stored in a further json file, eliminating the textual part including the description that the model makes about the response it provides.
### ° Task 2
### ° Task 3