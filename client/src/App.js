import React, { Component } from 'react';
import keke1 from './keke1.gif';
import keke2 from './keke2.gif';
import keke3 from './keke3.gif';
import './App.css';

class App extends Component {
  kekeArray = [keke1, keke2, keke3];

  handleImageClick() {
    // Honestly this is just to stop hummingbot from going to sleep on free heroku
    window.location.reload();
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>HummingBot is UP</h2>
        </div>
        <p className="App-intro">
          <a href="#"><img onClick={this.handleImageClick} src={this.kekeArray[Math.floor(Math.random() * 3)]}/></a>
        </p>
        <p>
          Click every now and then to keep me up.
        </p>
      </div>
    );
  }
}

export default App;
