from lxml import html


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

# Створення дерева HTML
tree = html.fromstring(html_content)

# XPath вирази
search_query_input = tree.xpath('//input[@id="searchQuery"]')
region_input = tree.xpath('//input[@id="regionInput"]')
search_button = tree.xpath('//button[@id="searchButton"]')

# Вивід результатів
print("Search Query Input:", search_query_input[0].attrib if search_query_input else "Not found")
print("Region Input:", region_input[0].attrib if region_input else "Not found")
print("Search Button:", search_button[0].attrib if search_button else "Not found")
