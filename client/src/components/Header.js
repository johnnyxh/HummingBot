import React, { Component } from 'react';
import { Button, Row, Col, Card, CardBody } from 'reactstrap';

import healthIcon from '../keke2.gif';

export default class Header extends Component {

	componentDidMount() {
		this.props.updateHealth()
		this.healthTimer = setInterval(this.props.updateHealth, 5000);
	}

	componentWillUnmount() {
		clearInterval(this.healthTimer);
	}

	render() {
		return (
			<Card>
				<CardBody>
					<Row>
						<Col xs="12" lg="3"><img alt='' height="100px" className="rounded mx-auto d-block" src={healthIcon} /></Col>
						<Col xs="12" lg="9">
							<Row>
								<Col xs="12" md="4">
									<h6><small>Status</small></h6>
									<h5><strong>{this.props.status}</strong></h5>
								</Col>
								<Col xs="12" md="4">
									<h6><small>Uptime</small></h6>
									<h5><strong>{this.props.uptime}</strong></h5>
								</Col>
								<Col xs="12" md="4">
									<h6><small>Server</small></h6>
									<h5><strong>{this.props.server}</strong></h5>
								</Col>
								<Col xs="0" md="10" />
								<Col className="md-bottom-right-align" xs="12" lg="2">
									<Button color="primary" size="sm" block disabled={this.props.pendingRestart} onClick={this.props.restartBot}>Restart Bot</Button>
								</Col>
							</Row>
						</Col>
					</Row>
				</CardBody>
			</Card>
		);
	}
}