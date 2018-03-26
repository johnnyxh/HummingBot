import React, { Component } from 'react';
import PlaylistContainer from './playlist/PlaylistContainer';
import SettingsContainer from './settings/SettingsContainer';

export default class Content extends Component {
	getCurrentModuleView() {
		switch (this.props.currentView) {
			case 'Playlist':
				return (<PlaylistContainer />);
			default:
				return (<SettingsContainer />);
		}
	}

	render() {
		return (
			<div>
				{this.getCurrentModuleView()}
			</div>
		);
	}
}