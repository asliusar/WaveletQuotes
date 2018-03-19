import React from 'react';
import {browserHistory} from 'react-router';
import autobind from 'autobind-decorator'
import {Card, CardHeader, CardMedia, CardActions, FlatButton} from 'material-ui';
import styles from './css/styles.css'
import {showUrl} from "../../api/show";

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    showInfo: React.PropTypes.object
};

class ShowListElement extends React.Component {
    static generateSubtitle(date) {
        return 'Year: ';
    }

    @autobind
    handleShowFullInfoButtonClicked() {
        browserHistory.push(showUrl + this.props.showInfo.id);
    }

    render() {
        return (
            <Card className={styles.show_container} key={this.props.showInfo.id}>
                <CardHeader
                    className={styles.show_header}
                    subtitle={ShowListElement.generateSubtitle(this.props.showInfo.date)}
                    title={this.props.showInfo.name}
                />
                <div className={styles.image_wrapper}>
                    {
                        this.props.showInfo.poster &&
                        <CardMedia>
                            <img src={this.props.showInfo.poster} className={styles.panel_image}/>
                        </CardMedia>
                    }

                </div>
                <CardActions>
                    <FlatButton
                        label="Details"
                        primary={true}
                        onClick={this.handleShowFullInfoButtonClicked}
                    />
                </CardActions>
            </Card>
        );
    }
}

ShowListElement.propTypes = propTypes;
export default ShowListElement;