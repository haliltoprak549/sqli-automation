# sqli-automation
SQL injection automation with python.

Extracts file names out of MySQL database using Blind SQL attacks with binary search.

It uses SELECT CASE to see the effect of the query on the vulnerable-pages/login.php.

First, it finds the total number of tables using binary search with SELECT CASE and COUNT function from information_schema.tables. If the query is provided, then it will not login to the system. And that is how we will know query is provided. If query is provided, it means we found the total number of tables.

Then, by using the total number of tables, it finds the length of all the table using binary search with SELECT CASE and LENGTH function, and iterates through all tables using LIMIT x, 1 function.

Last, by using the length of the table name, it finds every letter using binary search by iterating through table names. It searches for A-Z characters and underscore character with SUBSTRING function. When it finds a letter it will append it to a temporary letter list. And at the end of the iteration, it will join the table name together and will append it to a table name list.
