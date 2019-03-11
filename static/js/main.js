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

const cloneDropObject = (inputDropObject) => {
  let validDroppedClone = new Object();

  validDroppedClone.asset = this.state.userAssetList[
                              inputDropObject.source.index].image;
  validDroppedClone.draggableId =  Math.random().toString(36).substr(2, 9);
  validDroppedClone.key =  validDroppedClone.draggableId;

  return validDroppedClone
};
  
// const convertWindowChapters = (userChapters) => {
  
//   console.log("Incoming", userChapters);
//   let regex = /&#39;/gi;
//   // let regex2 = /\'/gi; 
//   // let regex3 = /\[/gi;
//   // let regex4 = /\]/gi;
//   let userChapterBoards = [];
//   let userChapterBoardList = userChapters.replace(regex, "").substr(1).slice(0, -1); // STRING
//   userChapterBoardList = userChapterBoardList.text()
//   JSON.parse(userChapterBoardList);
//   console.log("before mapping", userChapterBoardList);


  // let userChapterBoardList = userChapters.replace(regex, "'").replace(
  //                             regex2, "").substr(1).slice(0, -1).split(
  //                             "],"); // STRING
  // userChapterBoardList.map(board => {
  //   board = board.replace(regex3, "").replace(regex4, "").split(": ")
  //   board.boardName = board[0].replace(" ", "")
  //   board.boardAssets = board[1].split(", ")
  //   board.boardId = Math.random().toString(36).substr(2, 9);
  //   board.key = Math.random().toString(36).substr(2, 9);
  //   board.draggableId = Math.random().toString(36).substr(2, 9);
  //   userChapterBoards.splice(0, 0, board);
  // })

  // return userChapterBoards;
// }


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
                                  key={board.key}
                                  draggableId={board.draggableId}
                                  index={index}
                                  userChapterBoardAssets={board.boardAssets}
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

    let userAssets = window.images;
    let userAssetList = userAssets.substr(6).slice(0, -6).split("&#39;, &#39;");
    userAssetList = userAssetList.map(image => {
        return ({ image: image,
                  draggableId: Math.random().toString(36).substr(2, 9),
                  key: Math.random().toString(36).substr(2, 9)
                });
    })
    console.log("userAssets", userAssetList);

    let userChapters = window.chapters;
    console.log("userChapters window", userChapters);
    console.log(typeof userChapters);
    userChapters.map(chapter => {
      chapter.key = Math.random().toString(36).substr(2, 9)
      chapter.draggableId = Math.random().toString(36).substr(2, 9)
      chapter.chapterId = Math.random().toString(36).substr(2, 9)
      chapter.boardAssets = chapter.boardAssets.map(asset => {
        asset = { asset: asset }
        asset.key = Math.random().toString(36).substr(2, 9)
        asset.draggableId = Math.random().toString(36).substr(2, 9)
        return asset
      })
    })
    console.log("userChapterBoards:", userChapters);

    this.state = {
      userAssetList: userAssetList,
      userChapterBoardList: userChapters,
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
  

        let validDroppedClone = cloneDropObject(validDropped);
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