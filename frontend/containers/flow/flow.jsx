import React from "react";
import {connect} from "react-redux";
import styles from "./css/styles.css";
import {FilterContainer} from "../filter/filter";
import {AnalysisContainer} from "./../analysis/analysis";
import {loadStockData} from "../../actions/filter";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
    analysis: React.PropTypes.object
};


export class Flow extends React.Component {

    componentWillMount() {
        console.log(3);
        const {dispatch} = this.props;
        dispatch(loadStockData());
    }

    render() {
        return (
            <div className={styles.container}>
                <FilterContainer {...this.props} />
                {
                    this.props.analysis.data &&
                    <AnalysisContainer {...this.props}/>
                }
            </div>
        );
    }
}

Flow.propTypes = propTypes;

function mapStateToProps(state) {
    return state
}

export default connect(mapStateToProps)(Flow);