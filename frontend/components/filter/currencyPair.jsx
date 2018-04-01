import React from "react";
import autobind from "autobind-decorator";
import AutoComplete from "material-ui/AutoComplete";
import styles from "./css/styles.css";
import {changeCurrencyPair} from "../../actions/filter";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object
};


export class CurrencyPairPicker extends React.Component {

    @autobind
    handleCurrencyPairChangeEvent(event, pair) {
        console.log(event, pair);
        const {dispatch} = this.props;
        dispatch(changeCurrencyPair(event));
    };


    render() {
        const classes = [styles.container, styles.input_field].join(" ");

        return (
            <span className={classes}>
                <AutoComplete
                    hintText="Currency pair"
                    dataSource={this.props.filter.commonCurrencies}
                    onUpdateInput={this.handleCurrencyPairChangeEvent}
                />
            </span>
        );
    }
}

CurrencyPairPicker.propTypes = propTypes;
export default CurrencyPairPicker;
