"use strict";

FilePond.setOptions({
  server: {
    url: '/upload-inputs',
  }
})

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create( inputElement );

class ImageManipulator extends React.Component {
  render () {
    return (
      <div>
        <h1>Hey</h1>
        <br />
        <SearchBar />
        <br />
        <ImageUploadForm />
        <br />
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

class FilePondTest extends React.Component {
  constructor(props) {
    super(props);
    const inputElement = document.querySelector('input[type="file"]');
    const pond = FilePond.create( inputElement );

  }

  render() {
    return (
      <pond />
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

  handleUploadToServer(data) {
    
    fetch('/upload-inputs', {
      method: 'POST',
      body: data,
    })
    .then((response) => {response.json()});
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData();
    data.append('file1', this.fileInputOne.current.files);
    data.append('file2', this.fileInputTwo.current.files);


    fetch('/upload-inputs', {
      method: 'POST',
      body: data,
    })
    .then((response) => {response.json()});

    // const jsonResponse = handleUploadToServer(data);
    // return jsonResponse;
  }

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