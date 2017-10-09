import { connect } from 'react-redux';
import { updateHealth, restartBot } from '../actions/actions';
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
        },
        restartBot: () => {
        	dispatch(restartBot())
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);