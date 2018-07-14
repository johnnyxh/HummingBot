import { connect } from 'react-redux';
import { getUserInfo } from '../actions/actions';
import UserHeader from './UserHeader';

const mapStateToProps = (state) => {
    return {
        user: state.botReducer.user
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getUserInfo: () => {
            dispatch(getUserInfo());
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(UserHeader);