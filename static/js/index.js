// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.css';
'use strict';

class VisitorName extends React.Component {
  render() {
    return (
      <h2>
        Hey, {this.props.name}
      </h2>
    );
  }
}

ReactDOM.render(
  <VisitorName name="Guest"/>,
  document.getElementById('dynamic-greeting')
  );