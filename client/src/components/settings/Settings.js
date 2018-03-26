import React, { Component } from 'react';
import { Card, CardBody, CardTitle } from 'reactstrap';

export default class Settings extends Component {
	render() {
		return (
			<Card>
				<CardBody>
					<CardTitle>
						Settings
					</CardTitle>
					<h2 className='text-center text-muted'>
						Coming Soon...
					</h2>
				</CardBody>
			</Card>
		);
	}
}