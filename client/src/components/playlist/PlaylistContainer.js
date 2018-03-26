import { connect } from 'react-redux';
import { updatePlaylist } from '../../actions/actions';
import Playlist from './Playlist';

const mapStateToProps = (state) => {
	return {
		songs: state.botReducer.songs,
		currentSong: state.botReducer.currentSong
	}
};

const mapDispatchToProps = (dispatch) => {
	return {
		updatePlaylist: () => {
			dispatch(updatePlaylist())
		}
	};
}

export default connect(mapStateToProps, mapDispatchToProps)(Playlist);