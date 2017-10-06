import React, { Component } from 'react';
import keke1 from '../keke1.gif';
import keke2 from '../keke2.gif';
import keke3 from '../keke3.gif';

export default class Header extends Component {
  	kekeArray = [keke1, keke2, keke3];

	render() {
		return (
			<p className='text-center'>
	          <a href='#'><img alt='Who cares' onClick={this.props.updateHealth} src={this.kekeArray[Math.floor(Math.random() * this.kekeArray.length)]}/></a>
	        {this.props.health}
	        </p>
        );
	}
}