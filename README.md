# pcf-tensorflow-server
A sample python tensorflow server on PCF

Train the model, to be saved in the ./model directory
```
python train.py
```

Push to PCF
```
cf push -f mf.yml
```

To test the service 
```
https://<app-route>/test-predict
```

