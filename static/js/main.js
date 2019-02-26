"use strict";

FilePond.setOptions({
  server: {
    url: '/upload-inputs',
  }
})

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create( inputElement );

class DynamicGreeting extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
            <br />
            <h1>Hey</h1>
            <br />
          </div>
        </div>
      </div>
    );
  }
}

class ImageUploader extends React.Component {
  render () {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
            <br />
            <ImageUploadForm />
            <br />
          </div>
        </div>
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
    
    const formData = new FormData();
    const fileOne = new File(this.fileInputOne.current.files, this.fileInputOne.current.files.name);
    const fileTwo = new File(this.fileInputTwo.current.files, this.fileInputOne.current.files.name);
    const postUrl = "/upload-inputs"
    const xmlPackage = new XMLHttpRequest();

    formData.append('file1', fileOne);
    formData.append('file2', fileTwo);
    xmlPackage.open("POST", postUrl);
    xmlPackage.send(formData)
  }
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-6">
              <form onSubmit={this.handleSubmit} method="POST" encType="multipart/form-data">
                <input type="file" name="img-1" id="img-1" ref={this.fileInputOne} />
                <input type="file" name="img-2" id="img-2" ref={this.fileInputTwo} />
                <button type="submit">Submit</button>
              </form>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <ImageUploader />,
  document.getElementById('manual-uploads')
);

ReactDOM.render(
  <DynamicGreeting />,
  document.getElementById('dynamic-greeting')
);



