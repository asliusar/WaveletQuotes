import React from "react";
import {fetchShowsByFilter} from "../../actions/list/list";
import ShowList from "./../../components/list/list";
import {connect} from "react-redux";
import styles from "./css/styles.css";

const propTypes = {
    getMeEvents: React.PropTypes.array,
    dispatch: React.PropTypes.func.isRequired,
    showList: React.PropTypes.object,
};


class ShowListContainer extends React.Component {

    componentWillMount() {
        const {dispatch} = this.props;
        dispatch(fetchShowsByFilter(this.props.showFilter))
    }

    render() {
        return (
            <div className={styles.container}>
                <ShowList {...this.props} />
            </div>
        );
    }
}

ShowListContainer.propTypes = propTypes;

function mapStateToProps(state) {
    const {showList} = state;
    return {
        showList
    };
}

export default connect(mapStateToProps)(ShowListContainer);