"use strict";

class ImageManipulator extends React.Component {
  render () {
    return (
      <div>
        <h1>Hey</h1>
        <br />
        <SearchBar />
        <br />
        <ImageUploadForm />
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


// form not working yet
// need to read: https://reactjs.org/docs/forms.html
// IF THIS WERE A CONTROLLED COMPONENT, following changes:
// however, image uploads are UNCONTROLLED COMPONENTS 
class ImageUploadForm extends React.Component {
  constructor(props) {
    super(props);
    this.fileInputOne = React.createRef();
    this.fileInputTwo = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = [
      this.fileInputOne.current.files[0].name,
      this.fileInputTwo.current.files[0].name,
      ];
    console.log(data);
    alert(
      `Selected files: ${
        data
      }`
    );
  }

  // handleUploadToServer() {
  //   const data = new FormData(event.target);
    
  //   fetch('/upload-inputs', {
  //     method: 'POST',
  //     body: data,
  //   })
  //   .then((response) => {response.json()});
  // }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit} method="POST" encType="multipart/form-data">
          <input type="file" name="img-1" id="img-1" ref={this.fileInputOne} />
          <input type="file" name="img-2" id="img-2" ref={this.fileInputTwo} />
          <button type="submit">Submit</button>
        </form>
      </div>
    );
  }
}

ReactDOM.render(
  <ImageManipulator />,
  document.getElementById('unique')
  );