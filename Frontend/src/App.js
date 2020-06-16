import React,{Component} from 'react';
import './App.css';
import Nav from './Nav/Nav'
import {Image} from 'semantic-ui-react'
import InputBox from './InputBox/InputBox'
class App extends Component {
  state = {
      file: false,
      base64:null,
      prediction:null,
      nutrients: null
  }

  showImage = (file) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = () => {
      this.setState({
        file:file,
        base64: reader.result
      })
    } 
  }

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
    .then(result => this.setState({prediction:name,nutrients:result}))
    .catch(error => console.log('error', error));
    }
  

  makePredictRequest = ()=>{
    const requestOptions = {
      method: 'POST',
      headers: {"Content-Type":"application/json","Accept":"application/json"},
      body: JSON.stringify({image:this.state.base64})
    };  
    fetch("http://yo-fruits.eu-gb.mybluemix.net/", requestOptions)
      .then(result => result.json())
      .then(re => this.makeNutrientRequest(re.prediction))
      .catch(error => console.log('error', error));
  }
  

  render() {
    return ( <
      div id = "app" >
          <Nav />
          <div id='container'>
          <Image style={{'height':"250px","width":"auto", "margin":"0px auto 15px auto"}} src = {this.state.base64 ? this.state.base64 : null}/>
          <InputBox makeRequest={this.makePredictRequest} showImage={(file)=>this.showImage(file)}/>
          <div id="prediction">
              {this.state.prediction ? this.state.prediction : null} <br /><br />
              { this.state.nutrients ? `Calories = ${this.state.nutrients.foods[0].nf_calories}` : null}<br />
              { this.state.nutrients ? `Total Fat = ${this.state.nutrients.foods[0].nf_total_fat}` : null}<br />
              { this.state.nutrients ? `Protein = ${this.state.nutrients.foods[0].nf_protein}` : null}<br />
              { this.state.nutrients ? `Carbohydrates = ${this.state.nutrients.foods[0].nf_total_carbohydrate}` : null}<br />
          </div>
          </div>
          <div id='logo'></div>
      </div>
    );
  }
}

export default App;
