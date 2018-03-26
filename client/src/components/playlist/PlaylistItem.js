import React, { Component } from 'react';
import { Media, Col, Row } from 'reactstrap';

import { getTimestamp } from '../../utils/timestamps';

export default class PlaylistItem extends Component {

	constructor(props) {
		super(props)
		this.onSelected = this.onSelected.bind(this);
	}

	onSelected(event) {
		window.open(`https://www.youtube.com/watch?v=${this.props.videoId}`);
	}

	render() {
		return(
			<Row style={{ cursor: 'pointer' }} onClick={this.onSelected}>
				<Col className='playlist-item-vertical-align' xs='auto'>{this.props.position}</Col>
				<Col>
					<Media>
						<Media left>
							<img className='rounded playlist-item-thumbnail' src={`https://img.youtube.com/vi/${this.props.videoId}/1.jpg`} alt='' />
						</Media>
						<Media body className='playlist-item-body play'>
							<h5>
								{this.props.title}
							</h5>
							<span>{this.props.uploader}</span>
						</Media>
						<Media className='sm-hide' right>
							<span className='playlist-item-vertical-align playlist-item-requester'>Requested by: {this.props.requester}</span>
							<span className='playlist-item-vertical-align'>{getTimestamp(this.props.duration)}</span>
						</Media>
					</Media>
				</Col>
			</Row>
		)
	}
}