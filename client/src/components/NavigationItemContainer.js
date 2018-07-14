import { connect } from 'react-redux';
import { navigationChange } from '../actions/actions';
import NavigationItem from './NavigationItem';

const mapStateToProps = (state) => {
    return {
        currentView: state.navigationReducer.currentView
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        changeNav: (view) => {
            dispatch(navigationChange(view));
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(NavigationItem);