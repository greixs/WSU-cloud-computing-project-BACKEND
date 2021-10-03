"""
	woolies: https://www.woolworths.com.au/apis/ui/Search/products (straight up json)
	coles: https://shop.coles.com.au/online/COLRSSearchDisplay?storeId=20601&catalogId=10576&searchTerm=banana&categoryId=&tabType=everything&tabId=everything&personaliseSort=false&langId=-1&beginIndex=0&browseView=false&facetLimit=100&searchSource=Q&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&pageView=image&errorView=AjaxActionErrorResponse&requesttype=ajax (you need lxml html parse and find the "product", then there will be an array of dict for you to parse)
"""

