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

const cloneDropObject = (inputDropObject, userAssetList) => {
  let validDroppedClone = new Object();

  validDroppedClone.asset = userAssetList[
                              inputDropObject.source.index].image;  
  validDroppedClone.draggableId =  Math.random().toString(36).substr(2, 9);
  validDroppedClone.key =  validDroppedClone.draggableId;

  return validDroppedClone
};

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
                    )} >
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
    this.props.handleRemoveAssetClick(event);
  }

  render() {
    return (
      <Droppable
        droppableId={this.props.board} >
         {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            style={getListStyle(snapshot.isDraggingOver)} >
            {this.props.userChapterBoardAssets.map((asset, index) => (
              <Draggable
                key={asset.key}
                draggableId={asset.draggableId} 
                board={this.props.board}
                index={index} >
                {(provided, snapshot) => (
                  <div
                    className="chapterBoardAsset"
                    ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    style={getItemStyle(
                      snapshot.isDragging,
                      provided.draggableProps.style
                    )} >
                    <form onSubmit={this.onRemoveAssetClick} >
                      <button
                        type="submit"
                        id="remove-chapterboard"
                        className="remove-chapterboard"
                        value={asset.key}
                        board={this.props.board}>
                        x
                      </button>
                      <img src={asset.asset} height="100" width="100"/>
                    </form>
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

  this.handleRemoveAssetClick = this.handleRemoveAssetClick.bind(this);
  }

  handleRemoveAssetClick(event) {
    event.preventDefault();
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
                {this.props.userChapterBoardList.map((board, index) => (
                  <ChapterBoard
                    droppableId="chapterBoard"
                    board={board.boardName}
                    key={board.key}
                    draggableId={board.draggableId}
                    index={index}
                    userChapterBoardAssets={board.boardAssets}
                    handleRemoveAssetClick={this.handleRemoveAssetClick} >
                  </ChapterBoard>
                ))}
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
    this.props.onClick(event);
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
      validDropped.destination.droppableId.includes("board")) {

        let targetBoard = this.state.userChapterBoardList.find(function(board) {
          if (board.boardName === validDropped.destination.droppableId) {
            return board  
          }
        });

        if ( targetBoard.boardAssets[0].asset === "static/images/smiling-ready.png" ) {
          targetBoard.boardAssets.splice(0, 1);
        }

        let validDroppedClone = cloneDropObject(validDropped, this.state.userAssetList);
        validDropped.destination.droppableId = "assetTray";

        targetBoard.boardAssets.splice(validDropped.destination.index,
          0, validDroppedClone);
        
        this.setState({
          userChapterBoardList: this.state.userChapterBoardList,
        });
    }

    else if (validDropped.source.droppableId === 
            validDropped.destination.droppableId) {

        let board = this.state.userChapterBoardList.find(function(board) {
          let foundAsset = board.boardAssets.find(function(asset) {
            if (validDropped.draggableId === asset.draggableId) {
              return asset
            }
          })

          if (foundAsset) {
            return board
          }
        })

        let assetOrder = reorder(
          board.boardAssets,
          validDropped.source.index,
          validDropped.destination.index
        );  

        board.boardAssets = assetOrder;

        this.setState({
          userChapterBoardList: this.state.userChapterBoardList,
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
    this.state.userChapterBoardList.push({
      boardAssets: [{ asset: "static/images/smiling-ready.png",
                     draggableId: Math.random().toString(36).substr(2, 9),
                     key: Math.random().toString(36).substr(2, 9) }],
      boardName: "board_" + Math.random().toString(36).substr(2, 9),
      chapterId: Math.random().toString(36).substr(2, 9),
      draggableId: Math.random().toString(36).substr(2, 9),
      key: Math.random().toString(36).substr(2, 9),
    });

    this.setState({
      userChapterBoardList: this.state.userChapterBoardList,
    });

  }

  onRemoveAssetClick(event) {
    event.preventDefault();

    const boardId = event.target[0].getAttribute("board");
    const assetForRemoval = event.target[0].getAttribute("value")
    console.log(boardId, assetForRemoval);

    // get board object from boardName
    let board = this.state.userChapterBoardList.find(function(boarditem) {
      if (boarditem.boardName === boardId) {
        return boarditem.chapterId
        };
    });

    // get list of assets associated with board
    let chapterBoardAssets = board.boardAssets;
    
    // remove item from list of assets
    let index = chapterBoardAssets.find(function(asset) {
      if (asset.key === assetForRemoval) {
        return chapterBoardAssets.indexOf(asset)
      };
    });

    chapterBoardAssets.splice(index, 1);

    if ( chapterBoardAssets[0] === "" || chapterBoardAssets[0] === undefined ) {
      chapterBoardAssets.splice(0, 1, {
        asset: "static/images/smiling-ready.png",
        draggableId: Math.random().toString(36).substr(2, 9),
        key: Math.random().toString(36).substr(2, 9),
      });
    }
    
    this.setState({
      userChapterBoardList: this.state.userChapterBoardList,
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