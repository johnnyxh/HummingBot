import React, { Component } from 'react';
import { Card, CardBody, CardTitle, Table } from 'reactstrap';

import PlaylistItem from './PlaylistItem';
import PlaylistCurrentItem from './PlaylistCurrentItem';

export default class Playlist extends Component {
	componentDidMount() {
		// Using setTimeout to ensure we wait for pending playlist calls
		const update = function () {
			this.props.updatePlaylist();
			this.updateTimer = setTimeout(update, 5000)
		}.bind(this);
		update();
	}

	componentWillUnmount() {
		clearTimeout(this.updateTimer);
	}

	renderPlaylistCurrentItem() {
		if (this.props.currentSong !== null) {
			return (
				<div>
					<PlaylistCurrentItem 
						videoId={this.props.currentSong.videoId} 
						title={this.props.currentSong.title}
						uploader={this.props.currentSong.uploader}
						requester={this.props.currentSong.requester}
						timestamp={this.props.currentSong.timestamp}
						duration={this.props.currentSong.duration}
						isLive={this.props.currentSong.isLive} />
					<br/> 
				</div>
			);
		}
	}

	renderPlaylistItems() {
		return this.props.songs.map((song, index) => {
				return (
					<tr>
						<td>
							<PlaylistItem
								position={++index}
								videoId={song.videoId}
								title={song.title}
								uploader={song.uploader}
								requester={song.requester}
								duration={song.duration}
								isLive={song.isLive} />
						</td>
					</tr>
				)
			});
	}

	render() {
		return (
			<div>
				{this.renderPlaylistCurrentItem()}
				<Card>
					<CardBody>
						<CardTitle>
							{this.props.songs.length ? 'Coming Up' : 'No Songs Queued'}
						</CardTitle>
						<Table hover size='sm'>
							<tbody>
								{this.renderPlaylistItems()}
							</tbody>
						</Table>
					</CardBody>
				</Card>
			</div>
		);
	}
}