import React from "react";
import {connect} from "react-redux";
import styles from "./css/styles.css";
import {FilterContainer} from "../filter/filter";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
};


export class Flow extends React.Component {

    render() {
        return (
            <div className={styles.container}>
                <FilterContainer {...this.props} />
            </div>
        );
    }
}

Flow.propTypes = propTypes;

function mapStateToProps(state) {
    return state
}

export default connect(mapStateToProps)(Flow);