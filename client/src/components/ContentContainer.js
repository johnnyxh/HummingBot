import { connect } from 'react-redux';
import Content from './Content';

const mapStateToProps = (state) => {
    return {
        currentView: state.navigationReducer.currentView
    };
};

export default connect(mapStateToProps)(Content);