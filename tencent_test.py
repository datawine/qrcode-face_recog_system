from tencent_util import search_person
import base64

with open("img/2019312690.jpeg", "rb") as FILE:
    picture = base64.encodestring(FILE.read()).decode('utf-8')
    result = search_person(picture)
    print(result)