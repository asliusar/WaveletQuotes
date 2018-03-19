import React from "react";
import autobind from "autobind-decorator";
import SelectField from "material-ui/SelectField";
import MenuItem from 'material-ui/MenuItem';
import styles from "./css/styles.css";
import {changeFrequency} from "../../actions/filter";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object
};


export class FrequencyPicker extends React.Component {

    @autobind
    handleFrequencyChangeEvent(event, val) {
        const {dispatch} = this.props;
        debugger;
        let frequency = this.props.filter.availableFrequency[val];
        dispatch(changeFrequency(frequency));
    };

    render() {
        debugger;
        console.log(this.props.filter.availableFrequency);
        return (
            <div className={styles.container}>
                <SelectField
                    floatingLabelText="Frequency"
                    value={this.props.filter.frequency}
                    onChange={this.handleFrequencyChangeEvent}
                >
                    {this.props.filter.availableFrequency.map((freq) =>
                        <MenuItem key={freq} value={freq} primaryText={freq}/>
                    )}
                </SelectField>
            </div>
        );
    }
}

FrequencyPicker.propTypes = propTypes;
export default FrequencyPicker;
