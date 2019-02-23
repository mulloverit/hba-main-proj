"use strict";

class ImageManipulator extends React.Component {
  render () {
    return (
      <div>
        <h1>Hey</h1>
        <SearchBar />
      </div>
    );
  }
}

class SearchBar extends React.Component {
  render() {
    return (
      <form>
        <input type="text" placeholder="Search..." />
      </form>
    );
  }
}





ReactDOM.render(
  <ImageManipulator />,
  document.getElementById('unique')
  );