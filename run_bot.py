# Set Up Environment
from kaggle_environments import evaluate, make
env = make("halite", configuration={ "episodeSteps": 400 }, debug=True)
print (env.configuration)

env.run(["bot_test.py", "random","random","random"])
env.render(mode="ipython")
