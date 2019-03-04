"use strict";

let S_Draggable = window.ReactDraggable;
const { DragDropContext, Draggable, Droppable } = window.ReactBeautifulDnd;
const grid = 8;

const reorder = (list, startIndex, endIndex) => {
  // create array from incoming list
  // and an empty array to populate with removed items from list
  // splice -> first arg is beginning of splice, 2nd arg is delete count
  //           last arg is the items that will be inserted at the
  //           beginning of splice
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

const getItems = (count) => {
  Array.from({ length: count }, (v, k) => k).map(k => ({
    id: `item-${k}`,
    content: `item ${k}`,
  }));
}

const getItemStyle = (isDragging, draggableStyle) => ({

  userSelect: 'none',
  padding: grid * 2,
  margin: `0 0 ${grid}px 0`,
  background: isDragging ? 'lightgreen' : 'grey',
  ...draggableStyle,
});

const getListStyle = (isDraggingOver) => ({
  background: isDraggingOver ? 'lightblue' : 'pink',
  padding: grid,
  width: 250,
}); 


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


class DroppableComp extends React.Component {
  constructor(props){
    super(props);
  }
  
  render() {
    console.log(this.props.userAssetList);

    return (
      <Droppable
        droppableId={this.props.droppableId}
        userAssetList={this.props.userAssetList}
      >
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            style={getListStyle(snapshot.isDraggingOver)}
          >

            {this.props.userAssetList.map((item, index) => (
              <Draggable 
                key={item.image}
                draggableId={item.image}
                index={index}
              >
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    style={getItemStyle(
                      snapshot.isDragging,
                      provided.draggableProps.style
                    )}
                  >
                    {item.content}
                  </div>
                )}
              </Draggable>
            ))}

            {provided.placeholder}

          </div>
        )}
      </Droppable>
    );
  }
}


class DragDropContextComp extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <DragDropContext
        onDragEnd={this.props.onDragEnd} >
          <DroppableComp
            droppableId="droppable"
            userAssetList={this.props.userAssetList}
           />
      </DragDropContext>
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
    this.props.userAssetList.forEach((asset) => {
      rows.push(
        <DraggableAssetContainer
          image={asset.image}
          key={asset.image}
        />
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
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
  }

  handleSubmit(event) {
    event.preventDefault();
    const file = new File(this.fileInput.current.files,
                          this.fileInput.current.files[0].name
                          );
    this.props.onSubmit(file)
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
              <form
                onSubmit={this.handleSubmit}
                method="POST"
                encType="multipart/form-data">
                  <input
                    type="file"
                    ref={this.fileInput}
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
    this.handleSubmit = this.handleSubmit.bind(this);
    this.onDragEnd = this.onDragEnd.bind(this);

    let userAssets = window.images;
    let userAssetList = userAssets.substr(6).slice(0, -6).split("&#39;, &#39;");

    userAssetList = userAssetList.map(image => {
      return ({ image: image});
    })

    this.state = {
      userAssetList: userAssetList
    };
  }


  onDragEnd(validDropped) {
    // if dropped otuside valid dropzone, do nothing
    if (!validDropped.destination) {
      return;
    }

    // of dropped in valid zone, reorder items accordingly
    // this.state.items is incoming list
    // source index is items being moved ("removed" in reorder func)
    // destination index is where the moved items will be inserted
    const userAssetList = reorder(
      this.state.userAssetList,
      validDropped.source.index,
      validDropped.destination.index
    );

    // and refresh state with new ordered list  
    this.setState({
      userAssetList,
    });
  }

  handleSubmit(file) {
    event.preventDefault();
    
    const formData = new FormData();
    const postUrl = "/upload-inputs"
    const xmlPackage = new XMLHttpRequest();

    formData.append('file', file);
    xmlPackage.open("POST", postUrl);
    xmlPackage.responseType = 'text';
    xmlPackage.onload = () => {
      let assetListString = xmlPackage.response
      let userAssetList = assetListString.substring(2).slice(0, -2).split("', '");
      console.log("MUNGED:", userAssetList);

      userAssetList = userAssetList.map(image => {
        return ({ image: image});
        })

      if (xmlPackage.status === 200) {
        console.log("ASSET LIST:", userAssetList);
        this.setState({userAssetList: userAssetList});
        }
    };

    xmlPackage.send(formData);
  }

  render() {
    return (
      <div>
        <AssetUpload 
          onSubmit={this.handleSubmit}
          />
        
        <div>
          <DragDropContextComp 
            onDragEnd={this.onDragEnd}
            userAssetList={this.state.userAssetList}
          />
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <DynamicGreeting />,
  document.getElementById('dynamic-greeting')
);

ReactDOM.render(
  <MainPageArea />,
  document.getElementById('main-page-container')
);