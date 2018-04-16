import React from "react";
import autobind from "autobind-decorator";
import {connect} from "react-redux";
import styles from "./css/styles.css";
import RaisedButton from "material-ui/RaisedButton";
import {toggleDetails, toggleRecommendations} from "../../actions/analysis";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
    data: React.PropTypes.object
};


export class Controls extends React.Component {

    @autobind
    handleWaveletAnalysisButtonClicked() {
        const {dispatch, analysis} = this.props;
        if (analysis.data.waveletDetails) {
            dispatch(toggleDetails());
        }
    };

    @autobind
    handleRecommendationsButtonClicked() {
        const {dispatch, analysis} = this.props;
        if (analysis.data.waveletDetails) {
            dispatch(toggleRecommendations());
        }
    };

    render() {
        const classes = [styles.container, styles.control_button].join(" ");

        return (
            <div className={classes}>
                <RaisedButton label="Recommendations" primary={true}
                              onClick={this.handleRecommendationsButtonClicked}/>

                <RaisedButton label="Wavelet analysis" primary={true}
                              onClick={this.handleWaveletAnalysisButtonClicked}/>
            </div>
        );
    }
}

Controls.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter} = state;
    return {
        filter
    };
}

export default connect(mapStateToProps)(Controls);