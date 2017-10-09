import React, { Component } from 'react';
import { Button, Row, Col, Card, CardBody } from 'reactstrap';

import healthIcon from '../keke2.gif';

export default class Header extends Component {
	render() {
		return (
			<Card>
				<CardBody>
					<Row>
						<Col xs="12" md="3"><a href="#"><img onClick={this.props.updateHealth} height="100px" className="rounded mx-auto d-block" src={healthIcon} /></a></Col>
						<Col xs="12" lg="9">
							<Col xs="12" md="4">
								<h2><small>Status</small></h2>
								<h2><strong>{this.props.health}</strong></h2>
							</Col>
							<Col xs="12" md="4">
								<h2><small>Uptime</small></h2>
								<h2><strong>12h:23m:37s</strong></h2>
							</Col>
							<Col xs="12" md="4">
								<h2><small>Server</small></h2>
								<h2><strong>Dedbois</strong></h2>
							</Col>
							<Col xs="0" md="10" />
							<Col className="md-bottom-right-align" xs="12" lg="2">
								<Button color="primary" size="lg" block>Restart Bot</Button>
							</Col>
						</Col>
					</Row>
				</CardBody>
			</Card>
		);
	}
}