# Chat_Bot

it's a Super Conversational chatbot that can ask any question.

it has a Simple  implementation with PyTorch. 

Whenever the propability of the response is < 0.75 it goes scrapping the a better response from wikipedia and question-answering platforms :quora and reddi using SELENIUM.

The implementation is straightforward with a Feed Forward Neural net with 2 hidden layers.

Customization for your own use case is super easy. Just modify intents.json with possible patterns and responses and re-run the training (see below for more info).


![Alt text](/Chat_Bot/3.png?raw=true "Titl3.png")
