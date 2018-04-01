import React from "react";
import {connect} from "react-redux";
import styles from "./css/styles.css";
import {RangeDatePicker} from "../../components/filter/date";
import {CurrencyPairPicker} from "../../components/filter/currencyPair";
import {FrequencyPicker} from "../../components/filter/frequency";
import {LoadButton} from "../../components/filter/loadButton";


const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
};


export class FilterContainer extends React.Component {

    render() {
        return (
            <div className={styles.container}>
                <CurrencyPairPicker {...this.props} />
                <RangeDatePicker {...this.props} />
                <FrequencyPicker {...this.props} />
                <LoadButton {...this.props} />
            </div>
        );
    }
}

FilterContainer.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter} = state;
    return {
        filter
    };
}

export default connect(mapStateToProps)(FilterContainer);