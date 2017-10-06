import { connect } from 'react-redux';
import { updateHealth } from '../actions/actions';
import Header from './Header';

const mapStateToProps = (state) => {
	return {
		health: state.botReducer.health
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		updateHealth: () => {
			dispatch(updateHealth())
		}
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);