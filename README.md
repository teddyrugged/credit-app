
## Coding Task

The given sample.json file contains bank transaction details of 10 customers over a 3 month period (April 1st 2022 to June 30th 2022).

You are to create an application to store the customers data and expose endpoints that return data about these customers.

The included api.spec.yaml file details the required endpoints and their return values.

- Required tools: Django, Django Rest Framework
- Optional tools: Any Python library
- Application should be created in this directory
- Database used should be sqlite
- If any details are unclear please ask. Assumptions lead to errors.

### Credit Worthiness Score

The credit worthiness score of a customer is calculated as follows:
 - The average of weekly credits is calculated for every week starting from 2022-04-01 to 2022-06-30
 - The average of weekly debits is calculated for every week starting from 2022-04-01 to 2022-06-30
 - Find ratio of sum of average weekly credits to sum of average weekly debits is calculated
 - Apply Sigmoid Function to ratio

 Example:
    
    Say Customer AA has two credits and three debits between 2022-04-01 and 2022-04-07
    
    Average credit for week 1 =  (credit_amount_1 + credit_amount_2) / 7
    Average debit for week 1 =  (debit_amount_1 + debit_amount_2 + debit_amount_3) / 7

    The average credits and debits are calculated for week 2 i.e 2022-04-08 to 2022-04-14 and so on.

    ratio = sum (average_credit_week_1 + ...) / sum (average_debit_week_1 + ...)
    score = SigmoidFunc(ratio)


### Deadline
 On or before Saturday, 28th January 2023, 11:59pm