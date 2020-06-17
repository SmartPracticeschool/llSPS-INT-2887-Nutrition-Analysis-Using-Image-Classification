import React,{Component} from 'react';
import './App.css';
import Nav from './Nav/Nav'
import {Image} from 'semantic-ui-react'
import InputBox from './InputBox/InputBox'
class App extends Component {
  state = {
      base64:null,
      prediction:null,
      nutrients: null,
      uploading:false,
      selected:false
  }


  // method to handle the event when user select the file from file browser
  // selected image is converted into DataURL
  showImage = (file) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = () => {
      this.setState({
        selected:true,
        base64: reader.result
      })
    } 
  }

  // method to make request to Nutritionix API to get the nutrients of the fruit
  makeNutrientRequest = (name) => {
    
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("x-app-key", "a0765d4678a8c6a7fb6cc657569868e7");
    myHeaders.append("x-app-id", "67f40abf");
    myHeaders.append("x-remote-uset-id", "vijitkambojdev");

    var raw = JSON.stringify({"query":`${name}`,"num_servings":1,"aggregate":"string","line_delimited":false,"locale":"en_US"});

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    fetch("https://trackapi.nutritionix.com/v2/natural/nutrients", requestOptions)
    .then(response => response.json())
    .then(result => this.setState({prediction:name,nutrients:result,uploading:false,selected:false,base64:null}))
    .catch(error => console.log('error', error));
    }
  
  // method to make request to flask-server for classification
  makePredictRequest = ()=>{
    this.setState({uploading:true})
    const requestOptions = {
      method: 'POST',
      headers: {"Content-Type":"application/json","Accept":"application/json"},
      body: JSON.stringify({image:this.state.base64})
    };  
    fetch("https://yo-fruits.eu-gb.mybluemix.net/", requestOptions)
      .then(result => result.json())
      .then(re => this.makeNutrientRequest(re.prediction))
      .catch(error => console.log('error', "sdadada"));
  }
  

  render() {
    const {uploading,prediction,base64,nutrients,selected} = this.state
    const object = nutrients && nutrients.foods  ? nutrients.foods[0] :null
    return ( 
      <div id = "app" >
        
            <div id="cover">
              <Nav />
              Scroll -Down
            </div>

            <div id='field'>
              <div id="quote">{"Always try to eat the colours of rainbow"}</div>
              <Image 
                hidden={!selected} 
                style={{'height':"250px","width":"auto", 'position':"absolute",'top':"120px"}} 
                src = {base64 ? base64 : null}
              />

              {selected ? null : 
                <div id="prediction">

                  {prediction ? `Name = ${prediction}` : null} <br /><br />
                  {object ? `Calories = ${object.nf_calories} kcal` : null}<br /><br />
                  {object ? `Total Fat = ${object.nf_total_fat} g` : null}<br /><br />
                  {object ? `Protein = ${object.nf_protein} g` : null}<br /><br />
                  {object ? `Carbohydrates = ${object.nf_total_carbohydrate} g` : null}<br />

                  </div>
              }

              <InputBox makeRequest={this.makePredictRequest} showImage={(file)=>this.showImage(file)} uploading={uploading}/>

              

            </div>
      </div>
    );
  }
}

export default App;
