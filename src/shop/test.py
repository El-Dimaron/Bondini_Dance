test_dict = {"search": [""], "category": ["issue", "majority", "require"]}

final_url = ""

for key, dict_list in test_dict.items():
    for item in dict_list:
        final_url += f"{key}={item}&"

print(final_url.rstrip("&"))


"search=&category=issue&category=majority&category=require&category=himsel"
