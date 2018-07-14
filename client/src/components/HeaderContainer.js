import { connect } from 'react-redux';
import { updateHealth, restartBot } from '../actions/actions';
import Header from './Header';

const mapStateToProps = (state) => {
    return {
        status: state.botReducer.status,
        server: state.botReducer.servers[0],
        uptime: state.botReducer.uptime,
        pendingRestart: state.botReducer.pendingRestart
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        updateHealth: () => {
            dispatch(updateHealth())
        },
        restartBot: (server) => {
        	dispatch(restartBot(server))
        	dispatch(updateHealth())
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);