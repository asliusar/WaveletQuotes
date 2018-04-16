import {format} from "d3-format";
import {timeFormat} from "d3-time-format";
import React from "react";
import PropTypes from "prop-types";
import {ChartCanvas, Chart} from "react-stockcharts";
import {AreaSeries, LineSeries} from "react-stockcharts/lib/series";
import {XAxis, YAxis} from "react-stockcharts/lib/axes";
import {
    CrossHairCursor,
    EdgeIndicator,
    CurrentCoordinate,
    MouseCoordinateX,
    MouseCoordinateY
} from "react-stockcharts/lib/coordinates";
import {discontinuousTimeScaleProviderBuilder} from "react-stockcharts/lib/scale";
import {OHLCTooltip, MovingAverageTooltip} from "react-stockcharts/lib/tooltip";
import {ema, sma, macd} from "react-stockcharts/lib/indicator";
import {fitWidth} from "react-stockcharts/lib/helper";
import {SimpleSeries} from "./simpleSeries";
import StraightLine from "react-stockcharts/lib/series/StraightLine";


function getMaxUndefined(calculators) {
    return calculators.map(each => each.undefinedLength()).reduce((a, b) => Math.max(a, b));
}
const LENGTH_TO_SHOW = 5000;


const propTypes = {
    data: PropTypes.object.isRequired,
    width: PropTypes.number.isRequired,
    ratio: PropTypes.number.isRequired,
    type: PropTypes.oneOf(["svg", "hybrid"]).isRequired,
};

export class CandleStickChartPanToLoadMore extends React.Component {
    constructor(props) {
        super(props);
        let inputData = props.data.timeSeries;

        const ema26 = ema()
            .id(0)
            .options({windowSize: 26})
            .merge((d, c) => {
                d.ema26 = c;
            })
            .accessor(d => d.ema26);

        const ema12 = ema()
            .id(1)
            .options({windowSize: 12})
            .merge((d, c) => {
                d.ema12 = c;
            })
            .accessor(d => d.ema12);

        const macdCalculator = macd()
            .options({
                fast: 12,
                slow: 26,
                signal: 9,
            })
            .merge((d, c) => {
                d.macd = c;
            })
            .accessor(d => d.macd);

        const smaVolume50 = sma()
            .id(3)
            .options({
                windowSize: 50,
                sourcePath: "volume",
            })
            .merge((d, c) => {
                d.smaVolume50 = c;
            })
            .accessor(d => d.smaVolume50);

        const maxWindowSize = getMaxUndefined([ema26,
            ema12,
            macdCalculator,
            smaVolume50
        ]);

        const hurstAccessor = (d) => d.hurst;
        const rickerWaveletAccessor = (d) => d.Ricker;
        const paulWaveletAccessor = (d) => d.Paul;
        const dogWaveletAccessor = (d) => d.DOG;

        /* SERVER - START */
        const dataToCalculate = inputData.slice(-LENGTH_TO_SHOW - maxWindowSize);

        const calculatedData = ema26(ema12(macdCalculator(smaVolume50(dataToCalculate))));
        const indexCalculator = discontinuousTimeScaleProviderBuilder().indexCalculator();
        debugger;
        // console.log(inputData.length, dataToCalculate.length, maxWindowSize)
        const {index} = indexCalculator(calculatedData);
        /* SERVER - END */

        const xScaleProvider = discontinuousTimeScaleProviderBuilder()
            .withIndex(index);
        const {data: linearData, xScale, xAccessor, displayXAccessor} = xScaleProvider(calculatedData.slice(-LENGTH_TO_SHOW));

        // console.log(head(linearData), last(linearData))
        // console.log(linearData.length)

        this.state = {
            ema26,
            ema12,
            macdCalculator,
            smaVolume50,
            linearData,
            data: linearData,
            xScale,
            xAccessor, displayXAccessor,
            hurstAccessor,
            rickerWaveletAccessor,
            paulWaveletAccessor,
            dogWaveletAccessor
        };
        this.handleDownloadMore = this.handleDownloadMore.bind(this);
    }

