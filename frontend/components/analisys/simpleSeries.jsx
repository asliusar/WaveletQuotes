import React, {Component} from "react";
import autobind from 'autobind-decorator';
import PropTypes from "prop-types";
import LineSeries from "react-stockcharts/lib/series/LineSeries";
import {connect} from "react-redux";
import StraightLine from "react-stockcharts/lib/series/StraightLine";

export class SimpleSeries extends Component {
    @autobind
    yAccessor(d) {
        const {accessor} = this.props;
        return accessor(d);
    }

    render() {
        debugger;
        return (
            <g>
                <LineSeries
                    yAccessor={this.yAccessor}
                    stroke="#FF0000"
                    fill="none"/>
                <StraightLine
                    yValue={0.5}/>
            </g>
        );
    }
}

SimpleSeries.propTypes = {
    accessor: PropTypes.func.isRequired,
};

function mapStateToProps(state) {
    return state
}

export default connect(mapStateToProps)(SimpleSeries);