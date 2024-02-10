You are mimicking a customer who is interested in a car and the features they are interested in are [range, top speed, color]. Write a convincing paragraph as the customer who inquires about car recommendations.  Try to be creative and feel free to specify specific values for the features. 

For the sake of clarification, here is an example:

 The customer is interested in a laptop and the features they are interested in are [display size, color, memory size]. 

AI: Hi! I have been looking for a laptop for my work for a few weeks now and I still can't decide which model to buy! I really need something with a big display like 16 inches. The theme of my office is all white so I'm looking for a laptop that's white too. Also, since I'm storing a lot of business files I need something with a lot of memory. Ideally a 2 terabyte laptop. Does anyone know what model laptop I should buy?? 

In this case, the display size was 16 inches, the color was white, and the memory size was 2 terabytes. 


Hey there! I'm on the hunt for a new car, and I could really use some recommendations. I'm all about eco-friendliness, so I'm looking for an electric or hybrid model with a fantastic range of at least 300 miles on a single charge. Speed is also a priority for me, and I'd love a car that can hit a top speed of around 150 mph. Lastly, I want something that stands out, so I'm thinking of a unique color like deep emerald green. Any suggestions for a car that ticks all these boxes? Thanks in advance!



todo 
1. specify a shorter output for the mimicking part
2. make input be just features and not product 
3. True: dimension and color False: price and telephone number 



list of dimensions and colors 

we tell model to write a sentence with the dim, color, price, or tn  (sample randomly for the true and false attributes)

then we make data set 

feed in data and we say that price and tn are NOT attributes. see if model can extract true attributes 

"Hello I am looking for a 3x4x5 laptop that is black", [3x4x5, 'black']

* Lets generate 100 first
* First determine true accuracy (nothing wrong), then look into precision and recall



In contex learning  LLMs and NLP

2/9
Be minimal with the prompt (we want diverse sentences)
to not give example
instead of parsing know ground truth and feed to LLM 


pre define color
pre define dims
pre define number
pre define price

