import React from "react";
import autobind from "autobind-decorator";
import styles from "./css/styles.css";
import {loadStockData} from "../../actions/filter";
import RaisedButton from "material-ui/RaisedButton";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object
};


export class LoadButton extends React.Component {

    @autobind
    handleLoadButtonClicked() {
        const {dispatch} = this.props;
        const {currencyPair, frequency, startDate, endDate} = this.props.filter;
        dispatch(loadStockData(currencyPair, frequency, startDate, endDate));
    };

    render() {
        const classes = [styles.container, styles.load_button].join(" ");

        return (
            <span className={classes}>
                <RaisedButton label="Load" primary={true} onClick={this.handleLoadButtonClicked}/>
            </span>
        );
    }
}

LoadButton.propTypes = propTypes;
export default LoadButton;
