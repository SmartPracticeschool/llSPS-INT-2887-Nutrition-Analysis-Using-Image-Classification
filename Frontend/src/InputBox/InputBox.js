import React,{Component} from 'react';
import {Button} from 'semantic-ui-react'
import './InputBox.css';

class InputBox extends Component {
  state = {
      file : false
  }
  fileInputRef = React.createRef();

  fileChange=(e)=>{
      if(e.target.files[0]){
        this.setState({
            file:e.target.files[0]
        })
        this.props.showImage(e.target.files[0])
      }
  }
  handleUpload = ()=>{
    this.props.makeRequest()
    this.setState({file:false})
  }

  render() {
    return ( 
    <div id = "input-box" >
        <Button
            content="Browse"
            labelPosition="left"
            icon="file"
            onClick={() => {this.fileInputRef.current.click()}}
            style={{width:"auto",marginRight:"150px"}}
            color="teal"
            size='large'
        />
        <input
            name='yoyo'
            id='yoyo'
            ref={this.fileInputRef}
            type="file"
            hidden
            onChange={this.fileChange}
            accept="image/*"
        />
        <Button
            content="Upload"
            labelPosition="left"
            icon="upload"
            disabled={!this.state.file}
            style={{width:"auto"}}
            onClick={ this.handleUpload}
            color="blue"
            size="large"
            loading={this.props.uploading}
        />
    </div>
    );
  }
}

export default InputBox;
