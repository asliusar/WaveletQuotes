import React from "react";
import {connect} from "react-redux";
import styles from "./css/styles.css";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
};


export class Indicators extends React.Component {

    render() {
        return (
            <div className={styles.container}>
            </div>
        );
    }
}

Indicators.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter} = state;
    return {
        filter
    };
}

export default connect(mapStateToProps)(Indicators);