# Meeting Minutes for CER

### Todo 
- [ ] specify a shorter output for the mimicking part

- [ ] make input be just features and not product 

- [ ] True: dimension and color False: price and telephone number 

- [ ] Fix the Evaluation Given Features section in `main.ipynb`


list of dimensions and colors 

we tell model to write a sentence with the dim, color, price, or tn  (sample randomly for the true and false attributes)

then we make data set 

feed in data and we say that price and tn are NOT attributes. see if model can extract true attributes 

"Hello I am looking for a 3x4x5 laptop that is black", [3x4x5, 'black']

* Lets generate 100 first
* First determine true accuracy (nothing wrong), then look into precision and recall



In context learning  LLMs and NLP

---

### 2/9

Be minimal with the prompt (we want diverse sentences)

do not give example


instead of parsing know ground truth and feed to LLM 


pre define color
pre define dims
pre define number
pre define price

---

### 2/14

metrics for measuring performance 

accuracy = Only get one with exact match everything else is 0
positive recall rate = how many positives you got right in total. 
negative recall rate = 
precision = count(false positives)


Make llm output match this format
ATTR_NAME :: ATTR_VALUE ;; ATTR_NAME :: ATTR_VALUE

This is for the evaluation phase. We want to make the processing as easy as possible.
Look into other possible solutions.

### 7/20
`main.ipynb`
- Added a `Setup` section to ensure future users can instantly run the notebook
- Fixed `parse_values()` utility function which can now assume no values (`"NONE"`) are present which will skip that line
- During the Evaluation Phase, it was discovered that a Division By Zero ERROR occurred
    - `PREC += matches / len(set(parsed_data.values()))`
    - Adding this to the TODO list

`prompts.py`
- Updated `get_eval_with_feature_prompt()`
    - returns `"NONE"` if the LLM cannot find any attributes
    - ensures that LLM returns the required proper format 

`model.py`
- updated model to use GPT-4o-mini

`README.md`
- updated to include setup information