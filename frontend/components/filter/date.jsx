import React from "react";
import autobind from 'autobind-decorator'
import DatePicker from "material-ui/DatePicker";
import styles from "./css/styles.css";
import {changeStartDate, changeEndDate} from "../../actions/filter";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object
};


export class RangeDatePicker extends React.Component {

    @autobind
    handleStartDateChangeEvent(event, date) {
        const {dispatch} = this.props;
        dispatch(changeStartDate(date));
    };

    @autobind
    handleEndDateChangeEvent(event, date) {
        const {dispatch} = this.props;
        dispatch(changeEndDate(date));
    };


    render() {
        return (
            <div className={styles.container}>
                <DatePicker
                    onChange={this.handleStartDateChangeEvent}
                    hintText="Start date"
                    mode="landscape"
                    autoOk={true}/>
                <DatePicker
                    onChange={this.handleEndDateChangeEvent}
                    hintText="End date"
                    mode="landscape"
                    autoOk={true}/>
            </div>
        );
    }
}

RangeDatePicker.propTypes = propTypes;
export default RangeDatePicker;
