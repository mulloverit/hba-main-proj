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

class AssetTray extends React.Component {
  constructor(props){
    super(props);
  }
  
  render() {
    return (
      <Droppable
        droppableId={this.props.droppableId}
        userAssetList={this.props.userAssetList}
        userChapterBoardList={this.props.userChapterBoardList}
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

class ChapterBoard extends React.Component {
  constructor(props){
    super(props);
  }
  
  render() {
    return (
      <Droppable
        droppableId={this.props.droppableId}
        userChapterBoardList={this.props.userChapterBoardList}
      >
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            style={getListStyle(snapshot.isDraggingOver)}
          >
            {this.props.userChapterBoardList.map((item, index) => (
              <Draggable 
                key="test"
                draggableId="test"
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
          <div className="container">
            <div className="row">
              <div className="col-6">
                <AssetTray
                  droppableId="droppable"
                  userAssetList={this.props.userAssetList}
                 />
              </div>
              <div className="col-6">
                <ChapterBoard
                  droppableId="chapterBoard"
                  userChapterBoardList={this.props.userChapterBoardList}
                />
              </div>
            </div>
          </div>
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

class NewChapterBoard extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {
    event.preventDefault();
    this.props.onNewBoardClick(event);
  }

  render() {
    return (
      <form
        onClick={this.handleClick}>
        <button type="submit">New chapter board</button>
      </form>
    );
  }
}

class MainPageArea extends React.Component {
  constructor(props) {
    super(props);
    this.onDragEnd = this.onDragEnd.bind(this);
    this.handleAssetUpload = this.handleAssetUpload.bind(this);
    this.handleNewBoardClick = this.handleNewBoardClick.bind(this);

    let userAssets = window.images;
    let userChapters = window.chapters;
    let userAssetList = userAssets.substr(6).slice(0, -6).split("&#39;, &#39;");
    let userChapterBoardList = userChapters.substr(6).slice(0, -6).split("&#39;, &#39;");


    // provide default image if user has no assets
    if ( userAssetList[0] === "" ) {
      userAssetList.splice(0, 1, "static/images/smiling-ready.png");
    }

    userAssetList = userAssetList.map(image => {
      return ({ image: image});
    })

    if ( userChapterBoardList[0] === "" ) {
      userChapterBoardList.splice(0, 1, "static/images/smiling-ready.png");
    }
    
    userChapterBoardList = userChapterBoardList.map(board => {
      return ({ board: board});
    })

    this.state = {
      userAssetList: userAssetList,
      userChapterBoardList: userChapterBoardList,
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

  handleAssetUpload(file) {
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

  handleNewBoardClick() {
    userChapterBoardList.push("new");
  }

  render() {
    return (
      <div>
        <NewChapterBoard 
          onClick={this.handleNewBoardClick}/>
        <AssetUpload 
          onSubmit={this.handleAssetUpload}
          />
        <DragDropContextComp 
          onDragEnd={this.onDragEnd}
          userAssetList={this.state.userAssetList}
          userChapterBoardList={this.state.userChapterBoardList}
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