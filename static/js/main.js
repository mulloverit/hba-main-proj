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
    this.state = {value: ''};

  this.handleChange = this.handleChange.bind(this);
  this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    
    fetch('/upload-inputs', {
      method: 'POST',
      body: data,
    })
    .then((response) => {response.json()});
  }

  render() {
    return (
      <div>
        <form action="/upload-inputs" className="user-input-images-form" method="POST" encType="multipart/form-data">
          <input type="file" name="img-1" id="img-1" value={this.state.value} onChange={this.handleChange} />
          <input type="file" name="img-2" id="img-2" value={this.state.value} onChange={this.handleChange} />
          <input type="submit" name="upload-inputs" value="Upload" id="user-image-submission"></input>
        </form>
      </div>
    );
  }
}

ReactDOM.render(
  <ImageManipulator />,
  document.getElementById('unique')
  );