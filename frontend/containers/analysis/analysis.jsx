import React from "react";
import {connect} from "react-redux";
import {CandleStickChartPanToLoadMore} from "../../components/analisys/stockChart";
import {Controls} from "../../components/analisys/controls";
import {Details} from "./details";
import styles from "./css/styles.css";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
};


export class AnalysisContainer extends React.Component {

    render() {
        return (
            <div className={styles.container}>
                <CandleStickChartPanToLoadMore {...this.props.analysis}/>
                <Controls {...this.props}/>
                <Details {...this.props}/>
            </div>
        );
    }
}

AnalysisContainer.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter, analysis} = state;
    return {
        filter,
        analysis
    };
}

export default connect(mapStateToProps)(AnalysisContainer);