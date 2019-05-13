# TetrisXQ
![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/python-3.7-blue.svg)
![](https://img.shields.io/badge/tensorflow-1.6%20or%20higher-orange.svg)

TetrisXQ - Reverse tetris Reinforcement Learning Environment and implementations(DQN).  
Here's the Tetris that will probably annoy you the *most?*

## *Calm down* and look around first
Feel a little bit about what's happening through Display.py
<pre><code>
python Display.py -e manual -g y # Playing the Tetris on Yourself
python Display.py -e auto -g y  # Watch AI play
</code></pre>

## Training with DQN
Start training with a simple Deep-Q-Network.
<pre><code>
python ./agent/dqn/Train.py -e auto -g y -c 2000  # Learn 2000 games with auto play.
</code></pre>

## It's your turn now!
It is probably very similar to OpenAI-gym. Your job is simple: just create an environment and then action on it!  
<pre><code>
env = AutoPlayEnvironment()  # Call Auto(Tetris AI) play environment.
state, reward, end = env.action(an_action)  # Action!
</code></pre>
If you want to play and train ***yourself***, following this:
<pre><code>
env = ManualPlayEnvironment()  # Call Manual play environment.
state, reward, end = env.action(an_action)  # Action!
</code></pre>
