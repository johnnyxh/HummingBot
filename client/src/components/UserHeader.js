import React, { Component } from 'react';
import { Col, Row } from 'reactstrap';

export default class UserHeader extends Component {
	componentDidMount() {
		this.props.getUserInfo();
	}

	renderLoginPrompt() {
		return (<span><a href='/api/auth'>Login</a> with Discord</span>)
	}

	renderLoggedIn() {
		return (
			<span>
				<img style={{ 'margin-right': 10 }} width='32' height='32' src={this.props.user.avatarUrl}/>
				<a href='#'>{this.props.user.username}</a> <a href='/api/revoke'>logout</a>
			</span>
		)
	}

	render() {
		return (
			<Row>
				<Col style={{ 'text-align': 'right', 'padding': 10 }}>
					{this.props.user ? this.renderLoggedIn() : this.renderLoginPrompt()}
				</Col>
			</Row>
		);
	}
}