    handleDownloadMore(start, end) {
        if (Math.ceil(start) === end) return;
        // console.log("rows to download", rowsToDownload, start, end)
        const {data: prevData, ema26, ema12, macdCalculator, smaVolume50} = this.state;
        let inputData = this.props.data.timeSeries;


        if (inputData.length === prevData.length) return;

        const rowsToDownload = end - Math.ceil(start);

        const maxWindowSize = getMaxUndefined([ema26,
            ema12,
            macdCalculator,
            smaVolume50
        ]);

        /* SERVER - START */
        const dataToCalculate = inputData
            .slice(-rowsToDownload - maxWindowSize - prevData.length, -prevData.length);

        const calculatedData = ema26(ema12(macdCalculator(smaVolume50(dataToCalculate))));
        const indexCalculator = discontinuousTimeScaleProviderBuilder()
            .initialIndex(Math.ceil(start))
            .indexCalculator();
        const {index} = indexCalculator(
            calculatedData
                .slice(-rowsToDownload)
                .concat(prevData));
        /* SERVER - END */

        const xScaleProvider = discontinuousTimeScaleProviderBuilder()
            .initialIndex(Math.ceil(start))
            .withIndex(index);

        const {data: linearData, xScale, xAccessor, displayXAccessor} = xScaleProvider(calculatedData.slice(-rowsToDownload).concat(prevData));

        // console.log(linearData.length)
        setTimeout(() => {
            // simulate a lag for ajax
            this.setState({
                data: linearData,
                xScale,
                xAccessor,
                displayXAccessor,
            });
        }, 300);
    }

