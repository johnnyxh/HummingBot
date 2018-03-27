import React, { Component } from 'react';
import { Col, Card, CardBody, Progress, Row, Table } from 'reactstrap';

import { getTimestamp } from '../../utils/timestamps';

export default class PlaylistCurrentItem extends Component {
	renderDuration() {
		if (this.props.isLive) {
			return (<p style={{'text-align': 'right'}}><strong style={{'color': 'red'}}>&#x25cf; LIVE</strong></p>)
		}
		return (<p style={{'text-align': 'right'}}>{getTimestamp(this.props.timestamp)}/{getTimestamp(this.props.duration)}</p>)
	}

	render() {
		return(
			<Card>
				<CardBody>
					<Row>
						<Col md='auto'>
							<img className='rounded playlist-current-thumbnail' src={`https://img.youtube.com/vi/${this.props.videoId}/hqdefault.jpg`} alt='' />
						</Col>
						<Col>
							<Table id='playlist-current-content'>
								<tr>
									<td valign='top'>
										<h3 style={{color: 'gray'}}>Now Playing</h3>
										<h5 style={{color: 'gray', 'margin-top': '10px'}}><small>Requested by: {this.props.requester}</small></h5>
									</td>
								</tr>
								<tr>
									<td id='valign-bottom'>
										<h2><strong>{this.props.title}</strong></h2>
										<h4 style={{'margin-top': '10px'}}>{this.props.uploader}</h4>
										{this.renderDuration()}
										<Progress color='danger' value={this.props.isLive ? 100 : (this.props.timestamp/this.props.duration) * 100} />
									</td>
								</tr>
							</Table>
						</Col>
					</Row>
				</CardBody>
			</Card>
		);
	}
}