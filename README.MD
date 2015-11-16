### Updates0.2
This repo will be mantained and updated within ai-se group. The old [repo](https://github.com/WeiFoo/TuningLearners) will be a history and as a reference.

###Updates0.1
 In version 0.1, we had to write a DE code for each specific leaner, which is a burden to some degree and also not a good progamming practice. We need to make some improvements in this verison. The improvements include DE tuner and also the learner
 
###DE Tuner
For each new learner to be tuned, you should write a class in tuner.py, which inherits DeBase class.
You should indicate how to treat your tuning parameters if some tuning parameter has constant relationship, which the new genereated parameters whould comply with. For example, two parameters, each time the new a should less than b. Then you should check this property in ```treat```function. Also, you need to indicate how to call your learner, which is defined in ```callModel()``` function.
 ```
 
class RfDE(DeBase):
  def __init__(i, model):
    super(RfDE, i).__init__(model)

  def treat(i, lst):
    return lst

  def callModel(i):
    return rf()[-1]
 ```
### New Learner
For each new learner to be tuned, you need to define a class inheriting ```Learner```class, where, ```default``` ,```optimizer``` and ```call``` functions have to be implemented.
**tunelst** contains the parameter names to be tuned, note: they're global variable, please check code to see how to use.
**tune_min** and **tune_max** specify the tuning range, if it's a nominal type, please use lst, e.g.```[a,b,c]``` in both tune_min and tune_max
```
class CART(Learner):
  def __init__(i, train, tune, predict):
    super(CART, i).__init__(train, tune, predict)
    i.tunelst = ["The.cart.max_features", "The.cart.max_depth", "The.cart.min_samples_split",
                 "The.cart.min_samples_leaf", "The.option.threshold"]
    i.tune_min = [0.01, 1, 2, 1, 0.01, 0]
    i.tune_max = [1, 50, 20, 20, 1, 100]

  def default(i):
    The.cart.max_features = None
    The.cart.max_depth = None
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 1
    The.option.threshold = 0.5

  def call(i): return cart()

  def optimizer(i):
    tuner = CartDE(i)
    tuner.DE()
```
 