    render() {
        const {type, width, ratio} = this.props;
        const {data, ema26, ema12, macdCalculator, smaVolume50, xScale, xAccessor, displayXAccessor} = this.state;

        if (this.props.showDetails)
            return (
                <ChartCanvas ratio={ratio} width={width} height={1250}
                             margin={{left: 70, right: 70, top: 20, bottom: 30}} type={type}
                             seriesName="MSFT"
                             data={data}
                             xScale={xScale} xAccessor={xAccessor} displayXAccessor={displayXAccessor}
                             onLoadMore={this.handleDownloadMore}>
                    <Chart id={1} height={400}
                           yExtents={[d => [d.high, d.low], ema26.accessor(), ema12.accessor()]}
                           padding={{top: 10, bottom: 20}}>
                        <XAxis axisAt="bottom" orient="bottom" showTicks={true} outerTickSize={0}/>
                        <YAxis axisAt="right" orient="right" ticks={5}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <AreaSeries
                            yAccessor={d => d.close}
                            stroke="#ff7f0e"
                            fill="#ff7f0e"
                        />
                        <LineSeries yAccessor={ema26.accessor()} stroke={ema26.stroke()}/>
                        <LineSeries yAccessor={ema12.accessor()} stroke={ema12.stroke()}/>

                        <CurrentCoordinate yAccessor={ema26.accessor()} fill={ema26.stroke()}/>
                        <CurrentCoordinate yAccessor={ema12.accessor()} fill={ema12.stroke()}/>

                        <EdgeIndicator itemType="last" orient="right" edgeAt="right"
                                       yAccessor={d => d.close} fill={d => d.close > d.open ? "#6BA583" : "#FF0000"}/>

                        <OHLCTooltip origin={[-40, 0]}/>
                        <MovingAverageTooltip
                            onClick={(e) => console.log(e)}
                            origin={[-38, 15]}
                            options={[
                                {
                                    yAccessor: ema26.accessor(),
                                    type: ema26.type(),
                                    stroke: ema26.stroke(),
                                    ...ema26.options(),
                                },
                                {
                                    yAccessor: ema12.accessor(),
                                    type: ema12.type(),
                                    stroke: ema12.stroke(),
                                    ...ema12.options(),
                                },
                            ]}
                        />
                    </Chart>

                    <text x="20" y="450" font-family="sans-serif" font-size="20px" fill="black">HURST</text>

                    <Chart id={2} height={150}
                           yExtents={this.state.hurstAccessor}
                           origin={(w, h) => [0, h - 800]} padding={{top: 10, bottom: 10}}>
                        <XAxis axisAt="bottom" orient="bottom"/>
                        <YAxis axisAt="right" orient="right" ticks={2}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <SimpleSeries accessor={this.state.hurstAccessor}/>
                        <StraightLine
                            yValue={0.5}/>
                    </Chart>

                    {/*Wavelet Part*/}

                    <text x="20" y="600" font-family="sans-serif" font-size="20px" fill="black">Paul</text>

                    <Chart id={4} height={150}
                           yExtents={this.state.paulWaveletAccessor}
                           origin={(w, h) => [0, h - 600]} padding={{top: 10, bottom: 10}}>
                        <XAxis axisAt="bottom" orient="bottom"/>
                        <YAxis axisAt="right" orient="right" ticks={2}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <SimpleSeries accessor={this.state.paulWaveletAccessor}/>
                    </Chart>

                    <text x="20" y="800" font-family="sans-serif" font-size="20px" fill="black">Ricker</text>

                    <Chart id={5} height={150}
                           yExtents={this.state.rickerWaveletAccessor}
                           origin={(w, h) => [0, h - 400]} padding={{top: 10, bottom: 10}}>
                        <XAxis axisAt="bottom" orient="bottom"/>
                        <YAxis axisAt="right" orient="right" ticks={2}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <SimpleSeries accessor={this.state.rickerWaveletAccessor}/>
                    </Chart>

                    <text x="20" y="1000" font-family="sans-serif" font-size="20px" fill="black">DOG</text>

                    <Chart id={6} height={150}
                           yExtents={this.state.dogWaveletAccessor}
                           origin={(w, h) => [0, h - 200]} padding={{top: 10, bottom: 10}}>
                        <XAxis axisAt="bottom" orient="bottom"/>
                        <YAxis axisAt="right" orient="right" ticks={2}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <SimpleSeries accessor={this.state.dogWaveletAccessor}/>
                    </Chart>

                    <CrossHairCursor />
                </ChartCanvas>
            );
        else
            return (
                <ChartCanvas ratio={ratio} width={width} height={500}
                             margin={{left: 70, right: 70, top: 20, bottom: 30}} type={type}
                             seriesName="MSFT"
                             data={data}
                             xScale={xScale} xAccessor={xAccessor} displayXAccessor={displayXAccessor}
                             onLoadMore={this.handleDownloadMore}>
                    <Chart id={1} height={400}
                           yExtents={[d => [d.high, d.low], ema26.accessor(), ema12.accessor()]}
                           padding={{top: 10, bottom: 20}}>
                        <XAxis axisAt="bottom" orient="bottom" showTicks={true} outerTickSize={0}/>
                        <YAxis axisAt="right" orient="right" ticks={5}/>

                        <MouseCoordinateX
                            at="bottom"
                            orient="bottom"
                            displayFormat={timeFormat("%Y-%m-%d")}/>
                        <MouseCoordinateY
                            at="right"
                            orient="right"
                            displayFormat={format(".2f")}/>

                        <AreaSeries
                            yAccessor={d => d.close}
                            stroke="#ff7f0e"
                            fill="#ff7f0e"
                        />
                        <LineSeries yAccessor={ema26.accessor()} stroke={ema26.stroke()}/>
                        <LineSeries yAccessor={ema12.accessor()} stroke={ema12.stroke()}/>

                        <CurrentCoordinate yAccessor={ema26.accessor()} fill={ema26.stroke()}/>
                        <CurrentCoordinate yAccessor={ema12.accessor()} fill={ema12.stroke()}/>

                        <EdgeIndicator itemType="last" orient="right" edgeAt="right"
                                       yAccessor={d => d.close} fill={d => d.close > d.open ? "#6BA583" : "#FF0000"}/>

                        <OHLCTooltip origin={[-40, 0]}/>
                        <MovingAverageTooltip
                            onClick={(e) => console.log(e)}
                            origin={[-38, 15]}
                            options={[
                                {
                                    yAccessor: ema26.accessor(),
                                    type: ema26.type(),
                                    stroke: ema26.stroke(),
                                    ...ema26.options(),
                                },
                                {
                                    yAccessor: ema12.accessor(),
                                    type: ema12.type(),
                                    stroke: ema12.stroke(),
                                    ...ema12.options(),
                                },
                            ]}
                        />
                    </Chart>
                    <CrossHairCursor />
                </ChartCanvas>
            );
    }
}

CandleStickChartPanToLoadMore.propTypes = propTypes;

CandleStickChartPanToLoadMore.defaultProps = {
    type: "svg",
};

CandleStickChartPanToLoadMore = fitWidth(CandleStickChartPanToLoadMore);

export default CandleStickChartPanToLoadMore;
