import React, { Component } from 'react';
import { Row, Col } from 'reactstrap';
import FontAwesome from 'react-fontawesome';


export default class Footer extends Component {
	render() {
		return (
			<Row style={{'margin-top': '5px', color: 'gray'}}>
				<Col xs={{size: 'auto', offset: 5}}>
					<FontAwesome style={{'vertical-align': 'middle'}} name='github' size='2x'/>
					<small>johnnyxh</small>
				</Col>
			</Row>
		)
	}
}