import re

# Ваш HTML-код як рядок
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search Page</title>
</head>
<body>
    <form id="searchForm">
        <input type="text" id="searchQuery" name="query" placeholder="Enter your search query">
        <input type="text" id="regionInput" name="region" placeholder="Enter your region">
        <button type="submit" id="searchButton">Search</button>
    </form>
</body>
</html>
'''

# Регулярні вирази для пошуку елементів
search_query_pattern = re.compile(r'<input[^>]*id="searchQuery"[^>]*>')
region_input_pattern = re.compile(r'<input[^>]*id="regionInput"[^>]*>')
search_button_pattern = re.compile(r'<button[^>]*id="searchButton"[^>]*>.*?</button>', re.DOTALL)

# Знаходження елементів
search_query_input = search_query_pattern.search(html_content)
region_input = region_input_pattern.search(html_content)
search_button = search_button_pattern.search(html_content)

# Вивід результатів
print("Search Query Input:", search_query_input.group() if search_query_input else "Not found")
print("Region Input:", region_input.group() if region_input else "Not found")
print("Search Button:", search_button.group() if search_button else "Not found")
