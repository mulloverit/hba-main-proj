// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.css';
'use strict';

class VisitorName extends React.Component {
  render() {
    return (
      <div>
        Hey, {this.props.name}
      </div>
    );
  }
}
ReactDOM.render(
  <VisitorName name="Guest"/>,
  document.getElementById('greeting-h2')
  );



// const el = React.createElement(
//   'div',
//   {className: 'greeting'},
//   'Hey, ' {this.props.name}
//   );

// ReactDOM.render(
//   el,
//   document.getElementById('greeting-h2')
//   );

