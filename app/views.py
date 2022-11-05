import openai
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

operation_types = {'multiplication':'*', 'addition':'+', 'subtraction':'-' } 

openai.api_key = "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"


@csrf_exempt
def sample(request: HttpRequest):
    if request.POST:
        data = request.POST
    else:
        data = json.loads(request.body)
     
    result = None
    operation_type = None
    data_ot = data['operation_type'].strip().lower()
    
    if data_ot in operation_types:

        operation_type = data_ot 
        result = eval(f'{data["x"]}{operation_types[data_ot]}{data["y"]}')
  

    else:
        
        synonyms = {'product':'multiplication', 'difference':'subtraction', 'sum':'addition'}
        
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{data_ot} \n\n| solution | operation_type |",
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        _, result, operation_type, _= [x.strip() for x in  [y for y in response.choices[0].text.split('\n') if y][-1].split('|')]
        operation_type = operation_type if not operation_type in synonyms else synonyms[operation_type]
      
    
    return JsonResponse({"slackUsername":"Oedjoat", "result":int(result) ,"operation_type":operation_type})



    