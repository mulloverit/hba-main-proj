"use strict";


class DynamicGreeting extends React.Component {
  render() {
    let UserName = window.username;

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

class Tray extends React.Component {
  constructor(props){
    super(props);
    
  }

  render () {
    const rows = [];
    
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
    this.handleAssetListUpdate = this.handleAssetListUpdate.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // my asset upload form should pass a prop to mainpagearea
  // that tells main page to update list of assets
  // no state passing, all components should manage their own satate
  // instead of "onAssetChange" maybe onSubimt or componentDidMount ??
  handleAssetListUpdate(event) {
    this.props.onAssetChange(event.target.value);
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
                <input
                  type="file"
                  ref={this.fileInput}
                  value={this.props.newAsset}
                  onChange={this.handleAssetListUpdate}
                />
                <button type="submit">Submit</button>
              </form>
          </div>
        </div>
      </div>
    );
  }
}

class MainPageArea extends React.Component {
  constructor(props) {
    super(props);
    
    let S_Draggable = window.ReactDraggable;
    let UserAssets = window.images;
    let UserAssetList = UserAssets.substr(6).slice(0, -6).split("&#39;, &#39;");

    UserAssetList = UserAssetList.map(image => {
      return ({ image: image});
    })

    this.state = {
      newAsset: '',
      assets: UserAssetList,
    };

    UserAssetList.forEach((image) => {
      console.log(image);
    })

    this.handleAssetListUpdate = this.handleAssetListUpdate.bind(this);
  }

  handleAssetListUpdate(assets) {
    this.setState({
      assets: assets
    });
  }

  render() {
    return (
      <div>
        <AssetUpload 
          newAsset={this.state.newAsset}
          onAssetChange={this.handleAssetListUpdate}
          />
        <Tray
          assets={this.state.assets}
        />
      </div>
    );
  }
}


ReactDOM.render(
  <DynamicGreeting />,
  document.getElementById('dynamic-greeting')
  )

ReactDOM.render(
  <MainPageArea />,
  document.getElementById('main-page-container')
);