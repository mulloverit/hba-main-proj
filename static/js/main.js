"use strict";

const { DragDropContext, Draggable, Droppable } = window.ReactBeautifulDnd;
const grid = 8;

const reorder = (list, startIndex, endIndex) => {
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
          <div className="col-6">
            <br />
            <form action="/sign-out" method="POST">
              <button type="submit" name="sign-out">sign-out</button>
            </form>
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
                    <img src={item.image} height="100" width="100"/>
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
    this.props.onSubmit(file);
    document.getElementById('file-input').value = "";
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
                    id="file-input"
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

    // provide default image if user has no assets
    if ( userAssetList[0] === "" ) {
      userAssetList.splice(0, 1, "static/images/smiling-ready.png");
    }

    userAssetList = userAssetList.map(image => {
      return ({ image: image});
    })

    this.state = {
      userAssetList: userAssetList
    };
  }

  onDragEnd(validDropped) {

    if (!validDropped.destination) {
      return;
    }

    const userAssetList = reorder(
      this.state.userAssetList,
      validDropped.source.index,
      validDropped.destination.index
    );

    this.setState({
      userAssetList: userAssetList,
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
      console.log("RESPONSE:", userAssetList);

      userAssetList = userAssetList.map(image => {
        return ({ image: image});
        })

      if (xmlPackage.status === 200) {
        console.log("ASSET LIST:", userAssetList);

        if ( userAssetList[0] === "static/images/smiling-ready.png" ) {
          userAssetList.splice(0, 1);
        }

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
        <DragDropContextComp 
          onDragEnd={this.onDragEnd}
          userAssetList={this.state.userAssetList}
        />
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