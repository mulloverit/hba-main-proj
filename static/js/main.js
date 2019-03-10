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
  render() {
    return (
      <Droppable
        droppableId={this.props.droppableId}
        userAssetList={this.props.userAssetList} >
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            style={getListStyle(snapshot.isDraggingOver)}
          >
            {this.props.userAssetList.map((item, index) => (
              <Draggable
                image={item.image}
                key={item.draggableId}
                draggableId={item.draggableId}
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
  constructor(props) {
    super(props);
    this.onRemoveAssetClick = this.onRemoveAssetClick.bind(this);
  }

  onRemoveAssetClick(event) {
    event.preventDefault();
    console.log("CLICKED Base");
    this.props.handleRemoveAssetClick(event);
  }

  render() {
    return (
      <Droppable
        droppableId="chapterBoardContainer"
        userChapterBoardAssets={this.props.userChapterBoardAssets} >
         {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            style={getListStyle(snapshot.isDraggingOver)} >
            {this.props.userChapterBoardAssets.map((board, index) => (
              <Draggable 
                board={board.boardId}
                key={board.key}
                draggableId={board.draggableId} 
                index={index}>
                {(provided, snapshot) => (
                  <div
                    className="chapterBoard"
                    ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    style={getItemStyle(
                      snapshot.isDragging,
                      provided.draggableProps.style
                    )} >
                </div>
                )}
              </Draggable>
            ))}
          </div>
        )}
      </Droppable>
    );
  }
}


class DragDropContextComp extends React.Component {
  constructor(props) {
    super(props);

  // CREATE CHPATERBOARDS & THEIR ASSETS FROM DICT HERE
  //userChapterBoardList={this.props.userChapterBoardList}
  //userChapterBoardDict={this.props.userChapterBoardDict}
  this.handleRemoveAssetClick = this.handleRemoveAssetClick.bind(this);
  }

  handleRemoveAssetClick(event) {
    event.preventDefault();
    console.log("CLICKED Context");
    this.props.onRemoveAssetClick(event);
  }

  render() {
    return (
        <DragDropContext
          onDragEnd={this.props.onDragEnd} >
          <div className="container">
            <div className="row">
              <div className="col-6">
                <AssetTray
                  droppableId="assetTray"
                  userAssetList={this.props.userAssetList}
                 />
              </div>
              <div className="col-6">
              <Droppable
                droppableId="chapterBoardContainer" >
                  {(provided, snapshot) => (
                    <div
                    ref={provided.innerRef}
                    style={getListStyle(snapshot.isDraggingOver)} >
                      {this.props.userChapterBoardList.map((board, index) => (
                        <Draggable 
                          board={board.boardId}
                          key={board.key}
                          draggableId={board.draggableId} 
                          index={index}>
                          {(provided, snapshot) => (
                            <div
                              className="chapterBoard"
                              ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                              style={getItemStyle(
                                snapshot.isDragging,
                                provided.draggableProps.style
                              )} >
                                <ChapterBoard
                                  droppableId="chapterBoard"
                                  board={board.boardId}
                                  key={board.boardId}
                                  draggableId={board.draggableId}
                                  index={index}
                                  userChapterBoardAssets={board.assetList}
                                  handleRemoveAssetClick={this.handleRemoveAssetClick} >
                                    <form onSubmit={this.onRemoveBoardClick} >
                                      <button
                                        type="submit"
                                        id="remove-chapterboard"
                                        className="remove-chapterboard"
                                        value={board.boardId}>
                                        x
                                      </button>
                                    </form>
                              </ChapterBoard>
                          </div>
                          )}
                        </Draggable>
                      ))}
                    </div>
                  )}
                </Droppable>
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

  // can this just be {this.props.onNewBoardClick(event)} in form?
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
    this.onRemoveAssetClick = this.onRemoveAssetClick.bind(this);

    // let userAssets = window.images;
    let userAssetList = ["https://s3.amazonaws.com/hackbright-image-upload-test/cmahon/173440d7-9111-4aa8-8ecd-f13ae916aee3_static/images/cmahon_IMG_4625.JPG"];
    let userChapters = window.chapters; // TO DO FIX THIS
    // let userAssetList = userAssets.substr(6).slice(0, -6).split("&#39;, &#39;");
    let userChapterBoardList = userChapters.substr(6).slice(0, -6).split("&#39;, &#39;"); // TO DO FIX THIS
    let userChapterBoardAssets = userChapters.substr(6).slice(0, -6).split("&#39;, &#39;"); // TO DO FIX THIS
    // COMBINE BOARDLIST WITH BOARD ASSETS AS DICT - ASSETS ARE VALUES TO BOARD KEY
    // DO THIS ON THE BACKEND
    console.log("FRESH LIST", userAssetList);
    userAssetList = userAssetList.map(image => {
        return ({ image: image,
                  draggableId: Math.random().toString(36).substr(2, 9),
                  key: Math.random().toString(36).substr(2, 9)
                });
    })
    console.log("FORMATTED LIST", userAssetList);

    let exampleBoardList = new Array();
    let exampleBoardOne = new Object();
    let exampleBoardTwo = new Object();
    exampleBoardList.splice(0, 0, exampleBoardOne);
    exampleBoardList.splice(0, 0, exampleBoardTwo);

    console.log("POPULATED BOARD LIST", exampleBoardList);

    userChapterBoardList = exampleBoardList.map(board => {
      board.boardId = Math.random().toString(36).substr(2, 9);
      board.key = Math.random().toString(36).substr(2, 9);
      board.draggableId = Math.random().toString(36).substr(2, 9);
      board.assetList = userAssetList;
    })
    
    // exampleBoardOne.boardId = Math.random().toString(36).substr(2, 9);
    // exampleBoardOne.key = Math.random().toString(36).substr(2, 9);
    // exampleBoardOne.draggableId = Math.random().toString(36).substr(2, 9);
    // exampleBoardTwo.boardId = Math.random().toString(36).substr(2, 9);
    // exampleBoardOne.assetList = userAssetList;
    // exampleBoardTwo.assetList = userAssetList;

    userChapterBoardList = exampleBoardList;
    console.log("Test BOARD LIST:", userChapterBoardList);

    userChapterBoardList.map((board, index) => (
      console.log("board.list", board.assetList)))
   

    this.state = {
      userAssetList: userAssetList,
      userChapterBoardList: userChapterBoardList,
      // userChapterBoardAssets: userChapterBoardAssets,
    };
  }

  onDragEnd(validDropped) {

    if (!validDropped.destination) {
      return;
    }

    if (validDropped.source.droppableId === "assetTray" &&
      validDropped.destination.droppableId === "assetTray") {
        
        const userAssetList = reorder(
          this.state.userAssetList,
          validDropped.source.index,
          validDropped.destination.index
        );  

        this.setState({
        userAssetList: userAssetList,
        });
    }

    else if (validDropped.source.droppableId === "assetTray" && 
      validDropped.destination.droppableId === "chapterBoard") {
  
        const validDroppedClone = new Object();

        validDroppedClone.asset = this.state.userAssetList[
                                    validDropped.source.index].image;
        validDroppedClone.draggableId =  Math.random().toString(36).substr(2, 9);
        validDroppedClone.key =  validDroppedClone.draggableId;
        validDropped.destination.droppableId = "assetTray";
        
        this.state.userChapterBoardAssets.splice(validDropped.destination.index,
          0, validDroppedClone);
        
        this.setState({
          userChapterBoardAssets: this.state.userChapterBoardAssets,
        });
    }

    else if (validDropped.source.droppableId === "chapterBoard" &&
      validDropped.destination.droppableId === "chapterBoard") {

        const userChapterBoardAssets = reorder(
          this.state.userChapterBoardAssets,
          validDropped.source.index,
          validDropped.destination.index
        );  

        this.setState({
          userChapterBoardAssets: userChapterBoardAssets,
        });
    } 
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
        return ({ image: image,
                  draggableId: Math.random().toString(36).substr(2, 9)
                });
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
    // THIS FUNCTION IS TO DO //
    userChapterBoardList.push("new");
  }

  onRemoveAssetClick(event) {
    event.preventDefault();
    console.log("CLICKED Main");
    console.log(event.target[0].getAttribute("value"));
    console.log(this.state.userChapterBoardAssets);

    const chapterBoardAssets = this.state.userChapterBoardAssets
    const removeItem = event.target[0].getAttribute("value");
    const result = chapterBoardAssets.filter(asset => 
      asset.draggableId === removeItem);
    const idx = chapterBoardAssets.findIndex(asset => 
      asset.draggableId === removeItem);

    console.log("RESULT", result);
    console.log("IDX", idx);

    chapterBoardAssets.splice(idx, 1);

    console.log("AFTER RM", chapterBoardAssets[0])

    if ( chapterBoardAssets[0] === "" || chapterBoardAssets[0] === undefined ) {
      
      chapterBoardAssets.splice(0, 1, {
        asset: "static/images/smiling-ready.png",
        draggableId: Math.random().toString(36).substr(2, 9),
      });
    }
    
    this.setState({
      userChapterBoardAssets: this.state.userChapterBoardAssets,
    });
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
          onRemoveAssetClick={this.onRemoveAssetClick}
          userAssetList={this.state.userAssetList}
          userChapterBoardList={this.state.userChapterBoardList}
          // userChapterBoardAssets={this.state.userChapterBoardAssets}
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