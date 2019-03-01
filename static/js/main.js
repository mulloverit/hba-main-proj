"use strict";


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
            <h1>Welcome, {UserName}</h1>
            <br />
          </div>
        </div>
      </div>
    );
  }
}

class DragDropTest extends React.Component {
  onBeforeDragStart = () => {
    /*...*/
  };

  onDragStart = () => {
    /*...*/
  };
  onDragUpdate = () => {
    /*...*/
  };
  onDragEnd = () => {
    // the only one that is required
  };

  render() {
    return (
      <DragDropContext
        onBeforeDragStart={this.onBeforeDragStart}
        onDragStart={this.onDragStart}
        onDragUpdate={this.onDragUpdate}
        onDragEnd={this.onDragEnd}
      >
        <div>Hello world</div>
      </DragDropContext>)
  }
}

const { DragDropContext, Draggable, Droppable } = window.ReactBeautifulDnd;
let S_Draggable = window.ReactDraggable;
let UserName = window.username;
let UserAssetResponse = window.images;
let UserAssetList = UserAssetResponse.substr(6).slice(0, -6).split("&#39;, &#39;");

UserAssetList = UserAssetList.map(image => {
  return ({ image: image});
})

UserAssetList.forEach((image) => {
  console.log(image);
})

class DraggableAssetContainer extends React.Component {
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
    const image = this.props.image;
  
    return (
      <S_Draggable {...dragHandlers} >
        <div className="drag-container-display">
          <img className="drag-image-rows" src={image} />
        </div>
      </S_Draggable>
    );
  }
}

// class PlayArea extends React.Component {
//   render () {
//     const rows = []
//     const columns = []

//   }
// }

class Tray extends React.Component {
  render () {
    const rows = [];
    let UserAssetList = this.props.assets;

    UserAssetList.forEach((asset) => {
      rows.push(
        <DraggableAssetContainer
          image={asset.image}
          key={asset.image} />
      );
    });
    
    return (
      <div className="bounding-tray">
        <h2>Asset Tray</h2>
        <div id="tray-rows">{rows}</div>
      </div>
    );
  }
}

class AssetUpload extends React.Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const imageContainerOne = document.getElementById('contained-image');
    const formData = new FormData();
    const file = new File(this.fileInput.current.files, this.fileInput.current.files.name);
    const postUrl = "/upload-inputs"
    const xmlPackage = new XMLHttpRequest();

    formData.append('file', file);
    xmlPackage.open("POST", postUrl);
    xmlPackage.responseType = 'json';
    xmlPackage.onload = function() {
      const imageUrls = xmlPackage.response;
        return <Tray />;
    }

    xmlPackage.send(formData);

  }
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
              <form onSubmit={this.handleSubmit} method="POST" encType="multipart/form-data">
                <input type="file" name="img-1" id="img-1" ref={this.fileInput} />
                <button type="submit">Submit</button>
              </form>
          </div>
        </div>
      </div>
    );
  }
}

// const ASSETS = [
//   {image: 'http://hackbright-image-upload-test.s3.amazonaws.com/cmahon/3405a9fe-2bd2-49ab-b884-efb35b63f015_static/images/cmahon_undefined', text: "this is image one"},
//   {image: 'http://hackbright-image-upload-test.s3.amazonaws.com/cmahon/cdac03e0-6703-4d1e-926c-ee036a3134fe_static/images/cmahon_undefined', text: "this is from s3!"},
//   {image: 'http://hackbright-image-upload-test.s3.amazonaws.com/cmahon/720b2bed-fd81-4503-97cb-6c62c07fa462_static/images/cmahon_undefined', text: "derp"},
//   {image: 'http://hackbright-image-upload-test.s3.amazonaws.com/cmahon/6455288a-8bfe-4bfa-b5aa-012a50c9f852_static/images/cmahon_undefined', text: "deeeurp"}
// ];

class MainPageArea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      assets: UserAssetList,
    };
  }

  handleAssetUpdate(assets) {
    this.setState({
      assets: assets
    });
  }

  render() {
    return (
      <div>
        <AssetUpload />
        <Tray
          assets={this.state.assets}
          handleAssetUpdate={this.handleAssetUpdate}
        />
      </div>
    );
  }
}

ReactDOM.render(
  <DynamicGreeting />,
  document.getElementById('dynamic-greeting')
  )

// ReactDOM.render(
//   <DragDropTest />,
//   document.getElementById('drag-drop-test')
//   )

ReactDOM.render(
  <MainPageArea />,
  document.getElementById('main-page-container')
);