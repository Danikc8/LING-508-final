# Cantonese Dictionary

## Searching a character

You can enter in a Chinese character using the Search interface and click submit. You will get information about that character displayed as a JSON string. For example:

```
"Character": "心"
"Part of Speech": "NOUN"
"Jyutping": "sam1"
"Phonological Components": 
    "Onset": "s"
    "Nucleus": "a"
    "Coda": "m"
    "Tone": "1"
"English Translation": "heart"
```

The API can be called directly without the UI, using a POST request. The endpoint is http://localhost:5000/parse. The POST request must contain a JSON body with the "word" key, for example:

```
{"word": "心"}
```

The curl command is as follows:

```
curl -X POST http://127.0.0.1:5000/pronounce \
     -H "Content-Type: application/json" \
     -d '{"word": "白"}'
```

You should receive a success message like below:

```
{"msg": "success"}
```