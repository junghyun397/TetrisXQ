# TetrisXQ
![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/python-3.7-blue.svg)
![](https://img.shields.io/badge/tensorflow-1.6%20or%20higher-orange.svg)

TetrisXQ - Reverse tetris Reinforcement Learning Environment and implementations(DQN).  
Here's the Tetris that will probably annoy you the *most?*

## Look around first
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

## Train *Your Model* with TetrisXQ Environment
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

## File information
<pre><code>
TetrisXQ
├── agent   # inforcement Learning Agent Configuration
│   ├── a3c  # A3C algorithm agent
│   │   ├── ACNetwork.py  # Actor-Critic network
│   │   └── Train.py  # Training using the A3C algorithm
│   ├── dqn  # Deep-Q-Network algorithm aget
│   │   ├── data  # Self-replay
│   │   │   └── BatchManager.py  # Self-replay manager
│   │   ├── Demo.py  # Demo by loading a trained DQN model
│   │   ├── QCNNModel.py  # CNN network approximating Q
│   │   ├── QMLPModel.py  # MLP network to approximate Q
│   │   └── Train.py  # Training using the Deep-Q-Learning algorithm
│   └── DeepNetworkModel.py  # Neural-Network Interface Class
├── environment  # Environment Configuration
│   ├── reward  # Reward system
│   │   ├── AnalyseBoardReward.py  # Reward by analyse tetris board
│   │   ├── RewardModule.py  # Reward module Interface class
│   │   ├── SumTurnsReward.py  # Reward by number of turns played
│   │   └── ZeroScoreReward.py  # Reward by when turn score is 0
│   ├── AutoPlayEnvironment.py  # Autoplay-Environment with built-in Tetris AI engine
│   ├── EnvironmentModel.py  # Common Action-Reward Environment Interface
│   └── ManualPlayEnvironment.py  # ManualPlay-Environment with human play interface
├── graphics  # Tetris graphics Configuration
│   ├── DummyGraphicModule.py  # Dummy to use no-graphics
│   ├── GraphicInterface.py  # Tetris graphical interface
│   └── GraphicModule.py  # PyGame-based Tetris graphics module
├── tetris  # Tetris game logic Configuration
│   ├── ai  # Weigth-based Tetris-AI engin
│   │   ├── TetrisAI.py  # Weight Evaluation-based Tetris AI Engine
│   │   └── TetrisWeight.py  # pre-Defined weights
│   ├── TetrisModel.py  # Generalized Tetris logic model
│   └── Tetromino.py  # Definition of Tetris Block
├── Display.py  # Simply play Tetris or watch AI play
├── README.md
├── requirements.txt  # PyPl dependency list
└── Settings.py  # Tetris model definition and hyper-parameter settings
</code></pre>
