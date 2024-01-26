
from promptflow import tool
import requests
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

@tool
def get_value_from_ai_search(data: str) -> str:

    search_service_name = "hotboard"
    api_key = "ao52MO88dTqe1it6nBnNu6grJwmZLk8RMat3TQoXZeAzSeDHy0Qm"
    index_name = "hotboard-index"
    
    parsed_data = json.loads(data)
    parsed_data = json.dumps(parsed_data)
    
    parsed_data = json.loads(data)
    search_fields = parsed_data.get('searchFields', '*')
    top = parsed_data.get('top', 50)
    orderby = parsed_data.get('orderby', '')

    url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}/docs?api-version=2023-11-01&searchFields={search_fields}&$top={top}&$orderby={orderby}"
    headers = {"api-key": api_key, "Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    print(f"Response body: {response.text}")

    response_json = json.loads(response.text)

    result = []
    for item in response_json.get('value', []):
        result.append({
            'bank': item.get('bank'),
            'name': item.get('name'),
            'rate': item.get('rate'),
            'price': str(item.get('price'))
        })

    return result
