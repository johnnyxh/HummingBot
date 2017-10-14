import React, { Component } from 'react';
import { Button, Row, Col, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

export default class Popup extends Component {
	render() {
		return (
			<Modal isOpen={this.props.isOpen} toggle={this.props.toggle}>
				<ModalHeader>Header</ModalHeader>
				<ModalBody>Body</ModalBody>
				<ModalFooter>
					<Button color="primary">Do Something</Button>{' '}
            		<Button color="secondary">Cancel</Button>
				</ModalFooter>
			</Modal>
		);
	}
}