## IoT Smart Home System
Program structure

```
  -- code (Main Folder)
      --AWS (This folder contains code, running inside the AWS EC2 instance)
          -- app.py     (The main python file use to render the main program)
          -- static     (Contain the .js and .css files use to styling the GUI)
          -- templates  (Contain the .html files use to crete a GUI)
      
      --PI (This folder contains code, running inside the Raspberry Pi)
          -- pub.py      (The main python file use to send data to main program from Raspberry pi)
          -- my_model    (AI model)
      
      --CNN_Train (This folder contains code used to training the weather prediction model)
          -- Prediction.ipynb        (AI model tram=ning python notebook code file)
          -- weatherHistory.csv      (Traning data)
          -- my_model                (Saved model folder, used in PI progaram)
      
```
