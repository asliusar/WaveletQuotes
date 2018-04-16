import React from "react";
import Divider from "material-ui/Divider";
import {connect} from "react-redux";
import styles from "./css/styles.css";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
    data: React.PropTypes.object
};

export class Recommendations extends React.Component {
    render() {
        debugger;
        const {analysis} = this.props;
        let prediction = (analysis.data.prediction == "true");
        let operation = prediction ? "Buy" : "Sell";

        return (
            <div className={styles.container}>
                {
                    analysis.showRecommendations &&
                    <div>
                        <Divider/>
                        <span className={styles.recommendation_text}>Recommendations: </span>
                        <span className={styles.recommendation_text}>{operation}</span>
                        <Divider/>
                    </div>
                }
            </div>
        );
    }
}

Recommendations.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter} = state;
    return {
        filter
    };
}

export default connect(mapStateToProps)(Recommendations);