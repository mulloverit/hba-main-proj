// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.css';
'use strict';

class VisitorName extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      name: "Guest",
      message: "you are not signed in."
    }
  }

  render() {
    return (
      <div>
        Hey, {this.state.name}, {this.state.message}
      </div>
    );
  }
}


ReactDOM.render(
  <VisitorName name=""/>,
  document.getElementById('greeting-h2')
  );
