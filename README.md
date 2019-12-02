# pcf-tensorflow-server
A sample python tensorflow server on PCF

Train the model, to be saved in the ./model directory
```
python train.py
```

Web frontend ui built with [create-react-app]
(https://github.com/facebook/create-react-app)


Build the react front end app
```
cd web/app 
npm run-script build
```

Push to PCF
```
cf push -f mf.yml
```

To test the service 
```
https://<app-route>/test-predict
```

