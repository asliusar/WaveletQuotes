import React from "react";
import {connect} from "react-redux";
import {Card, CardHeader, CardMedia, CardActions, DropDownMenu, MenuItem, FlatButton} from "material-ui";

import styles from "./css/styles.css";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.object,
    data: React.PropTypes.object
};

const IMAGE_HEADER = "data:image/png;base64, ";

export class Details extends React.Component {
    render() {
        const {dispatch, analysis} = this.props;
        const waveletDetails = Object.entries(analysis.data.waveletDetails).map(([wavelet,image])=>{
            return (
            <Card className={styles.card}>
                <CardHeader title={wavelet} tyle={styles.header_title}/>
                <CardMedia>
                    <img src={IMAGE_HEADER + image} />
                </CardMedia>
            </Card>
            );
        });
        return (
            <div className={styles.container}>
                {
                    analysis.showDetails && waveletDetails
                }
            </div>
        );
    }
}

Details.propTypes = propTypes;

function mapStateToProps(state) {
    const {filter} = state;
    return {
        filter
    };
}

export default connect(mapStateToProps)(Details);