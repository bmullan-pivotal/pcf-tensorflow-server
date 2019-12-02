import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
// import React from 'react';

class ImageList extends Component {

  componentDidMount() {

    console.log("componentDidMount")
    fetch('/get-image-ids')
    .then(res => res.json())
    .then((data) => {
      var images = data.map(function(image) {
        return { image_url : "/image/"+image, image : image } 
      });
      this.setState({ images: images })
      console.log("componentDidMount",this.state)  
    })
    .catch(console.log)
        
  }

  constructor(props) {
	  super(props);
	  this.predict = this.predict.bind(this);
	  this.state = { greeting: 'Hello' };
  }

  predict() {
    var images = this.state.images;
    var that = this;
    images.forEach(function(image,index) {
      fetch('/predict/'+image.image)
      .then(res => {
        console.log("res",res);
        return res.text()
      }) 
      .then((data) => {
        console.log("image",image,"index",index,"data",data);
        image.className = data;
        that.setState({ images : images});
      });
    })
    
  }
 //  frenchify() {
	//   this.setState({ greeting: 'Bonjour' });
	// }
  render() {
    console.log("state:",this.state)
    if (!this.state.images) {
      return (
        <div>No data!</div>
      );
    }

    const items = this.state.images.map((image, key) =>
        <Grid item>
          <Box width={150} m={2} p={3} color="primary" bgcolor="secondary.main">
            <img src={image.image_url} height="105" width="105"/>
            <div>{image.className ? image.className : ""}</div>
          </Box>
        </Grid>
    );

    return (
      <div>
        <button onClick={this.predict}>Predict</button>
  
      <Grid container direction="row" justify="center" alignItems="center">
      {items}
      </Grid>
      </div>
    );
  }
}

export default ImageList;
