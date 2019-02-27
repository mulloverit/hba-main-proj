"use strict";

var Draggable = window.ReactDraggable;


class DraggableDefinition extends React.Component {
  constructor(props) {
    super(props);
    this.handleDrag = this.handleDrag.bind(this);
    this.onStart = this.onStart.bind(this);
    this.onStop = this.onStop.bind(this);


    this.state = {
      activeDrags: 0,
      deltaPosition: {
        x: 0, y: 0
      },
      controlledPosition: {
        x: -400, y: 200
      }
    }
  }

  handleDrag(event, ui) {
    const {x, y} = this.state.deltaPosition;
    this.setState({
      deltaPosition: {
        x: x + ui.deltaX,
        y: y + ui.deltaY
      }
    });
  }

  onStart() {
    this.setState({
      activeDrags: ++this.state.activeDrags
    });
  }

  onStop() {
    this.setState({
      activeDrags: --this.state.activeDrags
    });
  }


  render() {
    const dragHandlers = {onStart: this.onStart, onStop: this.onStop};
    const {deltaPosition, controlledPosition} = this.state;
  
    return (
      <Draggable {...dragHandlers}>
        <div className="container-display">. I can be dragged anywhere</div>
      </Draggable>
    );
  }
}

class DynamicGreeting extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      name: 'guest'
    }
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
            <br />
            <h1>Welcome, {this.state.name} !</h1>
            <br />
          </div>
        </div>
      </div>
    );
  }
}

class ImageUploadForm extends React.Component {
  constructor(props) {
    super(props);
    this.fileInputOne = React.createRef();
    this.fileInputTwo = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const imageContainerOne = document.querySelector('#image-display-container #contained-image');
    const imageContainerTwo = document.getElementById('#image-display-container-2 #contained-image');
    const formData = new FormData();
    const fileOne = new File(this.fileInputOne.current.files, this.fileInputOne.current.files.name);
    const fileTwo = new File(this.fileInputTwo.current.files, this.fileInputOne.current.files.name);
    const postUrl = "/upload-inputs"
    const xmlPackage = new XMLHttpRequest();

    formData.append('file1', fileOne);
    formData.append('file2', fileTwo);
    xmlPackage.open("POST", postUrl);
    xmlPackage.responseType = 'json';
    xmlPackage.onload = function() {
      const imageUrls = xmlPackage.response;
      imageContainerOne.setAttribute('src', imageUrls[0]);
      imageContainerTwo.setAttribute('src', imageUrls[1]);
    }

    xmlPackage.send(formData);

  }
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
              <form onSubmit={this.handleSubmit} method="POST" encType="multipart/form-data">
                <input type="file" name="img-1" id="img-1" ref={this.fileInputOne} />
                <input type="file" name="img-2" id="img-2" ref={this.fileInputTwo} />
                <button type="submit">Submit</button>
              </form>
          </div>
        </div>
      </div>
    );
  }
}

class ImageDisplayContainer extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
            <div className="container-display">
              <img id="contained-image" src="" />
            </div>
          </div>
        </div>
      </div>
    );
  };
}


ReactDOM.render(
  <DynamicGreeting />,
  document.getElementById('dynamic-greeting')
);

ReactDOM.render(
  <ImageDisplayContainer />,
  document.getElementById('image-display-container')
);

ReactDOM.render(
  <ImageDisplayContainer />,
  document.getElementById('image-display-container-2')
);

ReactDOM.render(
  <DraggableDefinition />,
  document.getElementById('image-display-container')
);

ReactDOM.render(
  <DraggableDefinition />,
  document.getElementById('image-display-container-2')
);


ReactDOM.render(
  <ImageUploadForm />,
  document.getElementById('image-upload-form')
);
