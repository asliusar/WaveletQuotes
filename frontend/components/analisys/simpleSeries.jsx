import React, {Component} from "react";
import autobind from 'autobind-decorator';
import PropTypes from "prop-types";
import LineSeries from "react-stockcharts/lib/series/LineSeries";

class SimpleSeries extends Component {
    constructor(props) {
        super(props);
    }

    @autobind
    yAccessor(d) {
        const {accessor} = this.props;
        return accessor(d) && accessor(d).macd;
    }

    render() {
        return (
            <g className={className}>
                <LineSeries
                    yAccessor={this.yAccessor}
                    stroke="#FF0000"
                    fill="none"/>
                {/*<StraightLine*/}
                    {/*stroke={zeroLineStroke}*/}
                    {/*opacity={zeroLineOpacity}*/}
                    {/*yValue={0}/>*/}
            </g>
        );
    }
}

SimpleSeries.propTypes = {
    yAccessor: PropTypes.func.isRequired,
};

export default SimpleSeries;
